import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['xtick.color'] = 'black'
plt.rcParams['ytick.color'] = 'black'

file_path = 'Final_8760_Profile ICIS.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet2')

scenarios = ['Without AI', 'ICIS US Profile', 'ICIS UK Profile']
colors = ['#009900', '#000099', '#CC0000'] 
labels =  ['Without AI', 'ICIS US Profile', 'ICIS UK Profile']

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

for i, col in enumerate(scenarios):
    ldc_values = df[col].sort_values(ascending=False).values / 1e6 
    hours = range(1, len(ldc_values) + 1)
    
    ax.plot(hours, ldc_values, color=colors[i], label=labels[i], linewidth=1, antialiased=True)

ax.set_xlabel('Hours', fontsize=8, fontweight='bold', color='black')
ax.set_ylabel('TWh Net Load: \n Demand - Renewable Generation', fontsize=8, fontweight='bold', color='black')
ax.tick_params(axis='both', which='both', labelsize=8, direction='in', bottom=True, left=True)
ax.axhline(0, color='black', linewidth=0.5, linestyle='-') 
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(frameon=False, loc='upper right', fontsize=7)

ax_ins = inset_axes(ax, width="35%", height="35%", loc='lower center', 
                    bbox_to_anchor=(0.07, 0.15, 1, 1), bbox_transform=ax.transAxes)

for i, col in enumerate(scenarios):
    ldc_values = df[col].sort_values(ascending=False).values / 1e6
    ax_ins.plot(hours, ldc_values, color=colors[i], linewidth=1)

x1, x2 = 6100, 6400 
y1, y2 = -1, 1     

ax_ins.set_xlim(x1, x2)
ax_ins.set_ylim(y1, y2)
ax_ins.axhline(0, color='black', linewidth=0.3)

ax_ins.tick_params(axis='both', which='both', direction='in', labelsize=8)
ax_ins.grid(True, linestyle='--', alpha=0.2)

mark_inset(ax, ax_ins, loc1=2, loc2=4, fc="none", ec="0.4", linestyle='--', linewidth=0.6)

plt.tight_layout()
plt.show()