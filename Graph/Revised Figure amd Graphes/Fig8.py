import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

plt.rcParams["font.family"] = "serif"

pue_axis = np.array([1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4]) 
years_axis = np.array([2030, 2035, 2040, 2045, 2050]) 

data_matrices = {
    ('UK', 'Cost'): np.array([
        [4.5, 3, 1, 0, -2, -5, -7.5], 
        [5, 3, 2, 0, -2, -4, -7.5], 
        [4, 3, 3, 0, -3.0, -5, -6],
        [5, 3, 3, 0, -3.0, -5, -5], 
        [6, 3, 3, 0, -4.2, -7.0, -7.0] 
    ]),
    ('UK', 'Emission'): np.array([
        [5, 3, 0.5, 0, -0.5, -4, -6.0], 
        [4, 2, 0.5, 0, -0.75, -3, -6.0], 
        [3, 2, 1, 0, -1, -3, -6.5],
        [2, 1, 1, 0, -1, -2, -3.5],
        [1, 1, 1, 0, -1, -1, -1]    
    ]),
    ('UK', 'Peak'): np.array([
        [5.0, 6.2, 2, 0, -2, -4.0, -4.0], 
        [5.0, 5.2, 2, 0, -2, -5.0, -4.0],
        [4.5, 3.5, 3, 0, -3, -5.5, -4.5], 
        [5, 4.5, 3, 0, -3, -5.5, -4.5],
        [6.2, 5.8, 1, 0, -0.5, -6.0, -6]   
    ]),
    ('US', 'Cost'): np.array([
        [6, 4, 3, 0, -3.0, -6.0, -8.0], 
        [7, 5, 3, 0, -2.0, -6.0, -7.0],
        [6, 4,  4, 0, -4.0,-6, -7.0],  
        [6, 4.5,  4.5, 0, -4.5,-6, -7.5],
        [7, 5.0,  4, 0, -4.0, -5.0, -8.0]    
    ]),
    ('US', 'Emission'): np.array([
        [6.6, 6, 1, 0, -1.0, -5.0, -8.0],
        [7, 6, 1, 0, -1.0, -6.0, -9.0],
        [6, 6, 3, 0, -1, -5, -7.0], 
        [5, 5, 1, 0, -0.5, -4, -5.0],
        [1, 1, 1, 0, -1, -1, -1]  
    ]),
    ('US', 'Peak'): np.array([
        [7.2, 5.0, 2.7, 0, -3, -4, -5.0],
        [7.9, 6.0, 3, 0, -2, -5, -6.0],
        [6.5, 6, 3, 0, -3.5, -5.2, -7.0], 
        [6.5, 6.5, 3, 0, -3.75, -6.2, -7.5], 
        [7, 7.0, 2, 0, -4.0, -7.0, -8.2]   
    ]),
}

fig, axes = plt.subplots(3, 2, figsize=(11, 14), sharex=False, sharey=False)
metrics_labels = ['Total Cost Change (%)', 'Emission Change (%)', 'Peak Demand Change (%)']
panel_labels = [['a', 'b'], ['c', 'd'], ['e', 'f']]

X, Y = np.meshgrid(pue_axis, years_axis)

for row, metric in enumerate(['Cost', 'Emission', 'Peak']):
    for col, profile in enumerate(['UK', 'US']):
        ax = axes[row, col]
        Z = -data_matrices[(profile, metric)]
        
        norm = TwoSlopeNorm(vcenter=0, vmin=min(Z.min(), -0.1), vmax=max(Z.max(), 0.1))
        
        contour = ax.contourf(X, Y, Z, levels=50, cmap='coolwarm', norm=norm, alpha=0.9)
        
        lines = ax.contour(X, Y, Z, levels=12, colors='black', linewidths=0.5)
        ax.clabel(lines, inline=True, fontsize=8, fmt='%1.0f%%')
        
        if Z.min() < 0 < Z.max():
            ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=1.2, linestyles='--')
        
        ax.set_xticks(pue_axis)
        ax.set_yticks([2030, 2035, 2040, 2045, 2050])
        
        # برچسب a تا ف ساده بالای هر پنل
        ax.set_title(panel_labels[row][col], fontsize=12, fontweight='bold', loc='left')
        
        if col == 0: 
            ax.set_ylabel(f"{metrics_labels[row]}\nYear", fontsize=11, fontweight='bold')
        else:
            ax.set_ylabel('Year', fontsize=11, fontweight='bold')
            
        if row == 2:
            ax.set_xlabel('Efficiency Change (PUE)', fontsize=11, fontweight='bold')

    cbar = fig.colorbar(contour, ax=axes[row, :], location='right', shrink=0.8, pad=0.03)
    cbar.set_label('% Change', fontsize=10)

# ایجاد فضای خالی در سمت راست برای جلوگیری از روی هم افتادن Colorbarها
fig.subplots_adjust(right=0.75, hspace=0.3, wspace=0.33)

plt.savefig('heatmap_panels.png', dpi=300, bbox_inches='tight')
plt.show()