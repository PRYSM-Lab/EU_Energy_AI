
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# 1. Formatting
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1

# 2. Data
scenarios = ['ICIS Base', 'ICIS Pessimistic Def', 'ICIS Pessimistic Med', 'ICIS Pessimistic End']
colors = ['#000000', '#e63946', '#0077b6', '#33CC33']

scenario_values = {
    'ICIS Base': {'Peak2050': 1252, 'FirmShare': 21.9, 'LCOE': 62.2},
    'ICIS Pessimistic Def':  {'Peak2050': 1216, 'FirmShare': 24, 'LCOE': 64},
    'ICIS Pessimistic Med':  {'Peak2050': 1225, 'FirmShare': 23.9, 'LCOE': 63.7},
    'ICIS Pessimistic End':  {'Peak2050': 1235, 'FirmShare': 23.5, 'LCOE': 63},
}

df = pd.DataFrame([{
    'Scenario': s, 'Color': colors[i],
    'X': scenario_values[s]['Peak2050'],
    'Y': scenario_values[s]['FirmShare'],
    'LCOE': scenario_values[s]['LCOE']
} for i, s in enumerate(scenarios)])

# 3. Scaling (Safe range 60-66 to avoid sqrt errors)
LCOE_MIN_SCALE, LCOE_MAX_SCALE = 60, 66

def get_area(lcoe):
    norm = (lcoe - LCOE_MIN_SCALE) / (LCOE_MAX_SCALE - LCOE_MIN_SCALE)
    return 1000 + (norm * 4000)

df['Size'] = df['LCOE'].apply(get_area)

# 4. Main Plot
fig, ax = plt.subplots(figsize=(11, 7), dpi=200)

# Scatter plot
ax.scatter(df['X'], df['Y'], s=df['Size'], c=df['Color'],
           edgecolors='black', linewidth=1.0, alpha=0.7, zorder=5)

# Axis adjustments (Giving more space for large bubbles)
x_pad = (df['X'].max() - df['X'].min()) 
y_pad = (df['Y'].max() - df['Y'].min()) * 0.8
ax.set_xlim(df['X'].min() - x_pad, df['X'].max() + x_pad)
ax.set_ylim(df['Y'].min() - y_pad, df['Y'].max() + y_pad)
ax.grid(True, linestyle=':', alpha=0.6)

# 5. BOTTOM LEGEND: Scenario Colors
legend_elements = [Line2D([0], [0], marker='o', color='w', label=row['Scenario'],
                          markerfacecolor=row['Color'], markersize=12, 
                          markeredgecolor='black') for i, row in df.iterrows()]

ax.legend(handles=legend_elements, loc='upper center', 
          bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False, fontsize=10)

# 6. SIDE LEGEND: Nested (Concentric) Circles for LCOE
ax_leg = fig.add_axes([0.86, 0.8, 0.12, 0.25]) 
ax_leg.set_aspect('equal')
ax_leg.axis('off')

legend_vals = [65, 63, 61]
def get_radius_for_legend(val):
    return np.sqrt(get_area(val)) / 220 # Adjust divisor if circles look too big/small

for v in sorted(legend_vals, reverse=True):
    r = get_radius_for_legend(v)
    # y=r centers circles on a common bottom line (nesting)
    circle = Circle((0.3, r), r, facecolor='none', edgecolor='black', 
                    linewidth=0.8, transform=ax_leg.transAxes)
    ax_leg.add_patch(circle)
    # Label at top of each circle
    ax_leg.text(0.35, 2*r, f'{v}', transform=ax_leg.transAxes, va='center', fontsize=9)

ax_leg.text(0.4, -0.3, 'Average LCOE\n (€/MWh)', transform=ax_leg.transAxes, 
            ha='center', fontsize=10, fontweight='bold')

# 7. Labels
ax.set_xlabel('Peak Demand in 2050 (GWh)', fontsize=12)
ax.set_ylabel('Share of Firm Generation (%)', fontsize=12)
plt.tight_layout()
# Save with bbox_inches='tight' to capture both legends
plt.savefig('Final_Energy_Plot.png', dpi=300, bbox_inches='tight')
plt.show()
