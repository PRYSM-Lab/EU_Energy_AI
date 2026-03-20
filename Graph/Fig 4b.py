
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from shapely.geometry import MultiPolygon
import matplotlib as mpl
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap
plt.rcParams['font.family'] = 'Serif'

# Load world and filter Europe countries
world = gpd.read_file("ne_110m_admin_0_countries.shp")
europe = world[(world['CONTINENT'] == 'Europe') & (~world['ISO_A2'].isin(['RU', 'IS']))].copy()
europe.loc[europe['NAME'] == 'France', 'ISO_A2'] = 'FR'
europe.loc[europe['NAME'] == 'Montenegro', 'ISO_A2'] = 'ME'
europe.loc[europe['NAME'] == 'Norway', 'ISO_A2'] = 'NO'
europe.loc[europe['ISO_A2'] == '-99', 'ISO_A2'] = None
europe = europe[~europe['ISO_A2'].isna()]

# Bounding box
spain_ymin = world.loc[world['NAME'] == 'Spain', 'geometry'].total_bounds[1]
ireland_xmin = world.loc[world['NAME'] == 'Ireland', 'geometry'].total_bounds[0]
finland_ymax = world.loc[world['NAME'] == 'Finland', 'geometry'].total_bounds[3]
romania_xmax = world.loc[world['NAME'] == 'Romania', 'geometry'].total_bounds[2]

# Simplify multipolygons
europe['geometry'] = europe['geometry'].apply(lambda g: max(g.geoms, key=lambda a: a.area) if isinstance(g, MultiPolygon) else g)
europe['centroid'] = europe['geometry'].apply(lambda g: g.representative_point())

# Data
installed_capacity = {
 'AL': 0, 'AT': 16, 'BA': 0, 'BE': 0, 'BG': 4, 'CH': 5, 'CZ': 2, 'DE': 24,
 'DK': 6, 'EE': 0, 'ES': 106, 'FI': -6, 'FR': 83, 'GR': 14, 'HR': 2, 'HU': 3,
 'IE': 29, 'IT': 5, 'LT': 4, 'LU': 1, 'LV': -3, 'ME': 0, 'MK': 0, 'NL': 5,
 'NO': 6, 'PL': 57, 'PT': 30, 'RO': -3, 'RS': 2, 'SE': -26, 'SI': 3, 'SK': 3,
 'GB': 58
}

connection_values = {
    ('AL', 'GR'): 0.4,
    ('ME', 'AL'): 0.1,
    ('AL', 'MK'): 0.0,
    ('RS', 'AL'): 0.1,
    ('AT', 'CH'): 0.8,
    ('CZ', 'AT'): 1.3,
    ('AT', 'DE'): 2.3,
    ('HU', 'AT'): 0.5,
    ('AT', 'IT'): 0.1,
    ('SI', 'AT'): 2.7,
    ('HR', 'BA'): 0.0,
    ('BA', 'ME'): 0.2,
    ('BA', 'RS'): 0.1,
    ('BE', 'DE'): 1.7,
    ('BE', 'DK'): 0.6,
    ('FR', 'BE'): 4.1,
    ('BE', 'LU'): 0.9,
    ('NL', 'BE'): 4.0,
    ('BE', 'GB'): 3.2,
    ('GR', 'BG'): 0.1,
    ('MK', 'BG'): 0.1,
    ('BG', 'RO'): 2.9,
    ('RS', 'BG'): 0.1,
    ('CH', 'DE'): 1.3,
    ('FR', 'CH'): 0.4,
    ('CH', 'IT'): 0.3,
    ('CZ', 'DE'): 3.4,
    ('CZ', 'PL'): 1.3,
    ('SK', 'CZ'): 3.3,
    ('DK', 'DE'): 11.1,
    ('EE', 'DE'): 0.6,
    ('FR', 'DE'): 5.8,
    ('LU', 'DE'): 2.1,
    ('DE', 'NL'): 1.3,
    ('DE', 'NO'): 3.0,
    ('DE', 'PL'): 0.1,
    ('DE', 'SE'): 2.0,
    ('GB', 'DE'): 2.7,
    ('DK', 'NL'): 0.1,
    ('NO', 'DK'): 0.2,
    ('SE', 'DK'): 0.7,
    ('DK', 'GB'): 0.3,
    ('FI', 'EE'): 0.3,
    ('LV', 'EE'): 1.8,
    ('FR', 'ES'): 12.3,
    ('ES', 'PT'): 10.8,
    ('NO', 'FI'): 0.2,
    ('SE', 'FI'): 0.7,
    ('IE', 'FR'): 0.1,
    ('IT', 'FR'): 1.3,
    ('FR', 'GB'): 0.8,
    ('IT', 'GR'): 0.3,
    ('MK', 'GR'): 1.3,
    ('GR', 'SI'): 0.4,
    ('HR', 'HU'): 0.5,
    ('HR', 'RS'): 0.1,
    ('RS', 'SI'): 0.7,
    ('HU', 'RO'): 1.5,
    ('RS', 'HU'): 0.1,
    ('HU', 'SI'): 0.1,
    ('HU', 'SK'): 1.4,
    ('IE', 'GB'): 0.6,
    ('ME', 'IT'): 0.4,
    ('SI', 'IT'): 0.2,
    ('LT', 'LV'): 3.4,
    ('PL', 'LT'): 0.0,
    ('LT', 'SE'): 0.2,
    ('LV', 'SE'): 0.6,
    ('RS', 'ME'): 0.2,
    ('RS', 'MK'): 0.7,
    ('NL', 'NO'): 0.8,
    ('NL', 'GB'): 2.0,
    ('NO', 'SE'): 0.5,
    ('NO', 'GB'): 0.0,
    ('PL', 'SE'): 0.1,
    ('SK', 'PL'): 0.9,
    ('RS', 'RO'): 0.9
}

# Colormaps (custom)

# Red colormap with high contrast (light pink to deep red)
import seaborn as sns
cap_cmap = sns.color_palette("vlag_r", as_cmap=True)
# Blue colormap with high contrast (light blue to navy blue)
conn_cmap = LinearSegmentedColormap.from_list("custom_red", ["#FFC1B0", "#CC0000"]) 
# Normalize
cap_vals = list(installed_capacity.values())

vmin = np.min(cap_vals)   # واقعی‌ترین مقدار منفی
vmax = np.max(cap_vals)   # واقعی‌ترین مقدار مثبت

cap_norm = mpl.colors.TwoSlopeNorm(
    vmin=vmin,
    vcenter=0,
    vmax=vmax
)
conn_vals = list(connection_values.values())
conn_norm = mpl.colors.Normalize(vmin=0, vmax=max(conn_vals))

europe['capacity'] = europe['ISO_A2'].map(installed_capacity)
europe['color'] = europe['capacity'].map(lambda x: cap_cmap(cap_norm(x)) if pd.notna(x) else '#dddddd')

# Plot
fig, ax = plt.subplots(figsize=(20, 12))
europe.plot(ax=ax, color=europe['color'], edgecolor='black', linewidth=0.7)


# --- Connection classes (minimal change) ---
conn_bins = [
    (0, 0.2),
    (0.2, 1),
    (1.3, 3.5),
    (3.5, 7),
    (7, 10),
    (10, 12),
    (12, np.inf),
]

conn_widths = [0.9, 1.5, 2.5, 3.7, 4.9, 6.2, 8]
conn_colors = ["#FEE5D9", "#FCAE91", "#FB6A4A", "#DE2D26", "#A50F15", "#67000D","#67000D"]
conn_labels = ["0–0.2", "0.2–1", "1.3–3.5", "3.5–7", "7-10", "10-12", ">12"]



# Country labels
for idx, row in europe.iterrows():
    ax.text(row['centroid'].x, row['centroid'].y, row['ISO_A2'], ha='center', va='center', fontsize=12)

#min_w, max_w = 0.5, 4.0
node_offset = 0.1

for (src, dst), val in connection_values.items():
    if src not in installed_capacity or dst not in installed_capacity:
        continue
    try:
        p1 = europe.loc[europe['ISO_A2'] == src, 'centroid'].values[0]
        p2 = europe.loc[europe['ISO_A2'] == dst, 'centroid'].values[0]
    except IndexError:
        continue

    dx, dy = p2.x - p1.x, p2.y - p1.y
    length = np.hypot(dx, dy)
    if length == 0:
        continue
    ux, uy = dx / length, dy / length

    start = (p1.x + ux * node_offset, p1.y + uy * node_offset)
    end = (p2.x - ux * node_offset, p2.y - uy * node_offset)

    for i, (vmin, vmax) in enumerate(conn_bins):
        if vmin <= val < vmax:
            line_width = conn_widths[i]
            color = conn_colors[i]
            break
    else:
        line_width = conn_widths[-1]
        color = conn_colors[-1]

    ax.plot([start[0], end[0]], [start[1], end[1]],
            color=color, linewidth=line_width, alpha=0.7)

    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    arrow_length = 0.3
    arrow_length = 0.2 + line_width * 0.2  
    head_length = 2 + line_width * 1.5       
    head_width = 2 + line_width * 1.5 
    

    arrow = FancyArrowPatch(
        posA=(mid_x - ux * arrow_length / 2, mid_y - uy * arrow_length / 2),
        posB=(mid_x + ux * arrow_length / 2, mid_y + uy * arrow_length / 2),
        arrowstyle=f'-|>,head_length={head_length},head_width={head_width}',
        mutation_scale=1,
        color=color,
        linewidth=line_width * 0.09,
        alpha=0.9
    )
    ax.add_patch(arrow)


# Set map limits
#ax.set_xlim(ireland_xmin - 1, romania_xmax + 1)
#ax.set_ylim(spain_ymin - 1, finland_ymax + 1)
ax.axis("off")
from matplotlib.ticker import MaxNLocator

# Colorbars
divider = make_axes_locatable(ax)
cax1 = divider.append_axes("right", size="3%", pad=0.01)




#cax2 = divider.append_axes("left", size="3%", pad=0.01)
sm1 = mpl.cm.ScalarMappable(norm=cap_norm, cmap=cap_cmap)
sm1.set_array([])
cbar1 = plt.colorbar(sm1, cax=cax1)
cbar1.set_label("Deviation in Energy Production (TWh)", fontsize=16,fontweight='bold')

#sm2 = mpl.cm.ScalarMappable(norm=conn_norm, cmap=conn_cmap)
#sm2.set_array([])
#cbar2 = plt.colorbar(sm2, cax=cax2)
#cbar2.set_label("Net Energy Flow (TWh)", fontsize=16, fontweight='bold')
#cbar2.ax.yaxis.set_label_position("left")
#cbar2.ax.yaxis.set_ticks_position("left")
from matplotlib.lines import Line2D

legend_lines = [
    Line2D([0], [0], color=conn_colors[i], lw=conn_widths[i])
    for i in range(len(conn_bins))
]

ax.legend(
    legend_lines,
    [f"{lbl} TWh" for lbl in conn_labels],
    title="Net Energy Flow",
    loc="upper left",
    frameon=False,
    fontsize=13,
    title_fontsize=15
)

# Title and layout
#ax.set_title(" Energy Production & Exchange - Base Case", fontsize=14, fontweight='bold')
plt.subplots_adjust(left=0.01, right=0.98, top=0.98, bottom=0.02)
plt.show()