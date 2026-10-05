import warnings
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore", category=UserWarning)

# Style
matplotlib.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 9,
        "legend.fontsize": 8.0,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.dpi": 300,
    }
)

# Mappings
YEAR_MAP = {1: 2025, 2: 2030, 3: 2035, 4: 2040, 5: 2045, 6: 2050}

TECH_DISPLAY = {
    "Battery": "Battery",
    "Biomass": "Biomass",
    "BiomassCCS": "BiomassCCS",
    "CCGT": "CCGT",
    "CCGTCCS": "CCGTCCS",
    
    "Gas": "Gas (other)",
    "H2CCGT": "H₂ CCGT",
    "Hydro": "Hydro",
    "Nuclear": "Nuclear",
    "Oil": "Oil & Coal",
    "PumpHy": "Pumped Hydro",
    "Solar": "Solar",
    "WindOff": "Wind Offshore",
    "WindOn": "Wind Onshore",
}

TECH_STYLE = {
    "Solar": {"color": "#D48900", "marker": "o", "label": "Solar PV"},
    "WindOn": {"color": "#1A65B0", "marker": "^", "label": "Wind Onshore"},
    "WindOff": {"color": "#0D8C58", "marker": "s", "label": "Wind Offshore"},
    "CCGT": {"color": "#C9501A", "marker": "X", "label": "Gas CCGT"},
    "Nuclear": {"color": "#3A2B9C", "marker": "D", "label": "Nuclear"},
    "Hydro": {"color": "#005C00", "marker": "v", "label": "Hydro"},
    "H2CCGT": {"color": "#C44F7A", "marker": "P", "label": "H₂ CCGT"},
    "Battery": {"color": "#6A6A6A", "marker": "*", "label": "Battery"},
    "PumpHy": {"color": "#4682B4", "marker": "h", "label": "Pumped Hydro"},
    "Biomass": {"color": "#8B7355", "marker": "p", "label": "Biomass"},
    "BiomassCCS": {"color": "#4A3B2A", "marker": "H", "label": "Biomass+CCS"},
    "CCGTCCS": {"color": "#A63D15", "marker": "<", "label": "Gas CCS"},
    "Coal": {"color": "#2D2D2D", "marker": "x", "label": "Coal"},
    "Gas": {"color": "#E8874A", "marker": "+", "label": "Gas (other)"},
    "Oil": {"color": "#8B1A1A", "marker": "8", "label": "Oil"},
}


# Data Loading
def load_model_data(path: str) -> pd.DataFrame:
  df = pd.read_excel(path)
  df = df.rename(
      columns={"j": "technology", "c": "country", "t": "year_idx", "CAP": "cap_MW"}
  )
  df["year"] = df["year_idx"].map(YEAR_MAP)
  df["cap_model"] = df["cap_MW"] 
  return df[["technology", "country", "year", "cap_model"]]


def load_reference_data(path: str) -> pd.DataFrame:
  df = pd.read_excel(path)
  df = df.rename(
      columns={"j": "technology", "c": "country", "t": "year_idx", "CAP": "cap_MW"}
  )
  df["year"] = df["year_idx"].map(YEAR_MAP)
  df["cap_ref"] = df["cap_MW"] 
  return df[["technology", "country", "year", "cap_ref"]]


def merge_model_reference(
    df_model: pd.DataFrame, df_ref: pd.DataFrame
) -> pd.DataFrame:
  df = df_model.merge(
      df_ref, on=["technology", "country", "year"], how="inner"
  )
  both_zero = (df["cap_model"] < 1e-6) & (df["cap_ref"] < 1e-6)
  df = df[~both_zero].copy()
  return df


# Compute Metrics
def compute_metrics(x_ref: np.ndarray, y_mod: np.ndarray) -> dict:
  x = np.asarray(x_ref, float)
  y = np.asarray(y_mod, float)

  valid = np.isfinite(x) & np.isfinite(y) & (x > 1e-4)
  x, y = x[valid], y[valid]
  n = len(x)

  if n < 2:
    return {
        k: np.nan
        for k in ["R2", "nRMSE", "RMSE", "MAPE", "Bias", "Pearson_r2", "n"]
    }

  res = y - x
  rmse = np.sqrt(np.mean(res**2))
  nrmse = rmse / np.mean(x) * 100
  r2 = 1.0 - np.sum(res**2) / np.sum((y - y.mean()) ** 2)
  mape = np.mean(np.abs(res / x)) * 100
  bias = np.mean(res / x) * 100
  pr, _ = stats.pearsonr(x, y)

  return {
      "R2": r2,
      "nRMSE": nrmse,
      "RMSE": rmse,
      "MAPE": mape,
      "Bias": bias,
      "Pearson_r2": pr**2,
      "n": n,
  }


def metrics_by_group(
    df, group_col="technology", ref="cap_ref", mod="cap_model"
):
  rows = []
  for g, grp in df.groupby(group_col):
    m = compute_metrics(grp[ref].values, grp[mod].values)
    m[group_col] = g
    rows.append(m)

  return (
      pd.DataFrame(rows)
      .set_index(group_col)[["R2", "nRMSE", "MAPE", "Bias", "n"]]
  )


# Panel (a) Plot
def plot_panel_a(
    df: pd.DataFrame,
    ref_label: str = "Reference",
    panel_label: str = "",
    figsize: tuple = (3.5, 3.2),
    ax=None,
    save_path: str = None,
) -> tuple:
  if ax is None:
    fig, ax = plt.subplots(figsize=figsize)
  else:
    fig = ax.get_figure()

  gm = compute_metrics(df["cap_ref"].values, df["cap_model"].values)
  vmax = max(df["cap_ref"].max(), df["cap_model"].max()) * 1.06
  diag = np.array([0, vmax])

  ax.fill_between(
      diag,
      diag * 0.80,
      diag * 1.20,
      color="#888888",
      alpha=0.07,
      zorder=0,
      label="±20% band",
  )
  ax.plot(
      diag,
      diag * 1.20,
      color="#888888",
      lw=0.5,
      ls=":",
      alpha=0.5,
      zorder=1,
  )
  ax.plot(
      diag,
      diag * 0.80,
      color="#888888",
      lw=0.5,
      ls=":",
      alpha=0.5,
      zorder=1,
  )
  ax.plot(
      diag, diag, color="#222222", lw=0.9, ls="--", zorder=2, label="1:1 line"
  )

  tech_order = [t for t in TECH_STYLE if t in df["technology"].unique()]
  tech_order += [
      t for t in df["technology"].unique() if t not in TECH_STYLE
  ]

  for tech in tech_order:
    sub = df[df["technology"] == tech]
    sty = TECH_STYLE.get(tech, {"color": "gray", "marker": "o"})

    ax.scatter(
        sub["cap_ref"],
        sub["cap_model"],
        c=sty["color"],
        marker=sty["marker"],
        s=18,
        alpha=0.75,
        linewidths=0.2,
        edgecolors="white",
        zorder=3,
        label=TECH_DISPLAY.get(tech, tech),
    )

  ax.set_xlim(0, vmax)
  ax.set_ylim(0, vmax)
  ax.set_aspect("equal", adjustable="box")
  ax.set_xlabel("TYNDP 2024 (GW)", fontsize=8)
  ax.set_ylabel("This model (GW)", fontsize=8)
  ax.tick_params(labelsize=7)
  ax.grid(True, lw=0.3, color="#cccccc", zorder=0)
  ax.set_axisbelow(True)

  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)

  stats_str = (
      f"$R^2$    = {gm['R2']:.3f}\n"
      f"nRMSE = {gm['nRMSE']:.1f}%\n"
      f"MAPE  = {gm['MAPE']:.1f}%\n"
      f"Bias    = {gm['Bias']:+.1f}%\n"
      f"$n$       = {gm['n']}"
  )

  ax.text(
      0.97,
      0.03,
      stats_str,
      transform=ax.transAxes,
      fontsize=6.5,
      va="bottom",
      ha="right",
      fontfamily="monospace",
      bbox=dict(
          boxstyle="round,pad=0.35",
          fc="white",
          ec="#cccccc",
          lw=0.5,
          alpha=0.93,
      ),
  )
  tech_handles = [
        Line2D(
            [0],
            [0],
            marker=TECH_STYLE[t]["marker"],
            color=TECH_STYLE[t]["color"],  
            markerfacecolor=TECH_STYLE[t]["color"],   
            markeredgecolor=TECH_STYLE[t]["color"],  
            markeredgewidth=0.8,
            linestyle="None",  
            markersize=5,
            label=TECH_DISPLAY.get(t, TECH_STYLE[t].get("label", t)),
        )
        for t in tech_order
        if t in TECH_STYLE
    ]

  

  ref_handles = [
      Line2D([0], [0], color="#222222", lw=0.9, ls="--", label="1:1 line"),
      mpatches.Patch(fc="#888888", alpha=0.12, ec="none", label="±20%"),
  ]

  leg = ax.legend(
      handles=tech_handles + ref_handles,
      loc="upper left",
      fontsize=5.5,
      framealpha=0.93,
      edgecolor="#cccccc",
      borderpad=0.4,
      handlelength=1.0,
      handletextpad=0.4,
      labelspacing=0.22,
      ncol=2,
  )

  leg.get_frame().set_linewidth(0.4)

  ax.text(
      -0.16,
      1.06,
      panel_label,
      transform=ax.transAxes,
      fontsize=9,
      fontweight="bold",
      va="top",
  )

  if save_path:
    fig.savefig(save_path, bbox_inches="tight", dpi=300)
    print(f"Saved -> {save_path}")

  return fig, ax, gm


# Execution
if __name__ == "__main__":
  MODEL_PATH = r"C:\Users\Mohammed\statics.xlsx"
  REFERENCE_PATH = r"C:\Users\Mohammed\output_transformed.xlsx"

  print("Loading model data...")
  df_model = load_model_data(MODEL_PATH)
  print(
      f"{len(df_model)} rows | {df_model['country'].nunique()} countries |"
      f" {df_model['technology'].nunique()} technologies |"
      f" {df_model['year'].nunique()} years"
  )
  print(
      f"CAP range: {df_model['cap_model'].min():.2f} - "
      f"{df_model['cap_model'].max():.1f} GW"
  )

  print("\nLoading reference data...")
  df_ref = load_reference_data(REFERENCE_PATH)
  print(
      f"{len(df_ref)} rows | {df_ref['country'].nunique()} countries |"
      f" {df_ref['technology'].nunique()} technologies |"
      f" {df_ref['year'].nunique()} years"
  )
  print(
      f"Reference CAP range: {df_ref['cap_ref'].min():.2f} - "
      f"{df_ref['cap_ref'].max():.1f} GW"
  )

  df = merge_model_reference(df_model, df_ref)
  print(f"After merge & filtering trivial zeros: {len(df)} rows")

  print("\nGlobal Validation Metrics")
  gm = compute_metrics(df["cap_ref"].values, df["cap_model"].values)

  for k, v in gm.items():
    if k == "n":
      print(f"{'n':12s}: {v}")
    else:
      print(f"{k:12s}: {v:.4f}")

  print("\nPer-Technology Metrics")
  pt = metrics_by_group(df, group_col="technology")
  print(pt.sort_values("MAPE").round(2).to_string())

  print("\nPer-Country Metrics (worst 10 by MAPE)")
  pc = metrics_by_group(df, group_col="country")
  print(pc.sort_values("MAPE", ascending=False).head(10).round(2).to_string())

  
  fig_a, ax_a, _ = plot_panel_a(
      df,
      ref_label="Reference",
      save_path=r"C:\Users\Mohammed\panel_a.pdf",
  )

  plt.tight_layout(pad=0.6)
  plt.show()