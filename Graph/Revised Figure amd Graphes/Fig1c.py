import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ۱. مسیر فایل اکسل خود را در این بخش قرار دهید
EXCEL_FILE_PATH = r"C:\Users\Mohammed\statics_country.xlsx"

# لیست کشورهای موردنظر شما
TARGET_COUNTRIES = ["DE", "FR", "UK", "ES", "IT", "FI", "PL", "NL"]

# تنظیمات نام تکنولوژی‌ها
TECH_STYLE = [
    "CCGT",
    "Nuclear",
    "Coal",
    "Wind_Onshore",
    "Wind_Offshore",
    "Solar",
    "Hydro",
]
TECH_DISPLAY = {
    "CCGT": "CCGT",
    "Nuclear": "Nuclear",
    "Coal": "Coal",
    "Wind_Onshore": "Wind Onshore",
    "Wind_Offshore": "Wind Offshore",
    "Solar": "Solar",
    "Hydro": "Hydro",
}


def compute_metrics(ref: np.ndarray, model: np.ndarray) -> dict:
    mask = ref != 0
    if not np.any(mask):
        return {"MAPE": 0.0}
    mape = np.mean(np.abs((ref[mask] - model[mask]) / ref[mask])) * 100
    return {"MAPE": mape}


# ۲. خواندن فایل اکسل
df = pd.read_excel(EXCEL_FILE_PATH)

# ۳. فیلتر کردن کشورهای درخواستی
df_filtered = df[df["c"].isin(TARGET_COUNTRIES)].copy()

# ۴. محاسبه MAPE برای هر کشور و تکنولوژی
records = []
for (c, j), grp in df_filtered.groupby(["c", "j"]):
    m = compute_metrics(grp["CAP_ref"].values, grp["CAP"].values)
    records.append({"country": c, "technology": j, "MAPE": m["MAPE"]})

# ۵. محاسبه مجموع کل اروپا برای هر تکنولوژی و سال، و سپس محاسبه MAPE کل اروپا
europe_grp = df_filtered.groupby(["j", "t"])[["CAP_ref", "CAP"]].sum().reset_index()
for j, grp in europe_grp.groupby("j"):
    m = compute_metrics(grp["CAP_ref"].values, grp["CAP"].values)
    records.append({"country": "Europe", "technology": j, "MAPE": m["MAPE"]})

# ۶. ساخت جدول Pivot
mape_df = pd.DataFrame(records)
pivot = mape_df.pivot(index="country", columns="technology", values="MAPE")

# مرتب‌سازی ستون‌ها
col_order = [t for t in TECH_STYLE if t in pivot.columns]
col_order += [t for t in pivot.columns if t not in col_order]
pivot = pivot[col_order]

# مرتب‌سازی ردیف‌ها و قرار دادن Europe در انتهای ردیف‌ها
countries_only = pivot.drop(index="Europe", errors="ignore")
sorted_index = countries_only.mean(axis=1).sort_values().index.tolist()
if "Europe" in pivot.index:
    sorted_index.append("Europe")
pivot = pivot.loc[sorted_index]

# ۷. رسم نمودار
fig, ax = plt.subplots(figsize=(4, 3))

cmap = matplotlib.colormaps.get_cmap("RdYlGn_r")
im = ax.imshow(
    pivot.values,
    cmap=cmap,
    vmin=0,
    vmax=30,
    aspect="0.6",
    interpolation="nearest",
)

# تنظیم محورها و برچسب‌ها
short_labels = [TECH_DISPLAY.get(t, t).replace(" ", "\n") for t in pivot.columns]
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(short_labels, fontsize=6, rotation=90, ha="center")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index, fontsize=6)
ax.tick_params(length=0)

# نمایش اعداد روی سلول‌ها
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        v = pivot.values[i, j]
        if np.isfinite(v):
            ax.text(
                j,
                i,
                f"{v:.0f}",
                ha="center",
                va="center",
                fontsize=5,
                color="white" if v > 18 else "black",
            )

# خطوط جداکننده
for i in range(len(pivot)):
    ax.axhline(i - 0.5, color="white", lw=0.3)
for j in range(len(pivot.columns)):
    ax.axvline(j - 0.5, color="white", lw=0.3)

# Colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02, shrink=0.7)
cbar.set_label("MAPE [%]", fontsize=6.5)
cbar.ax.tick_params(labelsize=6)
cbar.outline.set_linewidth(0.4)

ax.set_title("MAPE [%] — country × technology", fontsize=7, pad=4)
ax.text(
    -0.22,
    1.02,
    "(b)",
    transform=ax.transAxes,
    fontsize=9,
    fontweight="bold",
    va="top",
)

# ذخیره و نمایش
plt.tight_layout()
plt.savefig("mape_heatmap.png", bbox_inches="tight", dpi=300)
plt.show()