import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Circle, Patch

plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1

countries = ['UK', 'FR', 'DE', 'IE', 'ES', 'PT', 'PL', 'IT', 'NL', 'AT', 'GR', 'DK']
scenarios = ['Base Case', 'ICIS Base', ]
colors = [ '#FFFF00', '#A9A9A9']
data = []
real_values = {
    'Base Case': {
        'UK': (33, -17, 134), 'FR': (7, 39, 32), 'DE': (129, -2, 101), 'IE': (7.5, 4, 67),
        'ES': (29,46,30), 'PT': (5,19,33), 'PL': (102,23,73), 'IT': (85,-37,50), 
        'NL': (36,78,92), 'AT': (4.8,11,40), 'GR': (20,-10,51), 'DK': (3,30,82)
    },
    'ICIS Base': {
        'UK': (39.3, -31, 162), 'FR': (8, 38, 44), 'DE': (135, -3, 116), 'IE': (8.7, -4, 81),
        'ES': (32,-23,40), 'PT': (6,8,38), 'PL': (106,15,80), 'IT': (95,-35,54), 
        'NL': (40,84,102), 'AT': (6.4,-14,48), 'GR': (22,-14,58), 'DK': (4,3.7,92)
    },
    
}

data = []
for i, s in enumerate(scenarios):
    for c in countries:
        x_val, y_val, ai_val = real_values.get(s, {}).get(c, (0, 0, 0))
        data.append({
            'Country': c, 
            'Scenario': s, 
            'Color': colors[i],
            'X': x_val, 
            'Y': y_val, 
            'AI_Demand': ai_val
        })
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(10, 5), dpi=140)

for i, s in enumerate(scenarios):
    sub = df[df['Scenario'] == s]
    ax.scatter(sub['X'], sub['Y'], s=sub['AI_Demand']*40, 
               c=sub['Color'], edgecolors='black', linewidth=0.9, alpha=0.7)
    
    for _, row in sub.iterrows():
        if row['AI_Demand'] <= 40:
            ax.annotate(row['Country'], 
                        xy=(row['X'], row['Y']), 
                        xytext=(row['X'] +10, row['Y']+10 ),
                        fontsize=7,
                        arrowprops=dict(arrowstyle='-', color='black', linewidth=0.5))
        else:
            ax.text(row['X'], row['Y'], row['Country'], 
                    fontsize=8, ha='center', va='center')

ax.axhline(0, color='#333333', linewidth=0.8)
ax.axvline(0, color='#333333', linewidth=0.8)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)
ax.set_xlim(-5, 150) 
ax.set_ylim(-60, 100)
ax.grid(True, linestyle=':', alpha=0.6, zorder=0)

legend_elements = [Patch(facecolor=colors[i], edgecolor='black', label=scenarios[i]) for i in range(2)]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15),
          ncol=2, frameon=False, edgecolor='black', fontsize=12)
ax_leg = fig.add_axes([0.87, 0.71, 0.1, 0.19]) 
ax_leg.set_aspect('equal')
ax.tick_params(axis='both', which='major', labelsize=12)
ax_leg.set_title(r'LCOE (€/MWh)', fontsize=10, fontweight='bold', pad=10)
sizes = [160, 120, 80, 50, 30]
for s in sizes:
    r = np.sqrt(s * 6) / 65 
    circle = Circle((0.5, r), r, edgecolor='black',label='LCOE (£/MWh)', facecolor='none', linewidth=0.8)
    ax_leg.add_patch(circle)
    ax_leg.text(0.5, 2*r, str(s), ha='center', fontsize=9, va='bottom')

ax_leg.axis('off')

ax.set_xlabel('Cumulative Emissition 2030-2050 (MtCO2)', fontsize=12)
ax.set_ylabel('Net Electricity Trade (TWh/yr)', fontsize=12)
plt.tight_layout()
plt.show()