import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

data = {
    "IEA (Base)": 5,
    "IEA (Lift-Off)": 7,
    "IEA (High-Efficiency)": 4,
    "IEA (Headwinds)": 2,
    "IEA (Pessimistic - Deflation)": 0,
    "IEA (Pessimistic - Med)": 3,
    "IEA (Pessimistic -End)": 4,

    "ICIS (Base)": 6,
    "ICIS (Lift-Off)": 7,
    "ICIS (High-Efficiency)": 5,
    "ICIS (Headwinds)": 3,
    "ICIS (Pessimistic- Deflation)": 1,
    "ICIS (Pessimistic- Med)": 3,
    "ICIS (Pessimistic- End)": 4,

    "McKinsey (Base)": 7,
    "McKinsey (Lift-Off)": 9,
    "McKinsey (High-Efficiency)": 7,
    "McKinsey (Headwinds)": 5,
    "McKinsey (Pessimistic- Deflation)": 2,
    "McKinsey (Pessimistic- Med)": 4,
    "McKinsey (Pessimistic- End)": 6,
}


sorted_items = sorted(data.items(), key=lambda x: x[1])
scenarios = [item[0] for item in sorted_items]
values = [item[1] for item in sorted_items]
labels = [f"{v}%" for v in values]

n = len(scenarios)

# -------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 4))
ax.set_xlim(-0.5, n - 0.5)
ax.set_ylim(0, 1)
ax.axis('off')  # حذف محورها

# -------------------------------------------------
arrow_y = 0.35
ax.annotate('',
            xy=(n - 0.5, arrow_y), xycoords=('data', 'axes fraction'),
            xytext=(-0.5, arrow_y), textcoords=('data', 'axes fraction'),
            arrowprops=dict(arrowstyle="->", lw=2.5, color='black', mutation_scale=22))

# -------------------------------------------------
ax.text((n-1)/2, arrow_y + 0.18,
        'Projected CAGR of AI-Data Centres (2030–2050)',
        transform=ax.get_xaxis_transform(),
        ha='center', va='bottom',
        fontsize=14, fontweight='bold')

# -------------------------------------------------
vals = np.array(values)
norm = plt.Normalize(vals.min(), vals.max())
cmap = cm.get_cmap('coolwarm')  

# -------------------------------------------------
for i, val in enumerate(labels):
    color = cmap(norm(values[i]))  
    ax.text(i, arrow_y + 0.02, val,
            transform=ax.get_xaxis_transform(),
            rotation=90,
            ha='center', va='bottom',
            fontsize=14,
            color=color,
            fontweight='bold')

# -------------------------------------------------
for i, scen in enumerate(scenarios):
    ax.text(i, arrow_y - 0.08, scen,
            transform=ax.get_xaxis_transform(),
            rotation=40,
            ha='right', va='top',
            fontsize=12)

# -------------------------------------------------
plt.tight_layout()
plt.show()
