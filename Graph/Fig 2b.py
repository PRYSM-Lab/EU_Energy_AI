
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"

# -----------------------------
countries = ["AT", "BE", "Nordic", "FR", "DE", "GR", "IE", "IT", "NL", "PL", "PT", "ES", "UK"]
scenarios = [
    "IEA Base", "IEA Lift", "IEA High Eff", "IEA Head",
    "IEA Pessimistic Def", "IEA Pessimistic Med", "IEA Pessimistic End",
    "ICIS Base", "ICIS Lift", "ICIS High Eff", "ICIS Head",
    "ICIS Pessimistic Def", "ICIS Pessimistic Med", "ICIS Pessimistic End",
    "McKinsey Base", "McKinsey Lift", "McKinsey High Eff", "McKinsey Head",
    "McKinsey Pessimistic Def", "McKinsey Pessimistic Med", "McKinsey Pessimistic End"
]


file_path = "AI Capacity 2050.xlsx"  

df = pd.read_excel(file_path, index_col=0)

df.columns = df.columns.str.strip()

df.index = df.index.str.strip()

df = df.loc[countries, scenarios]

plt.figure(figsize=(16, 10))
df_rounded = df.round(0).astype(int)
ax = sns.heatmap(df_rounded, annot=True, fmt=".0f", cmap="rocket_r", 
                 linewidths=0.5)


ax.xaxis.tick_bottom()
ax.set_title("AI_Data Centre Capacity by 2050 (GW)", fontsize=18, pad=20)
ax.set_yticklabels(ax.get_yticklabels(), size=14)

ax.set_xlabel("Scenarios", fontsize=16, fontweight='bold', labelpad=15)

ax.set_ylabel("Countries", fontsize=16, fontweight='bold', labelpad=15)
ax.set_xticklabels(ax.get_xticklabels(), size=12)
plt.tight_layout()
plt.show()
