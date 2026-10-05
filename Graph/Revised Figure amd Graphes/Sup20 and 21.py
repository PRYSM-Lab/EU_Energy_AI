import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "serif"

data = {
    "Hour_Continuous": list(range(1, 49)),
    "52_Days": [
        0,
        0,
        8437.0698,
        8331.6065,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        4955.2923,
        8008.6665,
        7908.5581,
        5689.4939,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2453.6693,
        2422.9984,
        9600.8741,
        9480.8632,
        9362.3524,
        9245.323,
        9129.7565,
        9015.6345,
        9958.4566,
        9912.7058,
        9788.797,
        9666.437,
        3046.9488,
        2289.9413,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
    "17_Days": [
        0,
        0,
        4661.028,
        11735.929,
        13401.387,
        13233.87,
        13068.446,
        6799.0461,
        5398.1688,
        5330.6917,
        5264.058,
        5198.2573,
        5133.2791,
        5069.1131,
        5005.7492,
        4943.1773,
        4881.3876,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        8322.9325,
        14443.082,
        22237.834,
        28589.083,
        28231.72,
        23972.797,
        11910.286,
        1582.8387,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
    "12_Days": [
        0,
        2715.726,
        6539.3596,
        8562.4994,
        8455.4682,
        5572.7476,
        2954.9139,
        0,
        0,
        1725.904,
        7211.5893,
        8566.2034,
        9791.3849,
        8381.4926,
        7537.5776,
        7712.9388,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2715.726,
        6539.3596,
        8562.4994,
        8455.4682,
        5572.7476,
        2954.9139,
        0,
        0,
        1725.904,
        12211.589,
        22566.203,
        32791.385,
        32381.493,
        22537.578,
        7712.9388,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(10, 6))

colors = ["#2ca02c", "#ff7f0e","#1f77b4" ]
columns = ["52_Days", "17_Days", "12_Days"]
labels = ["52 Days", "17 Days", "12 Days"]

for col, color, label in zip(columns, colors, labels):
    ax.plot(
        df["Hour_Continuous"],
        df[col],
        marker="o",
        linewidth=2,
        label=label,
        color=color,
    )

ax.axvline(
    x=24.5, color="black", linestyle="--", alpha=0.5, label="Day Boundary"
)


ax.set_xlabel("Hour", fontsize=14,fontweight='bold')
ax.set_ylabel("Storage level (MWh)", fontsize=14,fontweight='bold')

ax.tick_params(axis="x", colors="black", labelcolor="black")
ax.tick_params(axis="y", colors="black", labelcolor="black")
for spine in ax.spines.values():
    spine.set_color("black")

ax.legend()
plt.tight_layout()
plt.show()

#%%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "serif"

data = {
    "Hour": list(range(1, 25)),
    "12_Days": [
        1124.652,
        1714.8188,
        120.08144,
        0,
        1029.0932,
        5739.064,
        8890.8137,
        9913.2997,
        9405.6935,
        10193.347,
        10427.763,
        10608.257,
        9765.5934,
        9019.7895,
        9948.5042,
        9649.5903,
        9831.1404,
        10356.209,
        8294.1527,
        5852.6259,
        2477.6273,
        39.739609,
        0,
        0,
    ],
    "17_Days": [
        0,
        0,
        0,
        0,
        0,
        5513.1146,
        9364.9926,
        13840.921,
        13307.679,
        8022.3151,
        8172.3614,
        8363.5358,
        7635.3931,
        8478.2608,
        10232.288,
        12028.738,
        12781.957,
        12152.967,
        9980.7168,
        7214.6506,
        4043.1706,
        0,
        0,
        0,
    ],
    "52_Days": [
        0,
        0,
        1315.7501,
        2293.0676,
        7136.3371,
        8616.5067,
        9550.5939,
        9220.4393,
        10739.774,
        12953.789,
        12751.584,
        12224.87,
        12864.105,
        12926.355,
        11474.211,
        10793.806,
        10292.539,
        10525.219,
        7819.7743,
        3745.4669,
        0,
        0,
        0,
        0,
    ],
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(12, 6))

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
columns = ["12_Days", "17_Days", "52_Days"]
labels = ["12 Days", "17 Days", "52 Days"]

for col, color, label in zip(columns, colors, labels):
    ax.plot(
        df["Hour"],
        df[col],
        marker="o",
        linewidth=2,
        label=label,
        color=color,
    )

ax.set_xlabel("Hour", fontsize=14, fontweight="bold")
ax.set_ylabel("Power generation (MWh)", fontsize=14, fontweight="bold")

ax.tick_params(axis="x", colors="black", labelcolor="black")
ax.tick_params(axis="y", colors="black", labelcolor="black")
for spine in ax.spines.values():
    spine.set_color("black")

ax.legend()
plt.tight_layout()
plt.show()

#%%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ============================================================
# Professional style
# ============================================================

sns.set_theme(style="white")

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 11,

    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 13,
    "axes.labelweight": "bold",

    "xtick.labelsize": 11,
    "ytick.labelsize": 11,

    "legend.fontsize": 10.5,

    "figure.dpi": 120,
    "savefig.dpi": 300,
})


# ============================================================
# Colors
# ============================================================

colors_dict = {
    'Solar': '#FFD700',
    'WindOn': '#2ca02c',
    'WindOff': '#006400',
    'Gas': '#7f7f7f',
    'H2CCGT': '#ff69b4',
    'Nuclear': '#8B4513',
    'Biomass': '#7B6BA8',
    'Battery': '#CCFFFF'
}


# ============================================================
# Data
# ============================================================

data = {
    'Solar': [257, 259, 266],
    'WindOn': [164, 153, 130],
    'WindOff': [73, 72, 63],
    'Gas': [93, 94, 103],
    'H2CCGT': [26, 26, 26],
    'Nuclear': [1.3, 3.2, 3],
    'Biomass': [1, 1, 1],
    'Battery': [1.3, 2, 2]
}

states = ['12 Days', '17 Days', '52 Days']

df = pd.DataFrame(data, index=states)

plot_colors = [colors_dict[col] for col in df.columns]


# ============================================================
# Figure
# ============================================================

fig, ax = plt.subplots(figsize=(10.5, 6.5))


# ============================================================
# Stacked Bar Chart
# ============================================================

df.plot(
    kind='bar',
    stacked=True,
    ax=ax,
    color=plot_colors,
    edgecolor='black',
    linewidth=0.7,
    width=0.68
)


# ============================================================
# Title & Labels
# ============================================================


ax.set_xlabel(
    'Cases',
    fontsize=14,
    fontweight='bold',
    labelpad=10
)

ax.set_ylabel(
    'New Installed Capacity (GW)',
    fontsize=14,
    fontweight='bold',
    labelpad=10
)


# ============================================================
# Ticks
# ============================================================

ax.tick_params(
    axis='x',
    which='major',
    direction='out',
    length=5,
    width=1,
    colors='black',
    labelcolor='black',
    rotation=0,
    pad=6
)

ax.tick_params(
    axis='y',
    which='major',
    direction='out',
    length=5,
    width=1,
    colors='black',
    labelcolor='black',
    pad=6
)


# ============================================================
# Grid
# ============================================================

ax.grid(
    axis='y',
    linestyle='-',
    linewidth=0.7,
    alpha=0.18
)

ax.grid(
    axis='x',
    visible=False
)

ax.set_axisbelow(True)


# ============================================================
# Spines
# ============================================================

# حذف قاب بالا و راست برای ظاهر مدرن‌تر
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# نگه داشتن محورهای اصلی
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')

ax.spines['left'].set_linewidth(1.1)
ax.spines['bottom'].set_linewidth(1.1)


# ============================================================
# Legend
# ============================================================

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1.0),
    frameon=False,
    fontsize=10.5,
    handlelength=1.5,
    handleheight=1.0,
    labelspacing=0.8,
    borderaxespad=0
)


# ============================================================
# Layout
# ============================================================

plt.tight_layout()

plt.show()