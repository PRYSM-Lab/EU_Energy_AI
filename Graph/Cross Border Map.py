import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# =========================
# LOAD DATA
# =========================
nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")



# -------------------------
# CLEAN DATA (Excel-safe)
# -------------------------
nodes["id"] = nodes["id"].str.strip().str.upper()
edges["from"] = edges["from"].str.strip().str.upper()
edges["to"] = edges["to"].str.strip().str.upper()
edges["capacity_mw"] = pd.to_numeric(edges["capacity_mw"], errors="coerce")

# =========================
# STYLE FUNCTION
# =========================
def capacity_style(mw):
    if mw <= 500:
        return "#FFE082", 0.2
    elif mw <= 1000:
        return "#FFCA28", 0.7
    elif mw <= 2000:
        return "#FFB300", 1
    elif mw <= 3000:
        return "#FB8C00", 1.7
    elif mw <= 4000:
        return "#F4511E", 2.2
    elif mw <= 5000:
        return "#E53935", 4.0
    elif mw <= 6000:
        return "#C62828", 5.5   # ← NEW ROW (≤ 6000 MW)
    else:
        return "#B71C1C", 8.0   # > 6000 MW


# =========================
# BASE MAP
# =========================
fig = plt.figure(figsize=(20, 15))

ax = plt.axes(
    projection=ccrs.LambertConformal(
        central_longitude=10,
        central_latitude=50
    )
)

ax.set_extent([-12, 30, 35, 72], crs=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor="#F2F2F2", zorder=0)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor="#9E9E9E", zorder=1)
ax.add_feature(cfeature.BORDERS, linewidth=0.4, edgecolor="#9E9E9E", zorder=1)

# =========================
# DRAW CONNECTIONS (CRITICAL FIX HERE)
# =========================
for _, row in edges.iterrows():
    n1 = nodes[nodes.id == row["from"]]
    n2 = nodes[nodes.id == row["to"]]

    if n1.empty or n2.empty:
        continue

    n1 = n1.iloc[0]
    n2 = n2.iloc[0]

    color, width = capacity_style(row["capacity_mw"])

    ax.plot(
        [n1.lon, n2.lon],
        [n1.lat, n2.lat],
        transform=ccrs.Geodetic(),  # ← REQUIRED FOR LINES
        color=color,
        linewidth=width,
        alpha=0.9,
        solid_capstyle="round",
        zorder=4
    )

# =========================
# DRAW NODES
# =========================
ax.scatter(
    nodes.lon,
    nodes.lat,
    s=55,
    color="#F57C00",
    edgecolor="white",
    linewidth=0.6,
    transform=ccrs.PlateCarree(),
    zorder=5
)

# =========================
# LEGEND
# =========================
legend_lines = [
    ("1 – 500 MW", "#FFE082", 0.2),
    ("501 – 1,000 MW", "#FFCA28", 0.7),
    ("1,001 – 2,000 MW", "#FFB300", 1),
    ("2,001 – 3,000 MW", "#FB8C00", 1.7),
    ("3,001 – 4,000 MW", "#F4511E", 2.2),
    ("4,001 – 5,000 MW", "#E53935", 4),
    ("4,001 – 6,000 MW", "#C62828", 5.5),
    ("> 6,000 MW", "#B71C1C", 8),
]

handles = [
    plt.Line2D([0], [0], color=c, lw=w, label=l)
    for l, c, w in legend_lines
]

ax.legend(
    handles=handles,
    title="Cross-border Capacities (MW)",
    loc="upper right",
    bbox_to_anchor=(0.18, 0.75),
    frameon=False,
    fontsize=11,
    title_fontsize=13
)

ax.set_frame_on(False)
plt.tight_layout()
plt.show()
