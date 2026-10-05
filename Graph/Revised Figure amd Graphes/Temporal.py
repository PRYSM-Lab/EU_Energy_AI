import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import TwoSlopeNorm, Normalize, LinearSegmentedColormap

plt.rcParams["font.family"] = "serif"

# ===============================
# Read & prepare data
df_raw = pd.read_excel('Temporal.xlsx', header=[0, 1, 2], index_col=0)

# حذف سطح اضافی هدر
df_raw.columns = df_raw.columns.droplevel(2)

# Unpivot کردن داده‌ها
df = df_raw.stack(level=[0, 1]).reset_index()
df.columns = ['Hour', 'Scenario', 'Metric', 'Value']

# حذف ردیف‌های خالی و گرد کردن مقادیر
df = df.dropna(subset=['Value', 'Hour'])
df['Value'] = pd.to_numeric(df['Value']).round(2)

# اصلاح نام معیارها
df['Metric'] = df['Metric'].astype(str).str.strip()

# مرتب‌سازی سناریوها
scenario_order = sorted(df['Scenario'].unique(), key=lambda x: float(x))
df['Scenario'] = pd.Categorical(df['Scenario'], categories=scenario_order, ordered=True)

Hours = sorted(df['Hour'].unique())
metrics = df['Metric'].unique()

# عنوان اختصاصی Colorbar به ترتیب برای هر معیار
cbar_titles = [
    'GW change',
    'Mton CO2eq change',
    'TWh change',
    'GW change'
]

# mapping
scenario_idx = np.arange(len(scenario_order))
Hour_idx = np.arange(len(Hours))
scenario_map = {s: i for i, s in enumerate(scenario_order)}
Hour_map = {y: i for i, y in enumerate(Hours)}

# ===============================
# پالت منفی (استفاده از طیف آبی به جای سبز)
cmap_all_negative = LinearSegmentedColormap.from_list(
    'all_neg', ['#c6dbef', '#4292c6', '#08306b'], N=256
)

# پالت مثبت (استفاده از طیف نارنجی به جای قرمز)
cmap_all_positive = LinearSegmentedColormap.from_list(
    'all_pos', ['#fdd0a2', '#fd8d3c', '#d94801'], N=256
)

# پالت واگرا (ترکیب آبی و نارنجی مناسب برای مقادیر مثبت و منفی همزمان)
cmap_diverging = LinearSegmentedColormap.from_list(
    'div', ['#0570b0', '#67a9cf', '#fdd0a2', '#d94801'], N=256
)
# ===============================
# Plot
fig, axes = plt.subplots(1, len(metrics), figsize=(4 * len(metrics), 4.5), sharex=False, sharey=False)
if len(metrics) == 1:
    axes = [axes]

for i, metric in enumerate(metrics):
    ax = axes[i]
    metric_data = df[df['Metric'] == metric]

    if metric_data.empty:
        continue

    m_min = metric_data['Value'].min()
    m_max = metric_data['Value'].max()

    if pd.isna(m_min) or pd.isna(m_max):
        continue
    if m_min == m_max:
        m_min -= 0.01
        m_max += 0.01

    if m_max <= 0:
        current_cmap = cmap_all_negative.reversed()
        norm = Normalize(vmin=m_min, vmax=m_max)
    elif m_min >= 0:
        current_cmap = cmap_all_positive
        norm = Normalize(vmin=m_min, vmax=m_max)
    else:
        current_cmap = cmap_diverging
        norm = TwoSlopeNorm(vmin=m_min, vcenter=0, vmax=m_max)

    levels = np.linspace(m_min, m_max, 200)

    Z = np.full((len(Hours), len(scenario_order)), np.nan)

    for _, row in metric_data.iterrows():
        if row['Hour'] in Hour_map and row['Scenario'] in scenario_map:
            y_idx = Hour_map[row['Hour']]
            x_idx = scenario_map[row['Scenario']]
            Z[y_idx, x_idx] = row['Value']

    X, Y = np.meshgrid(scenario_idx, Hour_idx)

    cf = ax.contourf(
        X, Y, Z,
        levels=levels,
        cmap=current_cmap,
        norm=norm,
        extend='both'
    )

    # Contour lines
    if not np.all(np.isnan(Z)):
        cs = ax.contour(X, Y, Z, levels=5, colors='black', linewidths=0.3)
        ax.clabel(cs, inline=False, fmt='%.1f', fontsize=8)

    # Axes styling
    ax.set_xticks(scenario_idx)
    ax.set_xticklabels(scenario_order, fontsize=8)

    ax.set_yticks(Hour_idx)
    ax.set_yticklabels(Hours, fontsize=10)

    ax.set_title(str(metric), fontsize=12, fontweight='bold')
    ax.set_xlabel('Flexibility Level (%)', fontsize=10)

    # Colorbar اختصاصی
    cbar = fig.colorbar(cf, ax=ax, orientation='vertical', pad=0.04, fraction=0.046)
    
    cbar_label = cbar_titles[i] if i < len(cbar_titles) else ''
    cbar.set_label(cbar_label, fontsize=10, labelpad=8)
    
    cbar.ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
    cbar.ax.tick_params(labelsize=8)

axes[0].set_ylabel('Shifting Horizon (H)', fontsize=12)
axes[1].set_ylabel('Shifting Horizon (H)', fontsize=12)
axes[2].set_ylabel('Shifting Horizon (H)', fontsize=12)
axes[3].set_ylabel('Shifting Horizon (H)', fontsize=12)

plt.tight_layout()

# Save & Show
fig.savefig('metrics_heatmap_results.png', dpi=400, bbox_inches='tight')
plt.show()