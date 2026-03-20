import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
from matplotlib.colors import to_rgb, to_hex
from matplotlib.lines import Line2D

def lighten_color(color, amount=0.3):
    c = np.array(to_rgb(color))
    c = c + (1 - c) * amount
    c = np.clip(c, 0, 1)
    return to_hex(c)

def get_mainland(geometry):
    if isinstance(geometry, MultiPolygon):
        largest = max(geometry.geoms, key=lambda a: a.area)
        return largest
    elif isinstance(geometry, Polygon):
        return geometry
    else:
        return geometry

def draw_pie(ax, ratios, X, Y, size=1.0, colors=None):
    start_angle = 90
    for ratio, color in zip(ratios, colors):
        if ratio <= 0:
            continue
        wedge = plt.matplotlib.patches.Wedge(center=(X, Y), r=size,
                                            theta1=start_angle,
                                            theta2=start_angle + ratio * 360,
                                            facecolor=color,
                                             linewidth=0.2,
                                             edgecolor='black')
        ax.add_patch(wedge)
        start_angle += ratio * 360

plt.rcParams["font.family"] = "serif"

world = gpd.read_file("ne_110m_admin_0_countries.shp")
europe = world[(world['CONTINENT'] == 'Europe') & (~world['ISO_A2'].isin(['RU', 'IS']))].copy()
europe.loc[europe['NAME'] == 'France', 'ISO_A2'] = 'FR'
europe.loc[europe['NAME'] == 'Montenegro', 'ISO_A2'] = 'ME'
europe.loc[europe['NAME'] == 'Norway', 'ISO_A2'] = 'NO'
europe.loc[europe['ISO_A2'] == '-99', 'ISO_A2'] = None
europe = europe[~europe['ISO_A2'].isna()]

# مرزهای نمایش
spain = world[world['NAME'] == 'Spain']
_, spain_ymin, _, _ = spain.total_bounds
ireland = world[world['NAME'] == 'Ireland']
ireland_xmin, _, _, _ = ireland.total_bounds
finland = world[world['NAME'] == 'Finland']
_, _, _, finland_ymax = finland.total_bounds



energy_colors = ['#8da44e',  # Wind Offshore
                 '#2ca02c',  # Wind Onshore
                 '#ffbf00',  # Solar
                 '#1f77b4',  # Nuclear (مثلاً بنفش)
                 '#8c564b',  # Gas
                 '#FF69B4',  # Battery
                 '#1E90FF']  # Hydro





energy_share = pd.read_excel("Energy_Data.xlsx")
energy_share['Total'] = energy_share[['Wind Offshore','Wind Onshore', 'Solar','Nuclear','Gas', 'Battery', 'Hydro']].sum(axis=1)
min_size = 0.5
max_size = 2.5
totals = energy_share['Total']
totals_norm = (totals - totals.min()) / (totals.max() - totals.min())
sizes_dict = dict(zip(energy_share['ISO_A2'], min_size + totals_norm * (max_size - min_size)))


fig, ax = plt.subplots(figsize=(14, 14))
europe.plot(ax=ax, color='#F2F2F2', edgecolor="#9E9E9E", linewidth=0.5)
ax.set_xlim(ireland_xmin, europe.total_bounds[2])
ax.set_ylim(spain_ymin, finland_ymax)

for idx, row in europe.iterrows():
    main_geom = get_mainland(row['geometry'])
    point = main_geom.representative_point()
    country_code = row['ISO_A2']

    data_row = energy_share[energy_share['ISO_A2'] == country_code]
    if not data_row.empty:
        values = data_row[['Wind Offshore','Wind Onshore', 'Solar','Nuclear','Gas', 'Battery', 'Hydro']].values.flatten().astype(float)
        total = values.sum()
        if total > 0:
            values = values / total  
            size = sizes_dict.get(country_code, 0.8) 
            draw_pie(ax, values, point.x, point.y, size=size, colors=energy_colors)

            ax.text(point.x, point.y - size - 0,
                    f"{int(data_row['Total'].values[0])} GW",
                    ha='center', va='top',
                    fontsize=10, color='black')
        else:
            ax.text(point.x, point.y, country_code, ha='center', va='center',
                    fontsize=10, fontweight='medium', color='#6c757d', alpha=0.9)
    else:
        ax.text(point.x, point.y, country_code, ha='center', va='center',
                fontsize=12, fontweight='medium', color='#6c757d', alpha=0.9)

import matplotlib.patches as mpatches

legend_elements = [
    mpatches.Patch(facecolor=energy_colors[0], edgecolor='0.4', linewidth=0.6, label='Wind Offshore'),
    mpatches.Patch(facecolor=energy_colors[1], edgecolor='0.4', linewidth=0.6, label='Wind Onshore'),
    mpatches.Patch(facecolor=energy_colors[2], edgecolor='0.4', linewidth=0.6, label='Solar'),
    mpatches.Patch(facecolor=energy_colors[3], edgecolor='0.4', linewidth=0.6, label='Nuclear'),
    mpatches.Patch(facecolor=energy_colors[4], edgecolor='0.4', linewidth=0.6, label='Gas'),
    mpatches.Patch(facecolor=energy_colors[5], edgecolor='0.4', linewidth=0.6, label='Battery'),
    mpatches.Patch(facecolor=energy_colors[6], edgecolor='0.4', linewidth=0.6, label='Hydro'),
]

ax.legend(
    handles=legend_elements,
    fontsize=14,
    frameon=False,
    borderpad=1,
    labelspacing=0.25,
    loc='upper left',
    bbox_to_anchor=(0, 1)
)


ax.axis('off')
plt.tight_layout()
plt.show()
