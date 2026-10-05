import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family'       : 'serif',
    'font.size'         : 8,
    'axes.titlesize'    : 8,
    'axes.labelsize'    : 7,
    'xtick.labelsize'   : 6.0,
    'ytick.labelsize'   : 6.0,
    'legend.fontsize'   : 6.0,
    'axes.linewidth'    : 0.6,
    'axes.edgecolor' : 'black',
'xtick.color'    : 'black',
'ytick.color'    : 'black',
'text.color'     : 'black',
   
    'xtick.major.width' : 0.1,  'ytick.major.width'  : 0.1,
    'xtick.minor.width' : 0.4,  'ytick.minor.width'  : 0.4,
    'xtick.major.size'  : 3,  'ytick.major.size'   : 1,
    'xtick.minor.size'  : 3,  'ytick.minor.size'   : 1,
    'xtick.direction'   : 'out','ytick.direction'    : 'out',
    'axes.spines.top'   : False,'axes.spines.right'  : False,
    'pdf.fonttype'      : 42,   'ps.fonttype'        : 42,
    'lines.linewidth'   : 1.0,
    'figure.facecolor'  : 'white',
    'axes.facecolor'    : 'white',
})

filepath = 'sample_residual_load.xlsx'
df = pd.read_excel(filepath)
df.columns = [str(col) for col in df.columns]

ldcs = {}
for col in ['365', '52', '17', '12']:
    vals = df[col].dropna().values
    ldcs[int(col)] = np.sort(vals)[::-1] / 1e6  

N_GRID = len(ldcs[365])
x_hours = np.arange(1, N_GRID + 1)
ref = ldcs[365]

manual_mapes = {12: 7, 17: 7.8, 52: 8.1}
manual_peaks = {12: 6, 17: 3, 52: 1.5}

NDAYS = [12, 17, 52, 365]

PALETTE = {12: '#C0392B', 17: '#bf3eff', 52: '#2980B9', 365: '#1A252C'}
LSTYLE  = {12: (0, (3, 1.2, 1, 1.2)), 17: (0, (4, 1.8)), 52: (0, (2, 1, 1, 1, 1, 1)), 365: '-'}
LWIDTH  = {12: 0.6, 17: 0.6, 52: 0.6, 365: 0.8}
ALPHA   = {12: 0.8, 17: 0.8, 52: 0.8, 365: 1}
LABEL   = {12: '12 rep. days', 17: '17 rep. days', 52: '52 rep. days', 365: '365 days (ref.)'}

fig = plt.figure(figsize=(3.1, 2.5), dpi=300)
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.32], wspace=0.38, left=0.12, right=0.96, top=0.90, bottom=0.15)

ax_main = fig.add_subplot(gs[0])
ax_bar = fig.add_subplot(gs[1])

lo = np.where(ref >= 0, ref * 0.90, ref * 1.10)
hi = np.where(ref >= 0, ref * 1.10, ref * 0.90)

ax_main.fill_between(x_hours, lo, hi, color='#1A252C', alpha=0.09, lw=0, label='±10% ref. band', zorder=1)
ax_main.axhline(0, color='#7F8C8D', lw=0.1, ls='-', zorder=1)

neg_idx = int(np.clip(np.searchsorted(-ref, 0, side='right'), 1, N_GRID - 1))
neg_h = neg_idx + 1
#ax_main.axvspan(neg_h, N_GRID, alpha=0.04, color='#2980B9', zorder=1, lw=0)
#ax_main.axvline(neg_h, color='#BDC3C7', lw=0.5, ls='--', zorder=2)

for d in [12, 17, 52, 365]:
    ax_main.plot(x_hours, ldcs[d], color=PALETTE[d], lw=LWIDTH[d], ls=LSTYLE[d], alpha=ALPHA[d], label=LABEL[d], zorder=4)

for d in NDAYS:
    ax_main.scatter([1], [ldcs[d][0]], s=7, color=PALETTE[d], zorder=6, clip_on=False)

ax_main.set_xlim(0, 8800)
ax_main.set_xlabel('Hour')
ax_main.set_ylabel('Residual load (TWh)')
ax_main.xaxis.set_major_locator(mticker.MultipleLocator(2000))
ax_main.xaxis.set_minor_locator(mticker.MultipleLocator(1000))
ax_main.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=True))
ax_main.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

leg = ax_main.legend(loc='upper right', frameon=False, edgecolor='#D5D8DC', fancybox=False, handlelength=1.6, labelspacing=0.25)
leg.get_frame().set_linewidth(0.4)

ax_ins = ax_main.inset_axes([0.39, 0.09, 0.3, 0.3])
for d in [12, 17, 52, 365]:
    ax_ins.plot(x_hours, ldcs[d], color=PALETTE[d], lw=LWIDTH[d] * 0.8, ls=LSTYLE[d], alpha=ALPHA[d], zorder=3)
ax_ins.fill_between(x_hours, lo, hi, color='#1A252C', alpha=0.08, lw=0)
ax_ins.axhline(0, color='#7F8C8D', lw=0.4, ls=':')

ax_ins.set_xlim(8000, 8450)

zoom_mask = (x_hours >= 8000) & (x_hours <= 8350)
y_max_in_zoom = max(ldcs[d][zoom_mask].max() for d in NDAYS)
y_min_in_zoom = min(ldcs[d][zoom_mask].min() for d in NDAYS)

ax_ins.set_ylim(
    y_min_in_zoom - abs(y_min_in_zoom) * 0.15, 
    y_max_in_zoom + abs(y_max_in_zoom) * 0.15
)

ax_ins.tick_params(labelsize=4, pad=1, length=1.5, width=0.4)
ax_ins.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=True))
ax_ins.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

ax_ins.patch.set_facecolor('white')
ax_ins.patch.set_alpha(0.85)
for sp in ax_ins.spines.values():
    sp.set_linewidth(0.4)
    sp.set_color('#BDC3C7')

ax_main.indicate_inset_zoom(ax_ins, edgecolor='#95A5A6', lw=0.4, alpha=0.6)
comp = [52, 17, 12]
yb = np.arange(len(comp))
bh = 0.4

mapes = [manual_mapes[d] for d in comp]
perrs = [manual_peaks[d] for d in comp]

bars = ax_bar.barh(yb, mapes, bh, color=['#2980B9','#bf3eff','#C0392B'], alpha=0.85, zorder=3)
ax_bar.scatter(
    perrs, yb,
    marker='D',
    s=10,
    color='white',
    edgecolors=[PALETTE[d] for d in comp],
    linewidths=0.5,
    zorder=5,
    label='|Peak dev.| (%)'
)


ax_bar.axvline(10, color='#8B0000', lw=0.6, ls='--', zorder=4)
ax_bar.text(5.2, len(comp) - 0.55, '10% thresh.', color='#8B0000', fontsize=4.0, va='top', ha='left')

for bar_o, val in zip(bars, mapes):
    w = bar_o.get_width()
    ax_bar.text(w + 0.8, bar_o.get_y() + bar_o.get_height() / 2., f'{val:.1f}%', va='center', ha='left', fontsize=6, color='#2C3E50')

ax_bar.set_yticks(yb)
ax_bar.set_yticklabels(['12 days', '17 days', '52 days'], fontsize=6)
ax_bar.set_xlabel('MAPE (%)', labelpad=2, fontsize=6)
ax_bar.set_title('LDC accuracy vs 365 day', fontsize=6, pad=12 )
ax_bar.set_xlim(0, max(mapes) * 1.35)
ax_bar.set_ylim(-0.5, len(comp) - 0.3)
ax_bar.xaxis.set_major_locator(mticker.MaxNLocator(3))
ax_bar.tick_params(axis='both', labelsize=5)
ax_bar.legend(loc='lower right', frameon=False, fontsize=5.0, bbox_to_anchor=(1.1, 0.99))

# 5. ذخیره خروجی
plt.savefig('final_twh_ldc.png', dpi=300, bbox_inches='tight')
plt.savefig('final_twh_ldc.pdf', dpi=300, bbox_inches='tight')
plt.show()