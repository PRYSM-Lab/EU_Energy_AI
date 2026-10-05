import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ==============================
# GLOBAL STYLE
# ==============================
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.linewidth": 1.5,
    "grid.alpha": 0.9,
    "grid.linestyle": "--"
})

COLORS = {
    "Solar": "#FFD700", "WindOn": "#90EE90", "WindOff": "#228B22",
    "Nuclear": "#A52A2A", "CCGT": "#808080", "CCGTCCS": "#4F4F4F",
    "H2CCGT": "#FF69B4", "Hydro": "#4169E1", "Biomass": "#9370DB",
    "BiomasCCS": "#D8BFD8"
}

tech_order_gen = ["Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", "Biomass", "BiomasCCS", "WindOff", "WindOn", "Solar"]

# ==============================
# LOAD DATA FROM EXCEL
# ==============================
excel_file = 'Europe with and without flex.xlsx'
xls = pd.ExcelFile(excel_file)

# لیست ۴ سناریو بر اساس نام شیت‌ها
scenarios_keys = xls.sheet_names[:4]

scenario_data = {}
demand_data = {}

for sheet in scenarios_keys:
    df = pd.read_excel(xls, sheet_name=sheet)
    
    # خواندن تکنولوژی‌ها
    scenario_data[sheet] = {col: df[col].values for col in tech_order_gen if col in df.columns}
    
    # خواندن تقاضا
    if 'Demand' in df.columns:
        demand_data[sheet] = df['Demand'].values

# ==============================
# ROW-WISE Y-LIMIT CALCULATION (for 2x2 grid)
# ==============================
scenarios = list(scenario_data.items())
row1_max = 0  # ردیف اول (سناریوی ۱ و ۲)
row2_max = 0  # ردیف دوم (سناریوی ۳ و ۴)

for i, (scenario, tech_data) in enumerate(scenarios):
    stack_sum = np.sum([np.array(tech_data[t]) for t in tech_order_gen if t in tech_data], axis=0)
    scenario_peak = stack_sum.max()

    if scenario in demand_data:
        scenario_peak = max(scenario_peak, demand_data[scenario].max())

    if i < 2:
        row1_max = max(row1_max, scenario_peak)
    else:
        row2_max = max(row2_max, scenario_peak)

row1_max *= 1.05
row2_max *= 1.05

# ==============================
# PLOT SETUP (2x2)
# ==============================
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
axes = axes.flatten()

for i, (scenario, tech_data) in enumerate(scenario_data.items()):
    ax = axes[i]
    hours = np.arange(24)
    
    ax.grid(True, axis='y', zorder=0)
    ax.axhline(0, color='black', linewidth=1.5, zorder=2)

    stack_values = [tech_data[tech] for tech in tech_order_gen if tech in tech_data]
    colors = [COLORS[t] for t in tech_order_gen if t in tech_data]
    ax.stackplot(hours, stack_values, colors=colors, linewidth=0, zorder=5)

    if scenario in demand_data:
        dem_vals = demand_data[scenario]
        ax.step(hours, dem_vals, where='mid', color="black", linestyle="-", linewidth=2.5, label="Demand", zorder=6)
        
        # محاسبه Peak Demand و ساعت وقوع آن
        peak_val = np.max(dem_vals)/1000
        peak_hour = np.argmax(dem_vals)
        
        # درج اطلاعات Peak در بالای سمت راست هر نمودار
        ax.text(
            0.98, 0.90, 
            f"Peak: {peak_val:,.0f} GWh (h={peak_hour})", 
            transform=ax.transAxes, 
            fontsize=10, 
            ha='right', 
            va='top'
        )

    ax.set_title(f"{scenario}",  pad=7)
    ax.set_xlim(0, 23)
    ax.set_xticks(np.arange(0, 24, 2))
    ax.yaxis.set_major_locator(MultipleLocator(200000))
    ax.set_ylabel("Energy Dispatch (MWh)", fontsize=12)
    
    if i < 2:
        ax.set_ylim(0, row1_max)
    else:
        ax.set_ylim(0, row2_max)

# =========================================================
# ADD SIGNED DIFFERENCE (NET CHANGE) BARS FOR ROW 1 AND ROW 2
# =========================================================
row_pairs = [(0, 1), (2, 3)]

for row_idx, (sc1_idx, sc2_idx) in enumerate(row_pairs):
    if sc2_idx >= len(scenarios):
        continue
        
    sc1_name, sc1_techs = scenarios[sc1_idx]
    sc2_name, sc2_techs = scenarios[sc2_idx]
    
    ax_right = axes[sc2_idx]
    
    # ایجاد محور کوچک در سمت راست
    ax_bar = inset_axes(
        ax_right,
        width="6%",
        height="85%",
        loc="center left",
        bbox_to_anchor=(1.18, 0, 1, 1),
        bbox_transform=ax_right.transAxes,
        borderpad=0,
    )

    # محاسبه اختلاف واقعی تولید (سناریوی دوم منهای سناریوی اول)
    tech_diffs = {}
    for tech in tech_order_gen:
        val1 = np.sum(sc1_techs.get(tech, 0))
        val2 = np.sum(sc2_techs.get(tech, 0))
        tech_diffs[tech] = (val2 - val1)/1000  # مثبت = افزایش، منفی = کاهش

    # جداسازی مقادیر افزایش و کاهش برای پشته‌سازی (Stacking)
    pos_bottom = 0
    neg_bottom = 0

    for tech in tech_order_gen:
        diff_val = tech_diffs.get(tech, 0)
        if diff_val == 0:
            continue

        color = COLORS[tech]

        if diff_val > 0:
            # بخش افزایش (بالای صفر)
            ax_bar.bar(
                x=0,
                height=diff_val,
                bottom=pos_bottom,
                color=color,
                width=0.5,
            )
            pos_bottom += diff_val
        else:
            # بخش کاهش (پایین صفر)
            ax_bar.bar(
                x=0,
                height=diff_val,  # مقدار منفی است
                bottom=neg_bottom,
                color=color,
                width=0.5,
            )
            neg_bottom += diff_val

    # خط راهنمای صفر
    ax_bar.axhline(0, color='black', linewidth=0.8)

    # تنظیم محدوده Y محور اختصاصی تغییرات
    max_val = max(pos_bottom, 1)
    min_val = min(neg_bottom, -1)
    ax_bar.set_ylim(min_val * 1.15, max_val * 1.15)

    ax_bar.set_xlim(-0.4, 0.8)
    ax_bar.set_xticks([])
    ax_bar.set_ylabel("Δ Generation (GWh)", fontsize=9)
    ax_bar.tick_params(axis="y", labelsize=7.5, direction="out", length=3)

    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    ax_bar.spines["bottom"].set_visible(False)
    ax_bar.spines["left"].set_linewidth(0.8)
    ax_bar.spines["left"].set_color("black")

fig.subplots_adjust(left=0.07, right=0.91, top=0.93, bottom=0.15, wspace=0.25, hspace=0.25)

# ==============================
# GLOBAL LEGEND
# ==============================
legend_elements = [Line2D([0], [0], color='black', lw=2, label='Demand')]
legend_elements += [plt.Rectangle((0, 0), 1, 1, color=COLORS[t], ec="w") for t in tech_order_gen[::-1]]

fig.legend(handles=legend_elements, 
           labels=["Demand"] + tech_order_gen[::-1],
           loc='lower center', ncol=6,
           bbox_to_anchor=(0.5, 0.02),
           frameon=False, fontsize=10,
           bbox_transform=fig.transFigure)

plt.savefig('Daily_4Scenarios_Signed_Dev.png', dpi=300, bbox_inches='tight')
plt.show()