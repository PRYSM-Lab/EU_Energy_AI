import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import TwoSlopeNorm

plt.rcParams["font.family"] = "serif"

# ===============================
df_raw = pd.read_excel('New - Copy.xlsx',sheet_name='Sheet3', header=[0,1], index_col=0)
df = df_raw.stack(level=[0,1], future_stack=True).reset_index()
df.columns = ['Year', 'Scenario', 'Technology', 'Value']

scenario_order = df.groupby('Scenario')['Value'].mean().sort_values().index.tolist()
df['Scenario'] = pd.Categorical(df['Scenario'], categories=scenario_order, ordered=True)

years = sorted(df['Year'].unique())
scenario_idx = np.arange(len(scenario_order))
year_idx = np.arange(len(years))
scenario_map = {s:i for i,s in enumerate(scenario_order)}
year_map = {y:i for i,y in enumerate(years)}

# ===============================
tech = 'Emission'  

tech_data = df[df['Technology'] == tech]

Z = np.full((len(years), len(scenario_order)), np.nan)
for _, row in tech_data.iterrows():
    y_idx = year_map[row['Year']]
    x_idx = scenario_map[row['Scenario']]
    Z[y_idx, x_idx] = row['Value']

# ===============================
fig, ax = plt.subplots(figsize=(15, 8))

X, Y = np.meshgrid(scenario_idx, year_idx)

vmin, vmax = np.nanmin(Z), np.nanmax(Z)
if vmin < 0 < vmax:
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
else:
    norm = plt.Normalize(vmin=vmin, vmax=vmax)

cf = ax.contourf(X, Y, Z, levels=800, cmap='RdBu_r', norm=norm, extend='both', alpha=0.9)
cs = ax.contour(X, Y, Z, levels=13, colors='black', linewidths=0.4)
ax.clabel(cs, fmt='%1.0f', fontsize=8)





ax.set_xticks(scenario_idx)
ax.set_xticklabels(scenario_order, rotation=90, ha='right', fontsize=12)

ax.set_yticks(year_idx)
ax.set_yticklabels(years, fontsize=14)

ax.set_ylabel('Year', fontsize=18)

cbar = fig.colorbar(cf, ax=ax, fraction=0.045, pad=0.03)
cbar.set_label('Emission (Mton CO2)', fontsize=18)

plt.tight_layout()
plt.savefig('heatmap_single_tech.png', dpi=300, bbox_inches='tight')
plt.show()
