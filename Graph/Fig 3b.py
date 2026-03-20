import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.lines import Line2D
plt.rcParams["font.family"] = "serif"

# ۱. خواندن فایل اکسل
file_path = 'Capacity Factor.xlsx'
try:
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"error")

scenarios = ["ICIS Base", "ICIS Pessimistic Def", "ICIS Pessimistic Med", "ICIS Pessimistic End"]
techs = ['Wind', 'Solar', 'Battery', 'CCGT', 'CCGTCCS', 'Biomass', 'H2CCGT', 'Nuclear']

design_config = {
    "ICIS Base": "#000000",
    "ICIS Pessimistic Def": "#e63946",
    "ICIS Pessimistic Med": "#0077b6",
    "ICIS Pessimistic End": "#33CC33"
}

line_style_config = {
    "ICIS Base": "-",
    "ICIS Pessimistic Def": "--",
    "ICIS Pessimistic Med": "-.",
    "ICIS Pessimistic End": ":"
}

scenario_offset = {
    "ICIS Base": -0.9,
    "ICIS Pessimistic Def": -0.3,
    "ICIS Pessimistic Med": 0.3,
    "ICIS Pessimistic End": 0.9
}

fig, axes = plt.subplots(4, 2, figsize=(15, 18))
axes = axes.flatten()

for i, tech in enumerate(techs):
    ax1 = axes[i]
    ax2 = ax1.twinx()
    ax2.patch.set_alpha(0) 

    ax1.set_title(f"{tech}", fontsize=14, fontweight='bold', pad=15)

    df_tech = df[df['Technology'] == tech]

    cf_min = df_tech['CF'].min()
    cf_max = df_tech['CF'].max()

    padding = (cf_max - cf_min) * 0.15
    if padding == 0:
        padding = 0.02

    ax2.set_ylim(cf_min - padding, cf_max + padding)

    for sc in scenarios:
        df_sc = df_tech[df_tech['Scenario'] == sc].sort_values('Year')

        if not df_sc.empty:
            x = df_sc['Year'].values
            y_cap = df_sc['Capacity'].values
            y_cf = df_sc['CF'].values

            if len(x) > 2:
                x_smooth = np.linspace(x.min(), x.max(), 300)
                spl = make_interp_spline(x, y_cap, k=3)
                y_smooth = spl(x_smooth)

                ax1.plot(
                    x_smooth, y_smooth,
                    color=design_config[sc],
                    linewidth=2.5,
                    linestyle=line_style_config[sc],
                    alpha=0.95,
                    zorder=3
                )
            else:
                ax1.plot(
                    x, y_cap,
                    color=design_config[sc],
                    linewidth=2.5,
                    linestyle=line_style_config[sc],
                    alpha=0.95,
                    zorder=3
                )

            x_shifted = x + scenario_offset[sc]

            ax2.scatter(
                x_shifted, y_cf,
                color=design_config[sc],
                s=130,
                alpha=0.65,
                edgecolors='black',
                linewidth=0.7,
                zorder=5
            )

    ax1.set_ylabel("Capacity (GW)", fontsize=14, fontweight='bold')
    ax2.set_ylabel("CF", fontsize=14, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.5)

custom_lines = [
    Line2D([0], [0],
           color=design_config[sc],
           lw=3,
           linestyle=line_style_config[sc])
    for sc in scenarios
]

fig.legend(custom_lines, scenarios,
           loc='lower center',
           bbox_to_anchor=(0.5, -0.01),
           ncol=4,
           fontsize=14,
           frameon=False)

plt.tight_layout(rect=[0, 0.04, 1, 0.99])
plt.subplots_adjust(hspace=0.55, wspace=0.35)

plt.savefig('Energy_Plot.png', dpi=300, bbox_inches='tight')

plt.show()
