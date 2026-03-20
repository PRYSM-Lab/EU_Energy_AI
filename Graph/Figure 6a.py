import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.lines import Line2D

# ==============================
# GLOBAL STYLE
# ==============================
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.titlesize": 18,
    "axes.labelsize": 15,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.linewidth": 2.0,
    "grid.alpha": 0.6,
    "grid.linestyle": "--"
})

COLORS = {
    "Solar": "#FFD700", "WindOn": "#2ca02c", "WindOff": "#006400",
    "Nuclear": "#8B4513", "CCGT": "#7f7f7f", "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4", "Hydro": "#1E90FF", "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7", "Storage_Dis": "#CCFFFF", "Storage_CH": "#00FFFF",
    "Import/Export": "#FF8C00"
}

tech_order_gen = ["Nuclear","Hydro","CCGT","CCGTCCS","H2CCGT",
                  "Biomass","BECCS","WindOff","WindOn","Solar","Storage_Dis"]

countries = ["France","UK","Germany","Italy","Netherlands"]

file_matrix = [
    ("hourly_FR.xlsx","hourly_FR1.xlsx"),
    ("hourly_UK.xlsx","hourly_UK1.xlsx"),
    ("hourly_DE.xlsx","hourly_DE1.xlsx"),
    ("hourly_IT1.xlsx","hourly_IT.xlsx"),
    ("hourly_NL.xlsx","hourly_NL1.xlsx")
]

# ==============================
# TRUE SIGNED STACK FUNCTION
# ==============================
def stacked_signed(ax, x, positive_dict, negative_dict, colors):

    pos_base = np.zeros_like(x, dtype=float)
    neg_base = np.zeros_like(x, dtype=float)

    # --- Positive layers ---
    for k, v in positive_dict.items():
        ax.fill_between(x, pos_base, pos_base + v,
                        color=colors[k], linewidth=0)
        pos_base += v

    # --- Negative layers (reverse so small signals stay visible) ---
    for k, v in reversed(list(negative_dict.items())):
        ax.fill_between(x, neg_base, neg_base + v,
                        color=colors[k],
                        edgecolor='black',
                        linewidth=0.6)
        neg_base += v

    return pos_base, neg_base


def millions_formatter(x, pos):
    return f'{x/1e6:g}'


# ==============================
# FIGURE
# ==============================
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12,30))

for row in range(5):
    for col in range(2):

        ax = axes[row, col]

        try:
            df = pd.read_excel(file_matrix[row][col], sheet_name="Dispatch")
            df_demand = pd.read_excel(file_matrix[row][col], sheet_name="Demand")

            hours = np.arange(1,25)
            demand = df_demand["Demand"].values

            # ======================
            # Split physical flows
            # ======================
            gen_pos = {t: df[t].values for t in tech_order_gen if t in df}

            imp_exp = df["Import/Export"].values if "Import/Export" in df else np.zeros(24)
            imports = np.where(imp_exp > 0, imp_exp, 0)
            exports = np.where(imp_exp < 0, imp_exp, 0)

            storage_ch = df["Storage_CH"].values if "Storage_CH" in df else np.zeros(24)
            storage_ch = -np.abs(storage_ch)  # force sink sign

            positive_stack = dict(gen_pos)
            positive_stack["Import/Export"] = imports

            # Charging first so it sits near zero (visible)
            negative_stack = {
                "Storage_CH": storage_ch,
                "Import/Export": exports
            }

            # ======================
            # Draw signed dispatch
            # ======================
            stacked_signed(ax, hours, positive_stack, negative_stack, COLORS)

            # Demand overlay
            ax.step(hours, demand, where='mid',
                    color="black", linewidth=1.5, zorder=5)

            # ======================
            # PANEL-SPECIFIC SCALING
            # ======================
            pos_total = np.sum(np.vstack(list(positive_stack.values())), axis=0)
            neg_total = np.sum(np.vstack(list(negative_stack.values())), axis=0)

            local_max = max(pos_total.max(), demand.max())
            local_min = min(neg_total.min(), demand.min())

            yrange = local_max - local_min
            pad = 0.12 * yrange if yrange > 0 else 1.0

            ax.set_ylim(local_min - pad, local_max + pad)

            # ======================
            # Formatting
            # ======================
            ax.axhline(0, color='black', linewidth=1.8)
            ax.grid(True, axis='y')

            ax.set_xlim(1,24)
            ax.set_xticks([1,4,8,12,16,20,24])

            ax.margins(x=0.01, y=0.02)

            ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
            ax.yaxis.set_major_locator(MultipleLocator(80000))

            if row == 0:
                ax.set_title("Without AI" if col == 0 else "ICIS Base",
                             fontweight="bold", pad=13)

            if col == 0:
                ax.text(0.02,0.88,countries[row],
                        transform=ax.transAxes,
                        fontsize=12,fontweight='bold',
                        bbox=dict(facecolor='white',alpha=0.45,edgecolor='none'))
                ax.set_ylabel("TWh",fontweight='bold')
            if col == 1:
                ax.text(0.02,0.88,countries[row],
                        transform=ax.transAxes,
                        fontsize=12,fontweight='bold',
                        bbox=dict(facecolor='white',alpha=0.45,edgecolor='none'))
                ax.set_ylabel("TWh",fontweight='bold')   
                

        except Exception:
            ax.text(0.5,0.5,"Data Error",ha='center',transform=ax.transAxes)

# ==============================
# X labels
# ==============================
for ax in axes[4]:
    ax.set_xlabel("Hour of Day",fontsize=15,fontweight='bold')

# ==============================
# LEGEND
# ==============================
legend_elements = [Line2D([0],[0],color='black',lw=2.5,label='Demand')]
legend_elements += [plt.Rectangle((0,0),1,1,color=COLORS[t]) for t in tech_order_gen[::-1]]
legend_elements += [
    plt.Rectangle((0,0),1,1,color=COLORS["Storage_CH"],label="Charging"),
    plt.Rectangle((0,0),1,1,color=COLORS["Import/Export"],label="Imp/Exp")
]

fig.legend(handles=legend_elements,
           labels=["Demand"]+tech_order_gen[::-1]+["Charging","Imp/Exp"],
           loc='lower center',ncol=7,bbox_to_anchor=(0.5,-0.01),
           frameon=False,fontsize=14)

plt.tight_layout(rect=[0,0.08,1,0.99])
plt.subplots_adjust(hspace=0.3,wspace=0.3)

plt.savefig('Final_PanelScaled_Dispatch.png',dpi=300,bbox_inches='tight')
plt.show()