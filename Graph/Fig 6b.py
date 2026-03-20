import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import TwoSlopeNorm

plt.rcParams["font.family"] = "serif"


# ===============================
df = pd.read_excel("LMP.xlsx")  

# اطمینان از مرتب بودن ساعت‌ها
df["Hour"] = pd.to_numeric(df["Hour"])

# ===============================
country_order = df["Country"].drop_duplicates().tolist()
df["Country"] = pd.Categorical(df["Country"], categories=country_order, ordered=True)

# ===============================
pivot = df.pivot(index="Hour", columns="Country", values="LMP")

pivot = pivot.reindex(range(1, 25))

Z = pivot.values

hours = pivot.index.values
countries = pivot.columns.tolist()

x_idx = np.arange(len(countries))
y_idx = np.arange(len(hours))
X, Y = np.meshgrid(x_idx, y_idx)

# ===============================
vmin, vmax = np.nanmin(Z), np.nanmax(Z)

if vmin < 0 < vmax:
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
else:
    norm = plt.Normalize(vmin=vmin, vmax=vmax)

# ===============================
fig, ax = plt.subplots(figsize=(18, 7))

cf = ax.contourf(X, Y, Z, levels=1000, cmap="RdYlGn_r", norm=norm, extend="both")
cs = ax.contour(X, Y, Z, levels=12, colors="black", linewidths=0.35)
ax.clabel(cs, fmt="%1.0f", fontsize=6)

# ===============================
ax.set_xticks(x_idx)
ax.set_xticklabels(countries, rotation=90, fontsize=14)

ax.set_yticks(y_idx)
ax.set_yticklabels(hours, fontsize=14)

ax.set_ylabel("Hour", fontsize=16, fontweight="bold")
ax.set_xlabel("Country", fontsize=16, fontweight="bold")

# ===============================
cbar = fig.colorbar(cf, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label("Deviation in LMP (€/MWh)", fontsize=16, fontweight="bold")

plt.tight_layout()
plt.savefig("LMP_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()
