import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

# 1. تنظیم فونت استاندارد مقاله (Serif)
plt.rcParams['font.family'] = 'serif'

# 2. تعریف داده‌ها
technologies = [
    'CCGT',
    'CCGTCCS',
    'H2CCGT',
    'Nuclear',
    'Solar',
    'Wind\nOffshore',
    'Wind\nOnshore',
]

data_capacity = {
    '12 Day': [242, 33, 49, 110, 896, 273, 668],
    '17 Day': [262, 33, 52, 106, 940, 213, 675],
    '52 Day': [273, 33, 52, 107, 945, 213, 673],
}

data_cf = {
    '12 Day': [23, 42, 55, 82, 12, 47, 26.7],
    '17 Day': [27, 50, 54, 86, 12.5, 48, 25.8],
    '52 Day': [24.2, 43, 54, 85, 12.5, 48, 25.8],
}

df_cap = pd.DataFrame(data_capacity, index=technologies)
df_cf = pd.DataFrame(data_cf, index=technologies)

# 3. تعریف ساختار نمودار
fig, ax1 = plt.subplots(figsize=(8, 5.2), dpi=300)

x = np.arange(len(technologies))
width = 0.24

# پالت جدید: آبی، زرد پررنگ (خردلی آکادمیک) و طوسی
bar_colors = ['#1f4e78', '#d99b00', '#7f7f7f']
# رنگ‌های تیره متناظر برای واضح بودن مارکرها روی صفحه
marker_colors = ['#0d2840', '#8c6400', '#333333']
markers = ['o', 's', '^']

# 4. رسم میله‌ها
ax1.bar(
    x - width,
    df_cap['12 Day'],
    width,
    color=bar_colors[0],
    alpha=0.9,
    edgecolor='none',
)
ax1.bar(
    x,
    df_cap['17 Day'],
    width,
    color=bar_colors[1],
    alpha=0.9,
    edgecolor='none',
)
ax1.bar(
    x + width,
    df_cap['52 Day'],
    width,
    color=bar_colors[2],
    alpha=0.9,
    edgecolor='none',
)

ax1.set_ylabel('Installed Capacity (GW)', fontsize=9)
ax1.set_xticks(x)
ax1.set_xticklabels(technologies, fontsize=7)
ax1.set_ylim(0, 1050)
ax1.tick_params(axis='both', which='major')
ax1.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.5, color='#b0b0b0')
ax1.set_axisbelow(True)

# 5. رسم مارکرها
ax2 = ax1.twinx()

ax2.plot(
    x - width,
    df_cf['12 Day'],
    color=marker_colors[0],
    marker=markers[0],
    linestyle='None',
    markersize=6,
)
ax2.plot(
    x,
    df_cf['17 Day'],
    color=marker_colors[1],
    marker=markers[1],
    linestyle='None',
    markersize=6,
)
ax2.plot(
    x + width,
    df_cf['52 Day'],
    color=marker_colors[2],
    marker=markers[2],
    linestyle='None',
    markersize=6,
)

ax2.set_ylabel('Capacity Factor (%)', fontsize=9)
ax2.set_ylim(0, 100)
ax2.tick_params(axis='both', which='major')
ax2.grid(False)

# 6. قاب نمودار
for ax in [ax1, ax2]:
  for spine in ax.spines.values():
    spine.set_color('#444444')
    spine.set_linewidth(0.8)

# 7. ساخت Legend متناظر با رنگ‌های جدید
legend_elements = [
    mpatches.Patch(color=bar_colors[0], alpha=0.9, label='12 Day Capacity'),
    mpatches.Patch(color=bar_colors[1], alpha=0.9, label='17 Day Capacity'),
    mpatches.Patch(color=bar_colors[2], alpha=0.9, label='52 Day Capacity'),
    Line2D(
        [0],
        [0],
        color=marker_colors[0],
        marker=markers[0],
        linestyle='None',
        label='12 Day CF',
    ),
    Line2D(
        [0],
        [0],
        color=marker_colors[1],
        marker=markers[1],
        linestyle='None',
        label='17 Day CF',
    ),
    Line2D(
        [0],
        [0],
        color=marker_colors[2],
        marker=markers[2],
        linestyle='None',
        label='52 Day CF',
    ),
]

fig.legend(
    handles=legend_elements,
    loc='lower center',
    bbox_to_anchor=(0.5, 0.01),
    ncol=6,
    frameon=False,
    fontsize=6.5,
)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()