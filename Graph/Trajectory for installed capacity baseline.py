import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
plt.rcParams["font.family"] = "serif"

# ---------- داده‌ها ----------
data = {
    '2025': [228, 1, 104, 38,0, 269, 229, 34, 158, 32],
    '2030': [246, 3, 103, 38,0,  402, 339, 38, 158, 134],
    '2035': [326, 9, 98, 40,25, 612, 505, 97, 158, 134],
    '2040': [400, 32, 117, 61,49, 913, 651, 282, 158, 234],
    '2045': [402, 50, 134, 134,72, 1111, 768, 377, 158, 275],  
    '2050': [212, 40, 145, 174, 88, 1940, 899, 580, 158, 805],
}
categories = ['CCGT', 'CCGTCCS',  'Nuclear','Biomass','H2CCGT','Solar','WindOn','WindOff', 'Hydro', 'Battery']

df = pd.DataFrame(data, index=categories).T
df.index = df.index.astype(int)

years = df.index.values
x_smooth = np.linspace(years.min(), years.max(), 300)

color_map = {
    "Solar": "#ffbf00",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#1f77b4",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#17becf",
    'Battery':      "#9467bd",
    
}


colors = [color_map[c] for c in categories]

gap = 60

bottoms = []
tops = []

for year in df.index:
    sorted_data = df.loc[year].sort_values()
    bottom = {}
    top = {}
    base = 0
    for cat in sorted_data.index:
        bottom[cat] = base
        top[cat] = base + df.loc[year][cat]
        base = top[cat] + gap
    bottoms.append(bottom)
    tops.append(top)

fig, ax = plt.subplots(figsize=(14, 7))

for i, cat in enumerate(categories):
    y_bottom = [bottoms[j][cat] for j in range(len(df.index))]
    y_top = [tops[j][cat] for j in range(len(df.index))]

    yb_spline = make_interp_spline(years, y_bottom, k=3)(x_smooth)
    yt_spline = make_interp_spline(years, y_top, k=3)(x_smooth)

    ax.fill_between(x_smooth, yb_spline, yt_spline,
                    color=colors[i], label=cat, alpha=0.95)
    '''
    for j, year in enumerate(years):
        mid_val = (bottoms[j][cat] + tops[j][cat]) / 2
        ax.text(year, mid_val, str(df.loc[year][cat]),
                ha='center', va='center', fontsize=12, color='black')
'''
plt.rcParams["font.family"] = "serif"


ax.set_xticks(years)
ax.set_xticklabels(years, fontsize=18,   color='black')

#ax.set_title("Installed Capacity (GW) - Base Case", fontsize=20,fontweight='bold',)
ax.set_ylabel("Installed Capacity (GW)", fontsize=22, fontweight='bold',  color='black')
ax.tick_params(axis='y', labelsize=18, colors='black')

ax.legend(loc='upper left',ncol=2, fontsize=16, frameon=False)

ax.tick_params(axis='x', labelsize=18, colors='Black')

plt.tight_layout()
plt.show()