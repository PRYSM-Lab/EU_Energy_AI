import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# تنظیم فونت
plt.rcParams["font.family"] = "serif"

# ==============================
# READ DATA
# ==============================
file_path = "all_countries_scenarios.xlsx"

df_dispatch = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

# ==============================
# CONFIGURATIONS
# ==============================
countries = df_dispatch["Country"].unique()[:5]
scenarios = ["Without DC", "ICIS Base"]

COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
    "Storage_Dis": "#CCFFFF",
    "Storage_CH": "#00FFFF",
    "Import/Export": "#FF8C00",
}

tech_order_gen = [
    "Nuclear",
    "Hydro",
    "CCGT",
    "CCGTCCS",
    "H2CCGT",
    "Biomass",
    "BECCS",
    "Import/Export",
    "WindOff",
    "WindOn",
    "Solar",
    "Storage_Dis",
]

# لیست تکنولوژی‌ها برای نمودار ستونی انحراف (بدون ذخیره‌سازها)
tech_order_bar = [
    t for t in tech_order_gen if t not in ["Storage_Dis", "Storage_CH"]
]

# ==============================
# CREATE 5x2 FIGURE
# ==============================
fig, axes = plt.subplots(
    nrows=5,
    ncols=2,
    figsize=(11, 9),
    sharex=False,
    sharey=False,
    gridspec_kw={"wspace": 0.25, "hspace": 0.6},
)

axes[0, 0].set_title("Without DC", fontsize=16)
axes[0, 1].set_title("ICIS Base", fontsize=16)

# ==============================
# PLOTTING LOOP
# ==============================
for r, country in enumerate(countries):
    for c, scenario in enumerate(scenarios):
        ax = axes[r, c]

        sub_df = df_dispatch[
            (df_dispatch["Country"] == country)
            & (df_dispatch["Scenario"] == scenario)
        ].sort_values("Hour")

        sub_demand = df_demand[
            (df_demand["Country"] == country)
            & (df_demand["Scenario"] == scenario)
        ].sort_values("Hour")

        if sub_df.empty:
            continue

        hours = sub_df["Hour"].values

        # 1. Stack Generation
        stack_values = [
            sub_df[tech].values if tech in sub_df.columns else np.zeros(len(hours))
            for tech in tech_order_gen
        ]
        stack_colors = [COLORS[tech] for tech in tech_order_gen]

        ax.stackplot(
            hours,
            stack_values,
            colors=stack_colors,
            edgecolor="black",
            linewidth=0.3,
        )

        # 2. Storage Charging
        ch_vals = np.zeros(len(hours))
        if "Storage_CH" in sub_df.columns:
            ch_vals = -np.abs(sub_df["Storage_CH"].values)
            ax.stackplot(
                hours,
                ch_vals,
                colors=[COLORS["Storage_CH"]],
                edgecolor="black",
                linewidth=0.3,
            )

        # 3. Demand Line & Peak Calculation
        demand_vals = np.array([])
        peak_demand_val = 0

        if not sub_demand.empty and "Demand" in sub_demand.columns:
            demand_vals = sub_demand["Demand"].values
            peak_demand_val = np.max(demand_vals)/1000

            ax.plot(
                hours,
                demand_vals,
                color="black",
                linestyle="--",
                linewidth=2,
                label="Demand",
            )

        # محاسبه محدوده Y اختصاصی با افست
        total_gen_per_hour = np.sum(stack_values, axis=0)
        max_y = np.max(total_gen_per_hour)
        if len(demand_vals) > 0:
            max_y = max(max_y, peak_demand_val)

        min_y = np.min(ch_vals) if np.min(ch_vals) < 0 else 0

        y_upper = max_y * 1.25 if max_y > 0 else 1
        y_lower = min_y * 1.10 if min_y < 0 else 0
        ax.set_ylim(y_lower, y_upper)

        # نمایش نام کشور (سمت چپ)
        ax.text(0.03, 0.85, country, transform=ax.transAxes, fontsize=11)

        # نمایش Peak Demand (سمت راست)
        ax.text(
            0.99,
            0.87,
            f"Peak: {peak_demand_val:,.0f} GW",
            transform=ax.transAxes,
            fontsize=9,
            ha="right",
        )

        # تنظیمات محورها
        ax.set_xlim(1, 24)
        ax.set_xticks([1, 6, 12, 18, 24])
        ax.tick_params(axis="both", labelsize=11)

        # فرمت علمی Y
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((6, 6))
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.get_offset_text().set_fontsize(9)

        ax.set_xlabel("Hour", fontsize=14)
        ax.set_ylabel("MWh", fontsize=14)

    # =========================================================
    # ADD DEVIATION SHARE BAR (ABSOLUTE DIFFERENCE SHARE)
    # =========================================================
    ax_right = axes[r, 1]

    # ایجاد محور کوچک در سمت راست
    ax_bar = inset_axes(
        ax_right,
        width="6%",
        height="85%",
        loc="center left",
        bbox_to_anchor=(1.2, 0, 1, 1),
        bbox_transform=ax_right.transAxes,
        borderpad=0,
    )

    # استخراج داده‌های دو سناریو برای کشور جاری
    sub_df_without = df_dispatch[
        (df_dispatch["Country"] == country)
        & (df_dispatch["Scenario"] == "Without DC")
    ]
    sub_df_base = df_dispatch[
        (df_dispatch["Country"] == country)
        & (df_dispatch["Scenario"] == "ICIS Base")
    ]

    # محاسبه قدر مطلق انحراف تولید هر تکنولوژی
    tech_deviations = {}
    for tech in tech_order_bar:
        val_without = sub_df_without[tech].sum() if tech in sub_df_without.columns else 0
        val_base = sub_df_base[tech].sum() if tech in sub_df_base.columns else 0
        
        # قدر مطلق انحراف
        tech_deviations[tech] = abs(val_base - val_without)

    total_deviation = sum(tech_deviations.values())

    bottom_pos = 0
    if total_deviation > 0:
        for tech in tech_order_bar:
            dev_val = tech_deviations.get(tech, 0)
            if dev_val <= 0:
                continue

            # سهم درصدی این تکنولوژی از کل انحرافات
            pct = (dev_val / total_deviation) * 100
            color = COLORS[tech]

            # رسم میله رنگی
            ax_bar.bar(
                x=0,
                height=pct,
                bottom=bottom_pos,
                color=color,
                width=0.5,
            )

            # درج عدد درصد خارج از میله در سمت راست
            if pct >= 2.0:
                ax_bar.text(
                    0.35,
                    bottom_pos + pct / 2,
                    f"{pct:.0f}",
                    va="center",
                    ha="left",
                    fontsize=7,
                    color="black",
                )

            bottom_pos += pct

    # تنظیمات محور Y استاندارد
    ax_bar.set_ylim(0, 100)
    ax_bar.set_xlim(-0.4, 0.8)

    # درجه‌بندی مدرج محور Y
    ax_bar.set_yticks([0, 20, 40, 60, 80, 100])
    ax_bar.set_xticks([])

    # تنظیمات ظاهری محور استاندارد
    ax_bar.set_ylabel("Deviation (%)", fontsize=10)
    ax_bar.tick_params(axis="y", labelsize=7.5, direction="out", length=3)

    # مخفی کردن خطوط بالا، راست و پایین و حفظ فقط خط عمودی چپ (محور Y)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    ax_bar.spines["bottom"].set_visible(False)
    ax_bar.spines["left"].set_linewidth(0.8)
    ax_bar.spines["left"].set_color("black")

# ==============================
# GLOBAL LEGEND
# ==============================
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t]) for t in tech_order_gen[::-1]
]
handles.extend(
    [
        plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
        plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2),
    ]
)

labels = tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(
    handles,
    labels,
    loc="lower center",
    fontsize=9,
    ncol=7,
    frameon=False,
    bbox_to_anchor=(0.5, -0.01),
)

plt.tight_layout(rect=[0, 0.05, 0.90, 0.98])
plt.show()