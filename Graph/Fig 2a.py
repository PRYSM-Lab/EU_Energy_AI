import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
import numpy as np

# =====================================================
# 1. Load world map
# =====================================================
url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
world = gpd.read_file(url)

# =====================================================
# 2. Europe countries
# =====================================================
europe_list = [
    'Albania', 'Austria', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czechia',
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
    'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia',
    'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom',
    'Montenegro', 'North Macedonia', 
]
europe = world[world['name'].isin(europe_list)].copy()

# =====================================================
# 3. Load Excel data
# =====================================================
df = pd.read_excel('AI Demand_All.xlsx')  

df = df[df['Country'].isin(europe_list)]

# =====================================================
iea_scenarios = [s for s in df['Scenario'].unique() if 'IEA' in s]
icis_scenarios = [s for s in df['Scenario'].unique() if 'ICIS' in s]
ms_scenarios = [s for s in df['Scenario'].unique() if 'McKinsey' in s]

scenario_order = iea_scenarios + icis_scenarios + ms_scenarios

group_colors = {}
for s in iea_scenarios:
    group_colors[s] = 'red'
for s in icis_scenarios:
    group_colors[s] = 'green'
for s in ms_scenarios:
    group_colors[s] = 'blue'

# =====================================================
rocket = sns.color_palette("rocket_r", as_cmap=True)
colors = ["#ffffff", rocket(0.25), rocket(0.45), rocket(0.60), rocket(0.75), rocket(0.90), "#1b0612"]
custom_cmap = mcolors.LinearSegmentedColormap.from_list("rocket_white_zero", colors)

vmin, vmax = 0, df['Value'].max()
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

# =====================================================
# 6. Plot 3x7 subplots
# =====================================================
fig, axes = plt.subplots(3, 7, figsize=(28, 12))
axes = axes.flatten()

for i, scen in enumerate(scenario_order):
    ax = axes[i]
    df_scen = df[df['Scenario'] == scen]
    map_data = europe.merge(df_scen, left_on='name', right_on='Country', how='left')

    # Plot map
    map_data.plot(
        column='Value',
        ax=ax,
        cmap=custom_cmap,
        norm=norm,
        edgecolor='black',
        linewidth=0.5
    )

    # Set limits and remove axes
    ax.set_xlim(-15, 35)
    ax.set_ylim(34, 72)
    ax.set_axis_off()

    # Scenario title colored by group
    ax.set_title(scen, fontsize=12, fontweight='bold')

# Remove extra axes if less than 21 scenarios
for j in range(len(scenario_order), len(axes)):
    fig.delaxes(axes[j])

fig.subplots_adjust(
    top=0.92,    # فاصله بالای پنل‌ها تا بالا
    bottom=0.12, # فاصله پایین پنل‌ها تا colorbar یا legend
    left=0.02,   # فاصله چپ
    right=0.98,  # فاصله راست
    hspace=0.17, # فاصله عمودی بین ردیف‌ها
    wspace=0.07  # فاصله افقی بین ستون‌ها
)

# colorbar مشترک
sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
sm._A = []
cbar = fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.04)
cbar.set_label('AI Demand (TWh)', fontsize=16)

# سپس plt.show() بدون tight_layout
plt.savefig('All Map.png', dpi=300, bbox_inches='tight')

#plt.tight_layout()
plt.show()
