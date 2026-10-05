import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.colors import LinearSegmentedColormap, Normalize

plt.rcParams["font.family"] = "serif"

# ============================================================
# 1. ظرفیت کشورهای موردنظر
# ============================================================

capacity = {
    "GBR": 2064,   # UK
    "FRA": 2160,    # France
    "DEU": 789,    # Germany
    "NLD": 726,    # Netherlands
    "BEL": 231,    # Belgium
    "IRL": 1160,    # Ireland
    "LUX": 97      # Luxembourg
}


# ============================================================
# 2. دریافت نقشه واقعی Natural Earth
# ============================================================

shp_path = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_0_countries"
)

world = gpd.read_file(shp_path)


# ============================================================
# 3. انتخاب فقط 7 کشور
# ============================================================

selected = world[
    world["ADM0_A3"].isin(capacity.keys())
].copy()

selected["capacity"] = selected["ADM0_A3"].map(capacity)


# ============================================================
# 4. Colormap
#    ظرفیت کم  -> روشن
#    ظرفیت زیاد -> تیره
# ============================================================

cmap = LinearSegmentedColormap.from_list(
    "copper_scale",
    [
        "#f9d8cf",   # خیلی روشن
        "#f5b5a5",
        "#ef8d75",
        "#e85d3c",
        "#d93616"    # پررنگ
    ]
)

norm = Normalize(
    vmin=min(capacity.values()),
    vmax=max(capacity.values())
)


# ============================================================
# 5. Projection حرفه‌ای
# ============================================================

projection = ccrs.LambertConformal(
    central_longitude=4,
    central_latitude=51,
    standard_parallels=(49, 57)
)


# ============================================================
# 6. Figure
# ============================================================

fig = plt.figure(
    figsize=(5, 4),
    dpi=300
)

ax = plt.axes(projection=projection)

ax.set_facecolor("white")


# ============================================================
# 7. رسم کشورها با رنگ بر اساس ظرفیت
# ============================================================

for _, row in selected.iterrows():

    color = cmap(norm(row["capacity"]))

    temp = gpd.GeoDataFrame(
        [row],
        geometry="geometry",
        crs="EPSG:4326"
    ).to_crs(projection.proj4_init)

    temp.plot(
        ax=ax,
        facecolor=color,
        edgecolor="#A6A6A6",
        linewidth=0.01,
     
    )


# ============================================================
# 8. محدوده نقشه
# ============================================================

ax.set_extent(
    [-11.5, 15.5, 46.0, 56.5],
    crs=ccrs.PlateCarree()
)


# ============================================================
# 9. مرز کشورها
# ============================================================

selected.to_crs(
    projection.proj4_init
).boundary.plot(
    ax=ax,
    edgecolor="#A6A6A6",
    linewidth=0.1
)


# ============================================================
# 10. محل نمایش مقدار ظرفیت
# ============================================================

label_positions = {

    "IRL": (-8.0, 53.3),

    "GBR": (-2.5, 53.0),

    "NLD": (5.3, 52.2),

    "BEL": (4.4, 50.7),

    "LUX": (6.1, 49.8),

    "FRA": (2.0, 46.9),

    "DEU": (10.2, 51.0)
}


# ============================================================
# 11. نوشتن ظرفیت داخل کشور
# ============================================================

for country_code, (lon, lat) in label_positions.items():

    value = capacity[country_code]

    ax.text(
        lon,
        lat,
        f"{value:,}",
        transform=ccrs.PlateCarree(),
        fontsize=5,
        ha="center",
        va="center",
        color="#111111",
        zorder=10
    )


# ============================================================
# 12. حذف محور و قاب
# ============================================================

ax.axis("off")


# ============================================================
# 13. ذخیره خروجی
# ============================================================

plt.savefig(
    "western_europe_capacity_map.png",
    dpi=600,
    bbox_inches="tight",
    pad_inches=0.05,
    facecolor="white"
)

plt.show()

#%%
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.colors import LinearSegmentedColormap, Normalize

plt.rcParams["font.family"] = "serif"


# ============================================================
# 1. ظرفیت کشورهای موردنظر
# ============================================================

capacity = {
    "DNK": 228,   # Denmark
    "NOR": 185,   # Norway
    "SWE": 243,   # Sweden
    "FIN": 228,   # Finland
    "LVA": 104,   # Latvia
    "LTU": 65,   # Lithuania
    "EST": 104    # Estonia
}


# ============================================================
# 2. دریافت نقشه واقعی Natural Earth
# ============================================================

shp_path = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_0_countries"
)

world = gpd.read_file(shp_path)


# ============================================================
# 3. انتخاب فقط 7 کشور
# ============================================================

selected = world[
    world["ADM0_A3"].isin(capacity.keys())
].copy()

selected["capacity"] = selected["ADM0_A3"].map(capacity)


# ============================================================
# 4. Colormap آبی سرد
#    ظرفیت کم  -> آبی بسیار روشن
#    ظرفیت زیاد -> آبی پررنگ
# ============================================================

cmap = LinearSegmentedColormap.from_list(
    "cold_blue_scale",
    [
        "#E6F3FA",   # خیلی روشن
        "#C8E5F2",
        "#A6D4E9",
        "#78B9DD",
        "#4294D0",   # آبی سرد
        "#1976C5"    # پررنگ
    ]
)

norm = Normalize(
    vmin=min(capacity.values()),
    vmax=max(capacity.values())
)


# ============================================================
# 5. Projection حرفه‌ای برای شمال اروپا
# ============================================================

projection = ccrs.LambertConformal(
    central_longitude=15,
    central_latitude=57,
    standard_parallels=(50, 65)
)


# ============================================================
# 6. Figure
# ============================================================

fig = plt.figure(
    figsize=(5, 4),
    dpi=300
)

ax = plt.axes(projection=projection)

ax.set_facecolor("white")


# ============================================================
# 7. رسم کشورها با رنگ بر اساس ظرفیت
# ============================================================

for _, row in selected.iterrows():

    color = cmap(norm(row["capacity"]))

    temp = gpd.GeoDataFrame(
        [row],
        geometry="geometry",
        crs="EPSG:4326"
    ).to_crs(projection.proj4_init)

    temp.plot(
        ax=ax,
        facecolor=color,
        edgecolor="#9CCFE8",
        linewidth=0.01,
    )


# ============================================================
# 8. محدوده نقشه
# ============================================================

ax.set_extent(
    [4.0, 32.0, 54.0, 71.5],
    crs=ccrs.PlateCarree()
)


# ============================================================
# 9. مرز کشورها
# ============================================================

selected.to_crs(
    projection.proj4_init
).boundary.plot(
    ax=ax,
    color="#9CCFE8",
    linewidth=0.1
)


# ============================================================
# 10. محل نمایش مقدار ظرفیت
# ============================================================

label_positions = {

    "DNK": (9.2, 56.0),

    "NOR": (8.5, 61.5),

    "SWE": (15.0, 60.5),

    "FIN": (26.0, 63.0),

    "EST": (25.7, 58.7),

    "LVA": (24.5, 57.0),

    "LTU": (23.8, 55.4)
}


# ============================================================
# 11. نوشتن ظرفیت داخل کشور
# ============================================================

for country_code, (lon, lat) in label_positions.items():

    value = capacity[country_code]

    ax.text(
        lon,
        lat,
        f"{value:,}",
        transform=ccrs.PlateCarree(),
        fontsize=5,
        ha="center",
        va="center",
        color="#111111",
        zorder=10
    )


# ============================================================
# 12. حذف محور و قاب
# ============================================================

ax.axis("off")


# ============================================================
# 13. ذخیره خروجی
# ============================================================

plt.savefig(
    "northern_europe_capacity_map.png",
    dpi=600,
    bbox_inches="tight",
    pad_inches=0.05,
    facecolor="white"
)

plt.show()

#%%
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.colors import LinearSegmentedColormap, Normalize

plt.rcParams["font.family"] = "serif"


# ============================================================
# 1. ظرفیت کشورهای موردنظر
# ============================================================

capacity = {
    "ITA": 198,   # Italy
    "ESP": 1041,   # Spain
    "PRT": 794,   # Portugal
    "GRC": 170    # Greece
}


# ============================================================
# 2. دریافت نقشه واقعی Natural Earth
# ============================================================

shp_path = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_0_countries"
)

world = gpd.read_file(shp_path)


# ============================================================
# 3. انتخاب فقط 4 کشور
# ============================================================

selected = world[
    world["ADM0_A3"].isin(capacity.keys())
].copy()

selected["capacity"] = selected["ADM0_A3"].map(capacity)


# ============================================================
# 4. Colormap زرد
#    ظرفیت کم  -> زرد بسیار روشن
#    ظرفیت زیاد -> زرد پررنگ
# ============================================================

cmap = LinearSegmentedColormap.from_list(
    "warm_yellow_scale",
    [
        "#FFF4CC",   # خیلی روشن
        "#FCE9A3",
        "#F9DC75",
        "#F5CD4A",
        "#F2BD24",
        "#E9AD00"    # پررنگ
    ]
)

norm = Normalize(
    vmin=min(capacity.values()),
    vmax=max(capacity.values())
)


# ============================================================
# 5. Projection حرفه‌ای برای جنوب اروپا
# ============================================================

projection = ccrs.LambertConformal(
    central_longitude=15,
    central_latitude=40,
    standard_parallels=(35, 50)
)


# ============================================================
# 6. Figure
# ============================================================

fig = plt.figure(
    figsize=(5, 4),
    dpi=300
)

ax = plt.axes(projection=projection)

ax.set_facecolor("white")


# ============================================================
# 7. رسم کشورها با رنگ بر اساس ظرفیت
# ============================================================

for _, row in selected.iterrows():

    color = cmap(norm(row["capacity"]))

    temp = gpd.GeoDataFrame(
        [row],
        geometry="geometry",
        crs="EPSG:4326"
    ).to_crs(projection.proj4_init)

    temp.plot(
        ax=ax,
        facecolor=color,
        edgecolor="#E8D99A",
        linewidth=0.01,
    )


# ============================================================
# 8. محدوده نقشه
# ============================================================

ax.set_extent(
    [-10.5, 26.5, 34.0, 46.5],
    crs=ccrs.PlateCarree()
)


# ============================================================
# 9. مرز کشورها
# ============================================================

selected.to_crs(
    projection.proj4_init
).boundary.plot(
    ax=ax,
    color="#E8D99A",
    linewidth=0.1
)


# ============================================================
# 10. محل نمایش مقدار ظرفیت
# ============================================================

label_positions = {

    "PRT": (-8.0, 39.5),

    "ESP": (-3.0, 40.0),

    "ITA": (12.5, 42.0),

    "GRC": (22.0, 39.0)
}


# ============================================================
# 11. نوشتن ظرفیت داخل کشور
# ============================================================

for country_code, (lon, lat) in label_positions.items():

    value = capacity[country_code]

    ax.text(
        lon,
        lat,
        f"{value:,}",
        transform=ccrs.PlateCarree(),
        fontsize=5,
        ha="center",
        va="center",
        color="#111111",
        zorder=10
    )


# ============================================================
# 12. حذف محور و قاب
# ============================================================

ax.axis("off")


# ============================================================
# 13. ذخیره خروجی
# ============================================================

plt.savefig(
    "southern_europe_capacity_map.png",
    dpi=600,
    bbox_inches="tight",
    pad_inches=0.05,
    facecolor="white"
)

plt.show()
#%%
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from matplotlib.colors import LinearSegmentedColormap, Normalize

plt.rcParams["font.family"] = "serif"


# ============================================================
# 1. ظرفیت کشورهای موردنظر
# ============================================================

capacity = {
    "AUT": 376,   # Austria
    "POL": 732,   # Poland
    "BGR": 38,   # Bulgaria
    "CZE": 46,   # Czechia
    "HUN": 22,   # Hungary
    "ROU": 36,   # Romania
    "CHE": 134,   # Switzerland
    "SVK": 22,   # Slovakia
    "SVN": 64,   # Slovenia
    "HRV": 16    # Croatia
}


# ============================================================
# 2. دریافت نقشه واقعی Natural Earth
# ============================================================

shp_path = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_0_countries"
)

world = gpd.read_file(shp_path)


# ============================================================
# 3. انتخاب فقط 10 کشور
# ============================================================

selected = world[
    world["ADM0_A3"].isin(capacity.keys())
].copy()

selected["capacity"] = selected["ADM0_A3"].map(capacity)


# ============================================================
# 4. Colormap سبز
#    ظرفیت کم  -> سبز بسیار روشن
#    ظرفیت زیاد -> سبز پررنگ
# ============================================================

cmap = LinearSegmentedColormap.from_list(
    "green_scale",
    [
        "#E5F5E0",   # خیلی روشن
        "#C7E9C0",
        "#A1D99B",
        "#74C476",
        "#41AB5D",
        "#238B45"    # پررنگ
    ]
)

norm = Normalize(
    vmin=min(capacity.values()),
    vmax=max(capacity.values())
)


# ============================================================
# 5. Projection حرفه‌ای برای اروپای مرکزی و شرقی
# ============================================================

projection = ccrs.LambertConformal(
    central_longitude=18,
    central_latitude=48,
    standard_parallels=(45, 55)
)


# ============================================================
# 6. Figure
# ============================================================

fig = plt.figure(
    figsize=(5, 4),
    dpi=300
)

ax = plt.axes(projection=projection)

ax.set_facecolor("white")


# ============================================================
# 7. رسم کشورها با رنگ بر اساس ظرفیت
# ============================================================

for _, row in selected.iterrows():

    color = cmap(norm(row["capacity"]))

    temp = gpd.GeoDataFrame(
        [row],
        geometry="geometry",
        crs="EPSG:4326"
    ).to_crs(projection.proj4_init)

    temp.plot(
        ax=ax,
        facecolor=color,
        edgecolor="#A8D5A2",
        linewidth=0.01,
    )


# ============================================================
# 8. محدوده نقشه
# ============================================================

ax.set_extent(
    [7.0, 30.5, 43.5, 55.5],
    crs=ccrs.PlateCarree()
)


# ============================================================
# 9. مرز کشورها
# ============================================================

selected.to_crs(
    projection.proj4_init
).boundary.plot(
    ax=ax,
    color="#A8D5A2",
    linewidth=0.1
)


# ============================================================
# 10. محل نمایش مقدار ظرفیت
# ============================================================

label_positions = {

    "CHE": (8.2, 46.8),

    "AUT": (14.0, 47.6),

    "CZE": (15.5, 49.8),

    "POL": (19.0, 52.0),

    "SVK": (19.5, 48.7),

    "HUN": (19.2, 47.1),

    "SVN": (14.9, 46.1),

    "HRV": (16.5, 45.4),

    "ROU": (25.0, 45.8),

    "BGR": (25.0, 42.8)
}


# ============================================================
# 11. نوشتن ظرفیت داخل کشور
# ============================================================

for country_code, (lon, lat) in label_positions.items():

    value = capacity[country_code]

    ax.text(
        lon,
        lat,
        f"{value:,}",
        transform=ccrs.PlateCarree(),
        fontsize=5,
        ha="center",
        va="center",
        color="#111111",
        zorder=10
    )


# ============================================================
# 12. حذف محور و قاب
# ============================================================

ax.axis("off")


# ============================================================
# 13. ذخیره خروجی
# ============================================================

plt.savefig(
    "central_eastern_europe_capacity_map.png",
    dpi=600,
    bbox_inches="tight",
    pad_inches=0.05,
    facecolor="white"
)

plt.show()