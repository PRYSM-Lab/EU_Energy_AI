import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

plt.rcParams["font.family"] = "serif"

# ==============================
file_path = "hourly_FR.xlsx"  

df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
   "Storage_Dis": "#CCFFFF",  
    "Storage_CH": "#00FFFF",
    "Import/Export": "#FF8C00"  
}

# ==============================
tech_order_gen = [
    "Nuclear",
    "Hydro",
    "CCGT",
    "CCGTCCS",
    "H2CCGT",
    "Biomass",
    "BECCS",
    "Import/Export",
    "WindOff",
    "WindOn",
    "Solar",
   
    "Storage_Dis"
]

# ==============================
# CREATE FIGURE (ONE PANEL)
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# ==============================
# STACK GENERATION
# ==============================
stack_values = [df[tech].values for tech in tech_order_gen]
stack_colors = [COLORS[tech] for tech in tech_order_gen]

ax.stackplot(
    hours,
    stack_values,
    colors=stack_colors,
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# STORAGE CHARGING (NEGATIVE AREA)
# ==============================
ax.stackplot(
    hours,
    df["Storage_CH"].values,
    colors=[COLORS["Storage_CH"]],
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# DEMAND LINE
# ==============================
ax.plot(
    hours,
    demand,
    color="black",
    linestyle="--",
    linewidth=3,
    label="Demand"
)

# ==============================
# AXIS FORMAT
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=14, fontweight="bold")
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.tick_params(axis='both', labelsize=14)
ax.yaxis.set_major_locator(MultipleLocator(50000))

# ---- FORCE FIXED 10^6 SCALE ----
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))   # همیشه ×10^6

ax.yaxis.set_major_formatter(formatter)

# ==============================
# LEGEND
# ==============================
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t])
    for t in tech_order_gen[::-1]
]

handles.extend([
    plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
    plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.2)
])

labels = tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(handles, labels, loc="lower center",fontsize=18, ncol=7, frameon=False)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

# Set font style
plt.rcParams["font.family"] = "serif"

# ==============================
# READ FROM EXCEL
# ==============================
file_path = "hourly_UK.xlsx"
df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# COLOR DEFINITIONS
# ==============================
COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
    "Storage_Dis": "#CCFFFF",
    "Storage_CH": "#00FFFF",   # Cyan
    "Import/Export": "#FF8C00" # Orange
}

# ==============================
# DATA PRE-PROCESSING
# ==============================
# Split Import/Export into positive (Import) and negative (Export) components
imp_exp_raw = df["Import/Export"].values
imports_pos = np.where(imp_exp_raw > 0, imp_exp_raw, 0)
exports_neg = np.where(imp_exp_raw < 0, imp_exp_raw, 0)

# Storage charging is typically negative
storage_ch = df["Storage_CH"].values

# ==============================
# STACK ORDER (POSITIVE)
# ==============================
tech_order_gen = [
    "Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", 
    "Biomass", "BECCS", "WindOff", "WindOn", "Solar", "Storage_Dis"
]

# ==============================
# CREATE FIGURE (ONE PANEL)
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# ==============================
# STACK GENERATION (ABOVE ZERO)
# ==============================
# We stack standard generation + positive imports
stack_values_pos = [df[tech].values for tech in tech_order_gen]
stack_values_pos.append(imports_pos) # Add positive imports to the top of stack
stack_colors_pos = [COLORS[tech] for tech in tech_order_gen] + [COLORS["Import/Export"]]

ax.stackplot(
    hours,
    stack_values_pos,
    colors=stack_colors_pos,
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# STACK NEGATIVE AREA (BELOW ZERO)
# ==============================
# We use a second stackplot to stack Exports and Storage_CH downward
# We pass them as a list to ensure they stack relative to each other
ax.stackplot(
    hours,
    exports_neg,
    storage_ch,
    colors=[COLORS["Import/Export"], COLORS["Storage_CH"]],
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# DEMAND LINE
# ==============================
ax.plot(
    hours,
    demand,
    color="black",
    linestyle="--",
    linewidth=3,
    label="Demand"
)

# ==============================
# AXIS FORMAT
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=13)
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.axhline(0, color='black', linewidth=1.2) # Clear zero line
ax.tick_params(axis='both', labelsize=14)

ax.yaxis.set_major_locator(MultipleLocator(50000))

# ---- FORCE FIXED 10^6 SCALE ----
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)

# ==============================
# LEGEND
# ==============================
# Build handles for generation (reversed order)
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t])
    for t in tech_order_gen[::-1]
]

# Add specific handles for Import/Export, Storage_CH, and Demand
handles.insert(0, plt.Rectangle((0, 0), 1, 1, color=COLORS["Import/Export"]))
handles.extend([
    plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
    plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.2)
])

# Create matching labels
labels = ["Import/Export"] + tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(handles, labels, loc="lower center", ncol=9, frameon=False)

# Maintain your specific tight_layout schematic
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

# Professional font settings
plt.rcParams["font.family"] = "serif"

# ==============================
# 1. DATA LOADING
# ==============================
file_path = "hourly_PL.xlsx"
df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# 2. CONFIGURATION & COLORS
# ==============================
COLORS = {
    "Solar": "#FFD700", "WindOn": "#2ca02c", "WindOff": "#006400",
    "Nuclear": "#8B4513", "CCGT": "#7f7f7f", "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4", "Hydro": "#1E90FF", "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7", "Storage_Dis": "#CCFFFF", "Storage_CH": "#00FFFF",
    "Import/Export": "#FF8C00"
}

# The order for the positive stack (Bottom to Top)
# Import/Export will be added AFTER Solar to be on top
tech_order_gen = [
    "Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", 
    "Biomass", "BECCS", "WindOff", "WindOn", "Solar", "Storage_Dis"
]

# ==============================
# 3. DATA PRE-PROCESSING (The "No-Mess" Fix)
# ==============================
# We split the Import/Export column into two separate arrays
imp_exp_raw = df["Import/Export"].values
imports_only = np.where(imp_exp_raw > 0, imp_exp_raw, 0) # Only positive
exports_only = np.where(imp_exp_raw < 0, imp_exp_raw, 0) # Only negative

# Storage charging (Negative area)
storage_ch = df["Storage_CH"].values

# ==============================
# 4. PLOTTING
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# --- STACK ABOVE ZERO ---
# We add 'imports_only' as the last item so it sits on top of Solar/Storage_Dis
stack_pos_values = [df[tech].values for tech in tech_order_gen] + [imports_only]
stack_pos_colors = [COLORS[tech] for tech in tech_order_gen] + [COLORS["Import/Export"]]

ax.stackplot(hours, stack_pos_values, colors=stack_pos_colors, edgecolor="black", linewidth=0.3)

# --- STACK BELOW ZERO ---
# Exports and Storage stack downwards from the zero line
ax.stackplot(hours, exports_only, storage_ch, 
             colors=[COLORS["Import/Export"], COLORS["Storage_CH"]], 
             edgecolor="black", linewidth=0.3)

# --- DEMAND LINE ---
ax.plot(hours, demand, color="black", linestyle="--", linewidth=3, label="Demand", zorder=10)

# ==============================
# 5. FORMATTING
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=13)
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.axhline(0, color='black', linewidth=1.5) # Zero axis line
ax.tick_params(axis='both', labelsize=14)

# Y-Axis Scaling (Fixed 10^6)
ax.yaxis.set_major_locator(MultipleLocator(20000))
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)

# Legend (Matches the visual stack from top to bottom)
labels = ["Import/Export"] + tech_order_gen[::-1] + ["Storage_Chr", "Demand"]
handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS["Import/Export"])]
handles += [plt.Rectangle((0, 0), 1, 1, color=COLORS[t]) for t in tech_order_gen[::-1]]
handles += [plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
            plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.5)]

fig.legend(handles, labels, loc="lower center", ncol=9, frameon=False, fontsize=10)

plt.tight_layout(rect=[0, 0.1, 1, 1])
plt.show()

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

# Set font style
plt.rcParams["font.family"] = "serif"

# ==============================
# READ FROM EXCEL
# ==============================
file_path = "hourly_ES.xlsx"
df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# COLOR DEFINITIONS
# ==============================
COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
    "Storage_Dis": "#CCFFFF",
    "Storage_CH": "#00FFFF",   # Cyan
    "Import/Export": "#FF8C00" # Orange
}

# ==============================
# DATA PRE-PROCESSING
# ==============================
# Split Import/Export into positive (Import) and negative (Export) components
imp_exp_raw = df["Import/Export"].values
imports_pos = np.where(imp_exp_raw > 0, imp_exp_raw, 0)
exports_neg = np.where(imp_exp_raw < 0, imp_exp_raw, 0)

# Storage charging is typically negative
storage_ch = df["Storage_CH"].values

# ==============================
# STACK ORDER (POSITIVE)
# ==============================
tech_order_gen = [
    "Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", 
    "Biomass", "BECCS", "WindOff", "WindOn", "Solar", "Storage_Dis"
]

# ==============================
# CREATE FIGURE (ONE PANEL)
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# ==============================
# STACK GENERATION (ABOVE ZERO)
# ==============================
# We stack standard generation + positive imports
stack_values_pos = [df[tech].values for tech in tech_order_gen]
stack_values_pos.append(imports_pos) # Add positive imports to the top of stack
stack_colors_pos = [COLORS[tech] for tech in tech_order_gen] + [COLORS["Import/Export"]]

ax.stackplot(
    hours,
    stack_values_pos,
    colors=stack_colors_pos,
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# STACK NEGATIVE AREA (BELOW ZERO)
# ==============================
# We use a second stackplot to stack Exports and Storage_CH downward
# We pass them as a list to ensure they stack relative to each other
ax.stackplot(
    hours,
    exports_neg,
    storage_ch,
    colors=[COLORS["Import/Export"], COLORS["Storage_CH"]],
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# DEMAND LINE
# ==============================
ax.plot(
    hours,
    demand,
    color="black",
    linestyle="--",
    linewidth=3,
    label="Demand"
)

# ==============================
# AXIS FORMAT
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=13)
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.axhline(0, color='black', linewidth=1.2) # Clear zero line

ax.yaxis.set_major_locator(MultipleLocator(50000))

# ---- FORCE FIXED 10^6 SCALE ----
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)

# ==============================
# LEGEND
# ==============================
# Build handles for generation (reversed order)
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t])
    for t in tech_order_gen[::-1]
]

# Add specific handles for Import/Export, Storage_CH, and Demand
handles.insert(0, plt.Rectangle((0, 0), 1, 1, color=COLORS["Import/Export"]))
handles.extend([
    plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
    plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.2)
])

# Create matching labels
labels = ["Import/Export"] + tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(handles, labels, loc="lower center", ncol=9, frameon=False)

# Maintain your specific tight_layout schematic
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()


#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

# Professional font settings
plt.rcParams["font.family"] = "serif"

# ==============================
# 1. DATA LOADING
# ==============================
file_path = "hourly_IT1.xlsx"
df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# 2. CONFIGURATION & COLORS
# ==============================
COLORS = {
    "Solar": "#FFD700", "WindOn": "#2ca02c", "WindOff": "#006400",
    "Nuclear": "#8B4513", "CCGT": "#7f7f7f", "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4", "Hydro": "#1E90FF", "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7", "Storage_Dis": "#CCFFFF", "Storage_CH": "#00FFFF",
    "Import/Export": "#FF8C00"
}

# The order for the positive stack (Bottom to Top)
# Import/Export will be added AFTER Solar to be on top
tech_order_gen = [
    "Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", 
    "Biomass", "BECCS", "WindOff", "WindOn", "Solar", "Storage_Dis"
]

# ==============================
# 3. DATA PRE-PROCESSING (The "No-Mess" Fix)
# ==============================
# We split the Import/Export column into two separate arrays
imp_exp_raw = df["Import/Export"].values
imports_only = np.where(imp_exp_raw > 0, imp_exp_raw, 0) # Only positive
exports_only = np.where(imp_exp_raw < 0, imp_exp_raw, 0) # Only negative

# Storage charging (Negative area)
storage_ch = df["Storage_CH"].values

# ==============================
# 4. PLOTTING
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# --- STACK ABOVE ZERO ---
# We add 'imports_only' as the last item so it sits on top of Solar/Storage_Dis
stack_pos_values = [df[tech].values for tech in tech_order_gen] + [imports_only]
stack_pos_colors = [COLORS[tech] for tech in tech_order_gen] + [COLORS["Import/Export"]]

ax.stackplot(hours, stack_pos_values, colors=stack_pos_colors, edgecolor="black", linewidth=0.3)

# --- STACK BELOW ZERO ---
# Exports and Storage stack downwards from the zero line
ax.stackplot(hours, exports_only, storage_ch, 
             colors=[COLORS["Import/Export"], COLORS["Storage_CH"]], 
             edgecolor="black", linewidth=0.3)

# --- DEMAND LINE ---
ax.plot(hours, demand, color="black", linestyle="--", linewidth=3, label="Demand", zorder=10)

# ==============================
# 5. FORMATTING
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=13)
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.axhline(0, color='black', linewidth=1.5) # Zero axis line
ax.tick_params(axis='both', labelsize=14)

# Y-Axis Scaling (Fixed 10^6)
ax.yaxis.set_major_locator(MultipleLocator(50000))
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)

# Legend (Matches the visual stack from top to bottom)
labels = ["Import/Export"] + tech_order_gen[::-1] + ["Storage_Chr", "Demand"]
handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS["Import/Export"])]
handles += [plt.Rectangle((0, 0), 1, 1, color=COLORS[t]) for t in tech_order_gen[::-1]]
handles += [plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
            plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.5)]

fig.legend(handles, labels, loc="lower center", ncol=9, frameon=False, fontsize=10)

plt.tight_layout(rect=[0, 0.1, 1, 1])
plt.show()

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

# Set font style
plt.rcParams["font.family"] = "serif"

# ==============================
# READ FROM EXCEL
# ==============================
file_path = "hourly_NL.xlsx"
df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# COLOR DEFINITIONS
# ==============================
COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
    "Storage_Dis": "#CCFFFF",
    "Storage_CH": "#00FFFF",   # Cyan
    "Import/Export": "#FF8C00" # Orange
}

# ==============================
# DATA PRE-PROCESSING
# ==============================
# Split Import/Export into positive (Import) and negative (Export) components
imp_exp_raw = df["Import/Export"].values
imports_pos = np.where(imp_exp_raw > 0, imp_exp_raw, 0)
exports_neg = np.where(imp_exp_raw < 0, imp_exp_raw, 0)

# Storage charging is typically negative
storage_ch = df["Storage_CH"].values

# ==============================
# STACK ORDER (POSITIVE)
# ==============================
tech_order_gen = [
    "Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", 
    "Biomass", "BECCS", "WindOff", "WindOn", "Solar", "Storage_Dis"
]

# ==============================
# CREATE FIGURE (ONE PANEL)
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# ==============================
# STACK GENERATION (ABOVE ZERO)
# ==============================
# We stack standard generation + positive imports
stack_values_pos = [df[tech].values for tech in tech_order_gen]
stack_values_pos.append(imports_pos) # Add positive imports to the top of stack
stack_colors_pos = [COLORS[tech] for tech in tech_order_gen] + [COLORS["Import/Export"]]

ax.stackplot(
    hours,
    stack_values_pos,
    colors=stack_colors_pos,
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# STACK NEGATIVE AREA (BELOW ZERO)
# ==============================
# We use a second stackplot to stack Exports and Storage_CH downward
# We pass them as a list to ensure they stack relative to each other
ax.stackplot(
    hours,
    exports_neg,
    storage_ch,
    colors=[COLORS["Import/Export"], COLORS["Storage_CH"]],
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# DEMAND LINE
# ==============================
ax.plot(
    hours,
    demand,
    color="black",
    linestyle="--",
    linewidth=3,
    label="Demand"
)

# ==============================
# AXIS FORMAT
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=13)
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.axhline(0, color='black', linewidth=1.2) # Clear zero line
ax.tick_params(axis='both', labelsize=14)

ax.yaxis.set_major_locator(MultipleLocator(50000))

# ---- FORCE FIXED 10^6 SCALE ----
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)

# ==============================
# LEGEND
# ==============================
# Build handles for generation (reversed order)
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t])
    for t in tech_order_gen[::-1]
]

# Add specific handles for Import/Export, Storage_CH, and Demand
handles.insert(0, plt.Rectangle((0, 0), 1, 1, color=COLORS["Import/Export"]))
handles.extend([
    plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
    plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.2)
])

# Create matching labels
labels = ["Import/Export"] + tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(handles, labels, loc="lower center", ncol=9, frameon=False)

# Maintain your specific tight_layout schematic
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

# Set font style
plt.rcParams["font.family"] = "serif"

# ==============================
# READ FROM EXCEL
# ==============================
file_path = "hourly_IE.xlsx"
df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# COLOR DEFINITIONS
# ==============================
COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
    "Storage_Dis": "#CCFFFF",
    "Storage_CH": "#00FFFF",   # Cyan
    "Import/Export": "#FF8C00" # Orange
}

# ==============================
# DATA PRE-PROCESSING
# ==============================
# Split Import/Export into positive (Import) and negative (Export) components
imp_exp_raw = df["Import/Export"].values
imports_pos = np.where(imp_exp_raw > 0, imp_exp_raw, 0)
exports_neg = np.where(imp_exp_raw < 0, imp_exp_raw, 0)

# Storage charging is typically negative
storage_ch = df["Storage_CH"].values

# ==============================
# STACK ORDER (POSITIVE)
# ==============================
tech_order_gen = [
    "Nuclear", "Hydro", "CCGT", "CCGTCCS", "H2CCGT", 
    "Biomass", "BECCS", "WindOff", "WindOn", "Solar", "Storage_Dis"
]

# ==============================
# CREATE FIGURE (ONE PANEL)
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# ==============================
# STACK GENERATION (ABOVE ZERO)
# ==============================
# We stack standard generation + positive imports
stack_values_pos = [df[tech].values for tech in tech_order_gen]
stack_values_pos.append(imports_pos) # Add positive imports to the top of stack
stack_colors_pos = [COLORS[tech] for tech in tech_order_gen] + [COLORS["Import/Export"]]

ax.stackplot(
    hours,
    stack_values_pos,
    colors=stack_colors_pos,
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# STACK NEGATIVE AREA (BELOW ZERO)
# ==============================
# We use a second stackplot to stack Exports and Storage_CH downward
# We pass them as a list to ensure they stack relative to each other
ax.stackplot(
    hours,
    exports_neg,
    storage_ch,
    colors=[COLORS["Import/Export"], COLORS["Storage_CH"]],
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# DEMAND LINE
# ==============================
ax.plot(
    hours,
    demand,
    color="black",
    linestyle="--",
    linewidth=3,
    label="Demand"
)

# ==============================
# AXIS FORMAT
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=13)
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.axhline(0, color='black', linewidth=1.2) # Clear zero line
ax.tick_params(axis='both', labelsize=14)

ax.yaxis.set_major_locator(MultipleLocator(10000))

# ---- FORCE FIXED 10^6 SCALE ----
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))
ax.yaxis.set_major_formatter(formatter)
# ==============================
# LEGEND
# ==============================
# Build handles for generation (reversed order)
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t])
    for t in tech_order_gen[::-1]
]

# Add specific handles for Import/Export, Storage_CH, and Demand
handles.insert(0, plt.Rectangle((0, 0), 1, 1, color=COLORS["Import/Export"]))
handles.extend([
    plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
    plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.2)
])

# Create matching labels
labels = ["Import/Export"] + tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(handles, labels, loc="lower center", ncol=9, frameon=False)

# Maintain your specific tight_layout schematic
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter

plt.rcParams["font.family"] = "serif"

# ==============================
# READ FROM EXCEL
# ==============================
file_path = "hourly_IT1.xlsx"   # <<< مسیر فایل

df = pd.read_excel(file_path, sheet_name="Dispatch")
df_demand = pd.read_excel(file_path, sheet_name="Demand")

hours = df["Hour"].values
demand = df_demand["Demand"].values

# ==============================
# COLOR DEFINITIONS
# ==============================
COLORS = {
    "Solar": "#FFD700",
    "WindOn": "#2ca02c",
    "WindOff": "#006400",
    "Nuclear": "#8B4513",
    "CCGT": "#7f7f7f",
    "CCGTCCS": "#4d4d4d",
    "H2CCGT": "#ff69b4",
    "Hydro": "#1E90FF",
    "Biomass": "#7B6BA8",
    "BECCS": "#B4A7D7",
   "Storage_Dis": "#CCFFFF",   # bright cyan (very visible)
    "Storage_CH": "#00FFFF",
    "Import/Export": "#FF8C00"   # نارنجی برای تبادل شبکه
}

# ==============================
# STACK ORDER  (همان ترتیب قبلی)
# ==============================
tech_order_gen = [
    "Nuclear",
    "Hydro",
    "CCGT",
    "CCGTCCS",
    "H2CCGT",
    "Biomass",
    "BECCS",
    "Import/Export",
    "WindOff",
    "WindOn",
    "Solar",
   
    "Storage_Dis"
]

# ==============================
# CREATE FIGURE (ONE PANEL)
# ==============================
fig, ax = plt.subplots(figsize=(14, 8))

# ==============================
# STACK GENERATION
# ==============================
stack_values = [df[tech].values for tech in tech_order_gen]
stack_colors = [COLORS[tech] for tech in tech_order_gen]

ax.stackplot(
    hours,
    stack_values,
    colors=stack_colors,
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# STORAGE CHARGING (NEGATIVE AREA)
# ==============================
ax.stackplot(
    hours,
    df["Storage_CH"].values,
    colors=[COLORS["Storage_CH"]],
    edgecolor="black",
    linewidth=0.5
)

# ==============================
# DEMAND LINE
# ==============================
ax.plot(
    hours,
    demand,
    color="black",
    linestyle="--",
    linewidth=3,
    label="Demand"
)

# ==============================
# AXIS FORMAT
# ==============================
ax.set_xlim(1, 24)
ax.set_xticks([1, 6, 12, 18, 24])
ax.set_xlabel("Hour of Day", fontsize=14, fontweight="bold")
ax.set_ylabel("Energy Dispatch (TWh)", fontsize=16, fontweight="bold")
ax.tick_params(axis='both', labelsize=14)
ax.yaxis.set_major_locator(MultipleLocator(50000))

# ---- FORCE FIXED 10^6 SCALE ----
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((6, 6))   # همیشه ×10^6

ax.yaxis.set_major_formatter(formatter)

# ==============================
# LEGEND
# ==============================
handles = [
    plt.Rectangle((0, 0), 1, 1, color=COLORS[t])
    for t in tech_order_gen[::-1]
]

handles.extend([
    plt.Rectangle((0, 0), 1, 1, color=COLORS["Storage_CH"]),
    plt.Line2D([0], [0], color="black", linestyle="--", linewidth=2.2)
])

labels = tech_order_gen[::-1] + ["Storage_Chr", "Demand"]

fig.legend(handles, labels, loc="lower center",fontsize=12, ncol=9, frameon=False)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()
