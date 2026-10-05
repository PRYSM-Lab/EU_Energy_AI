import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# تنظیمات عمومی فونت و رنگ
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black"
})

# داده‌های پنل اول
data1 = {
    'Total': [4601.422, 4275.474, 4073.096, 4005.574, 3998.239, 4052.125, 4203.814, 4559.197, 5120.061, 5272.314, 5063.542, 4865.114, 4683.426, 4527.599, 4381.458, 4267.48, 4198.642, 4243.217, 4442.397, 4913.639, 5234.697, 5125.421, 5079.059, 4921.351],
    'Flex_Final': [9326.977, 4604.893, 2404.879, 8267.216, 8082.144, 4192.831, 4445.573, 5206.039, 5476.69, 2572.59, 5349.436, 5170.344, 3993.34, 3880.29, 3759.699, 3644.214, 375.6458, 459.4774, 7517.45, 2655.768, 2324.113, 2118.601, 4818.297, 9461.85],
    'Temporal': [4601.422, +56.09833, -1878.91, +4005.574, +3998.239, +53.88581, +151.689, +355.383, +560.8638, -1965.2, +876.9075, +833.3503, -181.688, -155.827, -146.141, -113.978, -3321.92, -3277.35, +3605.215, -1671.47, -2285.87, -2395.14, +157.7077, +4921.351],
    'Spatial': [+124.1336, +273.3213, +210.6967, +256.0673, +85.66566, +86.82021, +90.07027, +291.4591, -204.235, -734.519, -591.013, -528.121, -508.398, -491.483, -475.619, -509.288, -501.072, -506.392, -530.162, -586.401, -624.717, -611.676, -418.469, -380.851]
}

# داده‌های پنل دوم
data2 = {
    'Total': [+4340.55, +4075.071, +3906.831, +3803.103, +3796.05, +3891.596, +4053.065, +4234.283, +4638.756, +5046.05, +5414.787, +5749.669, +6085.491, +6362.632, +6531.718, +6674.379, +6822.589, +6871.679, +6749.142, +6393.195, +5969.82, +5759.167, +5335.04, +4843.861],
    'Flex_Final': [+8774.101, +302.4356, +1539.565, +2138.156, +3093.443, +2625.926, +5392.578, +3680.605, +2460.555, +4947.858, +10097.15, +10425.62, +6384.388, +6150.87, +6198.91, +6304.183, +7123.649, +6915.09, +6621.029, +6031.965, +5120.157, +3993.01, +3248.721, +7978.563],
    'Temporal': [+4340.55, -3445.49, -2316.38, -1746.43, -783.941, -1349.05, +1410.997, -478.998, -1924.98, +317.5572, +4728.493, +5749.669, +335.8224, +277.1404, +169.0867, +142.661, +148.2095, +49.08969, -122.536, -355.947, -844.73, -1761.4, -2081.91, +3138.704],
    'Spatial': [-92.99996, -327.141, -50.887, +81.4847, +81.33358, +83.38074, -71.4839, -74.6801, -253.218, -415.749, +446.13, +473.721, +436.925, -488.902, -501.895, -512.857, +152.8507, -5.67802, -5.57677, -5.28265, -4.93282, -4.75876, -4.4083, -4.00245]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
x = range(1, 25)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# تعریف مستقیم متغیرها برای ساخت لجند مطمئن
line1, = ax1.plot(x, df1['Flex_Final'], color='black', linestyle='-', linewidth=2, label='Final workload with Flex')
poly1 = ax1.fill_between(x, df1['Temporal'], 0, color='#4f7a8a', alpha=0.75, label='Workload that is shifted \n temporally (- delay, + advanced)')
poly2 = ax1.fill_between(x, df1['Spatial'], 0, color='#ff4d4d', alpha=0.75, label='Workload that is shifted to other region (-)\n comes from other region (+)')
line2, = ax1.plot(x, df1['Total'], color='black', linestyle='--', linewidth=2, label='Base workload')

# رسم پنل دوم
ax2.plot(x, df2['Flex_Final'], color='black', linestyle='-', linewidth=2)
ax2.fill_between(x, df2['Temporal'], 0, color='#4f7a8a', alpha=0.75)
ax2.fill_between(x, df2['Spatial'], 0, color='#ff4d4d', alpha=0.75)
ax2.plot(x, df2['Total'], color='black', linestyle='--', linewidth=2)

for ax in (ax1, ax2):
    ax.set_xlim(1, 24)
    ax.set_xticks(range(1, 24, 2))
    ax.set_xlabel("Hour", fontsize=10)
    ax.set_ylabel("Demand (MWh)", fontsize=12)
    ax.grid(True, axis='y', linestyle='--', color='gray', alpha=0.2)
    
    for spine in ax.spines.values():
        spine.set_color('grey')
        spine.set_linewidth(0.5)

# تعریف صریح دستگیره‌ها و برچسب‌ها
handles = [line1, poly1, poly2, line2]
labels = [h.get_label() for h in handles]

# افزودن لجند به شکل اصلی
fig.legend(handles=handles, labels=labels, loc='lower center', bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False, fontsize=9)

plt.tight_layout()
plt.subplots_adjust(bottom=0.22,wspace=0.3)
plt.savefig('combined_chart.png', dpi=300, bbox_inches='tight')
plt.show()