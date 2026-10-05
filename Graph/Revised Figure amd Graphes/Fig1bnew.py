import numpy as np
import matplotlib.pyplot as plt

# تنظیمات فونت و استایل مینیمال مشابه Nature
plt.rcParams['font.family'] = 'serif'

technologies = [
    'Coal', 'H₂CCGT', 'CCGT', 'Bio', 'Hydro', 
    'Nuclear', 'Solar', 'Wind Offshore', 'Wind Onshore'
]

# داده‌ها
tyndp = [13, 103, 214, 220, 548, 576, 1357, 1441, 1577]
pypsa = [15, 110, 221, 192, 540, 580, 1216, 1386, 1560]
our_model = [17, 116, 218, 218, 534, 670, 1212, 1358, 1631]

ape_tyndp = [30, 11, 2, 0, 3, 15, 9, 5, 3]
ape_pypsa = [13, 5, 2, 13, 2, 15, 0, 2, 4]

y_pos = np.arange(len(technologies))

# ساخت یک فریم افقی فشرده با اشتراک‌گذاری محور Y
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 4), dpi=250, sharey=True)

c_tyndp = '#1f77b4'  # آبی
c_pypsa = '#1b9e77'  # سبز
c_our = '#d95f02'    # نارنجی

# --- پنل a: تولید (Generation) ---
for i in range(len(technologies)):
    ax1.plot([tyndp[i], our_model[i]], [y_pos[i], y_pos[i]], color='#e0e0e0', linewidth=1.5, zorder=1)

ax1.scatter(tyndp, y_pos, color=c_tyndp, s=45, label='TYNDP 2024', zorder=3)
ax1.scatter(pypsa, y_pos, color=c_pypsa, s=45, label='PyPSA-EUR', zorder=3)
ax1.scatter(our_model, y_pos, color=c_our, s=45, label='Our model', zorder=3)

ax1.set_xscale('log')
ax1.set_xticks([10, 100, 1000])
ax1.get_xaxis().set_major_formatter(plt.ScalarFormatter())
ax1.set_xlabel('Generation (TWh, log scale)', fontsize=9)
ax1.set_xlim(8, 3000)

ax1.grid(axis='x', linestyle='-', alpha=0.3, color='#cccccc', linewidth=0.7)
ax1.set_axisbelow(True)

# حذف کادرهای اضافی
for spine in ['top', 'right', 'left']:
    ax1.spines[spine].set_visible(False)
ax1.spines['bottom'].set_color('#cccccc')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(technologies, fontsize=9)
ax1.tick_params(left=False, bottom=True, color='#cccccc')
ax1.tick_params(axis='x', labelsize=8)  # عدد 8 را می‌توانید به اندازه دلخواه تغییر دهید

# --- پنل b: درصد اختلاف (APE) ---
for i in range(len(technologies)):
    ax2.plot([ape_tyndp[i], ape_pypsa[i]], [y_pos[i], y_pos[i]], color='#e0e0e0', linewidth=1.5, zorder=1)

ax2.scatter(ape_tyndp, y_pos, color=c_tyndp, s=45, zorder=3)
ax2.scatter(ape_pypsa, y_pos, color=c_pypsa, s=45, zorder=3)

# خطوط عمودی مرجع
ax2.axvline(x=10, color='#b2912f', linestyle='--', linewidth=0.9)
ax2.axvline(x=20, color='#d95f02', linestyle='--', linewidth=0.9)

ax2.text(10, len(technologies) - 0.35, '10%', color='#b2912f', fontweight='bold', ha='center', fontsize=8)
ax2.text(20, len(technologies) - 0.35, '20%', color='#d95f02', fontweight='bold', ha='center', fontsize=8)

ax2.set_xlabel('APE (%)', fontsize=9)
ax2.set_xlim(-2, 33)
ax2.set_xticks([0, 10, 20, 30])

ax2.grid(axis='x', linestyle='-', alpha=0.3, color='#cccccc', linewidth=0.7)
ax2.set_axisbelow(True)

for spine in ['top', 'right', 'left']:
    ax2.spines[spine].set_visible(False)
ax2.spines['bottom'].set_color('#cccccc')

ax2.tick_params(left=False, bottom=True, color='#cccccc')

ax2.tick_params(axis='x', labelsize=8)  # عدد 8 را می‌توانید به اندازه دلخواه تغییر دهید
# راهنمای رنگ‌ها به صورت مشترک در پایین شکل
fig.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c_tyndp, markersize=6, label='TYNDP 2024'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c_pypsa, markersize=6, label='PyPSA-EUR'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c_our, markersize=6, label='Our model')
], loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.08), fontsize=9)

plt.tight_layout()
plt.savefig('Combined_Generation_APE_Compact.png', dpi=300, bbox_inches='tight')
plt.show()