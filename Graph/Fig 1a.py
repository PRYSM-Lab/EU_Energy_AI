import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import TwoSlopeNorm
plt.rcParams["font.family"] = "serif"

# ===============================
df_raw = pd.read_excel('New - Copy.xlsx', header=[0,1], index_col=0)
df = df_raw.stack(level=[0,1]).reset_index()
df.columns = ['Year', 'Scenario', 'Technology', 'Value']

scenario_order = df.groupby('Scenario')['Value'].mean().sort_values().index.tolist()
df['Scenario'] = pd.Categorical(df['Scenario'], categories=scenario_order, ordered=True)

years = sorted(df['Year'].unique())
techs = ['Wind', 'Solar', 'Nuclear', 'CCGT', 'CCGTCCS', 'H2CCGT', 'Biomass', 'Oil & Coal']
x_scale = 2.0 
# ساخت mapping برای X و Y برای contour
scenario_idx = np.arange(len(scenario_order))
year_idx = np.arange(len(years))
scenario_map = {s:i for i,s in enumerate(scenario_order)}
year_map = {y:i for i,y in enumerate(years)}


# ===============================
# ===============================
cmap = plt.get_cmap('RdBu_r')




# ===============================
fig, axes = plt.subplots(2, 4, figsize=(50, 10), sharex=False, sharey=False)
axes = axes.flatten()

for i, tech in enumerate(techs):
    ax = axes[i]
    tech_data = df[df['Technology'] == tech]

    Z = np.full((len(years), len(scenario_order)), np.nan)
    for _, row in tech_data.iterrows():
        y_idx = year_map[row['Year']]
        x_idx = scenario_map[row['Scenario']]
        Z[y_idx, x_idx] = row['Value']
     

    

    vmin, vmax = np.nanmin(Z), np.nanmax(Z)
    if vmin < 0 < vmax:
        norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
    else:
        norm = plt.Normalize(vmin=vmin, vmax=vmax)

    X, Y = np.meshgrid(scenario_idx, year_idx)

    cf = ax.contourf(
        X, Y, Z, levels=100, cmap='RdBu_r', norm=norm, extend='both', alpha=0.9
    )
    

    cs = ax.contour(X, Y, Z, levels=7, colors='black', linewidths=0.2)
    ax.clabel(cs, inline=False, fmt='%1.0f', fontsize=8)

    ax.set_xticks(scenario_idx)
    ax.set_xticklabels(scenario_order, rotation=90, ha='right', fontsize=8)
    
    ax.set_yticks(year_idx)
    ax.set_yticklabels(years, fontsize=12)

    ax.set_title(tech.upper(), fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('')
    ax.set_ylabel('Year', fontsize=12)
    
    

    cbar = fig.colorbar(cf, ax=ax, fraction=0.045, pad=0.03)
    cbar.set_label('Generation Deviation (TWh)', fontsize=12)
# Color each scenario label individually

for j in range(len(techs), len(axes)):
    fig.delaxes(axes[j])

fig.subplots_adjust(top=0.96, bottom=0.15, hspace=0.65, wspace=0.65)

fig.canvas.draw()

fig.savefig('heatmap_results.png', dpi=300)
plt.savefig('heatmap_results.png', dpi=300, bbox_inches='tight')

plt.show()
