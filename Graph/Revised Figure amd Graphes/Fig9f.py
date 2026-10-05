import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.6

regions = ['FLAP-D+', 'Nordic+Baltic', 'Southern', 'CEE', 'Balkan']
cap_without = [22.7, 2, 11, 14.2, 0]
share_without = [4.1, 1, 5, 5, 0]
cap_with = [21.8, 3.2, 15.7, 9, 2]
share_with = [3, 2, 6, 4.2, 7]

x = np.arange(len(regions))
width = 0.28

fig, ax1 = plt.subplots(figsize=(6, 1.9), dpi=300)

rects1 = ax1.bar(x - width/2, cap_without, width, label='Without Flex Cap.', color='#1f4e78', edgecolor='none')
rects2 = ax1.bar(x + width/2, cap_with, width, label='With Flex Cap.', color='#f2af00', edgecolor='none')

ax1.set_ylabel('DC install capacity (GW)', fontsize=6, color='#222222')
ax1.set_ylim(0, 26)
ax1.tick_params(axis='y', labelsize=5)
ax1.set_xticks(x)
ax1.set_xticklabels(regions, fontsize=6)
ax1.grid(axis='y', linestyle='--', alpha=0.2, zorder=0)

ax2 = ax1.twinx()

marker1 = ax2.scatter(x - width/2, share_without, color='#d9381e', marker='^', s=35, 
                      zorder=5, label='Without Flex Share')
marker2 = ax2.scatter(x + width/2, share_with, color='black', marker='X', s=35, 
                      zorder=5, label='With Flex Share')

ax2.set_ylabel('DC share of total demand (%)', fontsize=6, color='#222222')
ax2.set_ylim(0, 8)
ax2.tick_params(axis='y', labelsize=5)

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
all_handles = handles1 + handles2
all_labels = labels1 + labels2

ax1.legend(all_handles, all_labels, loc='lower center', bbox_to_anchor=(0.5, 1.05), 
           ncol=4, frameon=False, fontsize=5, handletextpad=0.3, columnspacing=1.0)

plt.tight_layout()
plt.savefig('nature_panel_final.pdf', format='pdf', bbox_inches='tight')
plt.show()