#%%DE
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
    'Total': [1330.152, 1235.929, 1177.427, 1157.908, 1155.787, 1171.364, 1215.214, 1317.946, 1480.077, 1524.089, 1463.739, 1406.378, 1353.857, 1308.812, 1266.566, 1233.618, 1213.719, 1226.604, 1284.182, 1420.406, 1513.215, 1481.626, 1468.224, 1422.635],
    'Flex_Final': [2607.337, 2400.053, 1044.856, 1065.548, 1145.248, 772.535, 0, 169.4434, 922.5148, 1985.234, 3093.601, 1480.628, 2779.191, 1332.865, 933.8296, 977.7038, 0, 0, 75.68694, 842.1007, 1543.076, 1420.478, 1773.406, 3464.139],
    'Temporal': [1330.152, 1169.22, -58.5021, -19.5188, -2.12043, -171.111, -958.787, -856.055, -693.924, 60.35064, 1463.739, 8e-11, 1353.857, -45.0455, -42.2455, -32.9482, -960.282, -947.396, -746.345, -92.8095, 31.58894, 13.40219, 45.5892, 1422.635],
    'Spatial': [-52.9667, -5.09613, -74.069, -72.8411, -8.41936, -227.718, -256.427, -292.447, 136.3615, 400.794, 166.1237, 74.24998, 71.4771, 69.09892, -290.491, -222.966, -253.436, -279.208, -462.15, -485.496, -1.72845, -74.5509, 259.5927, 618.8693]
}

# داده‌های پنل دوم
data2 = {
    'Total': [1254.741, 1177.997, 1129.364, 1099.379, 1097.34, 1124.96, 1171.636, 1224.022, 1340.944, 1458.682, 1565.275, 1662.08, 1759.158, 1839.272, 1888.151, 1929.39, 1972.234, 1986.424, 1951.002, 1848.107, 1725.72, 1664.826, 1542.222, 1400.235],
    'Flex_Final': [1461.214, 0, 231.3176, 1060.418, 163.1131, 1224.302, 1332.154, 813.189, 980.3191, 1467.021, 108.6802, 3369.777, 3916.267, 2082.397, 1861.669, 1956.575, 1891.009, 2019.676, 1944.894, 1727.665, 1469.286, 1340.728, 1435.357, 2956.131],
    'Temporal': [-95.9431, -896.572, -1044.64, -181.659, -1076.66, -46.6766, -52.3854, -116.923, -117.738, 405.328, -608.726, 1662.08, 1759.158, 80.11412, 48.87858, 41.23961, 42.84352, -187.576, -222.998, -325.893, -448.28, -509.175, -278.311, 1400.235],
    'Spatial': [302.4166, -281.426, 146.591, 142.699, 142.4343, 146.0194, 212.9035, -293.91, -242.887, -396.989, -847.868, 45.61641, 397.9514, 163.011, -75.3602, -14.0547, -124.068, 220.8277, 216.8899, 205.4512, 191.8457, 185.0761, 171.4464, 155.6619]
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


#%% ES
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
    'Total': [4185.021, 3888.569, 3704.506, 3643.094, 3636.423, 3685.432, 3823.394, 4146.617, 4656.726, 4795.202, 4605.322, 4424.851, 4259.604, 4117.879, 3984.963, 3881.299, 3818.69, 3859.232, 4040.388, 4468.985, 4760.989, 4661.602, 4619.435, 4475.999],
    'Flex_Final': [8265.966, 4858.343, 6750.3, 7284.794, 3670.401, 4026.919, 756.3262, 1729.119, 2532.062, 6482.876, 5171.774, 9361.611, 7938.442, 4103.527, 4247.012, 4162.325, 1079.742, 1260.967, 8339.847, 3457.688, 2360.523, 2303.66, 0, 0],
    'Temporal': [4185.021, 926.3052, 3004.383, 3600.975, -6.67145, 49.00947, -3016.61, -2693.38, -2183.27, 924.8013, 7.001831, 4244.03, 3291.601, -141.725, -132.916, -103.664, -3021.31, -2980.77, 4040.388, -1134.04, -2079.01, -2178.4, -1004.15, -2364.0],
    'Spatial': [-104.076, 43.46815, 41.4106, 40.72412, 40.64954, 292.4769, -50.4627, 275.8838, 58.60905, 762.873, 559.4499, 692.7301, 387.2368, 127.374, 394.9647, 384.6902, 282.3615, 382.503, 259.0724, 122.747, -321.455, -179.544, -3615.28, -2112.0]
}

# داده‌های پنل دوم
data2 = {
    'Total': [3947.757, 3706.302, 3553.286, 3458.945, 3452.53, 3539.43, 3686.288, 3851.107, 4218.977, 4589.413, 4924.782, 5229.359, 5534.791, 5786.852, 5940.638, 6070.389, 6205.186, 6249.834, 6138.386, 5814.65, 5429.588, 5237.998, 4852.251, 4405.521],
    'Flex_Final': [5740.045, 0, 0, 0, 0, 1386.583, 2156.419, 4095.912, 4488.82, 9633.701, 8826.358, 3241.242, 9095.092, 6612.47, 6683.222, 6801.799, 6955.003, 6913.926, 6635.337, 6067.226, 5582.673, 5565.565, 4384.194, 4958.674],
    'Temporal': [1917.822, -3116.63, -2203.79, -2156.33, -2218.07, -814.393, -164.819, -367.87, -370.436, 4589.413, 3738.409, -1602.59, 3398.973, 252.0609, 153.7854, 129.7511, 134.7974, 44.64737, -111.447, -323.736, -385.062, -191.59, -948.982, 116.5054],
    'Spatial': [-125.535, -589.667, -1349.49, -1302.61, -1234.46, -1338.45, -1365.05, 612.6761, 640.279, 454.8741, 163.1674, -385.526, 161.3276, 573.5567, 588.799, 601.6591, 615.0194, 619.4446, 608.3986, 576.3119, 538.1469, 519.1577, 480.9249, 436.6478]
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

#%% IE
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
    'Total': [1307.046, 1214.46, 1156.974, 1137.794, 1135.711, 1151.017, 1194.105, 1295.052, 1454.367, 1497.615, 1438.313, 1381.949, 1330.34, 1286.077, 1244.565, 1212.189, 1192.636, 1205.297, 1261.875, 1395.733, 1486.93, 1455.89, 1442.72, 1397.923],
    'Flex_Final': [3367.103, 2093.399, 2287.093, 2264.496, 2018.251, 2495.356, 2267.115, 1686.915, 1017.755, 382.5472, 266.5614, 256.73, 174.5274, 403.0474, 1308.077, 1301.509, 344.5072, 222.6764, 1111.203, 475.132, 795.1128, 1019.667, 2021.063, 1696.734],
    'Temporal': [1307.046, 179.2693, 463.5678, 471.2007, 228.2395, 681.2199, 385.0676, 100.9475, 159.3149, 43.24795, -59.3023, -56.3639, -126.874, 31.00186, -41.5116, -32.3759, -943.601, -930.94, -84.074, -740.504, 31.04022, 13.16939, 44.79729, 216.8809],
    'Spatial': [753.0102, 699.6697, 666.5511, 655.5014, 654.301, 663.1192, 687.9427, 290.9156, -595.927, -1158.32, -1112.45, -1068.85, -1028.94, -914.031, 105.0239, 121.6951, 95.47301, -51.6814, -66.5978, -180.096, -722.857, -449.392, 533.5452, 81.93012]
}

# داده‌های پنل دوم
data2 = {
    'Total': [1232.945, 1157.535, 1109.746, 1080.282, 1078.278, 1105.418, 1151.284, 1202.76, 1317.651, 1433.344, 1538.085, 1633.209, 1728.6, 1807.323, 1855.352, 1895.876, 1937.975, 1951.919, 1917.112, 1816.004, 1695.744, 1635.907, 1515.432, 1375.912],
    'Flex_Final': [3170.101, 2863.25, 660.3729, 2041.499, 2717.31, 709.493, 482.723, 1261.938, 553.2613, 1867.962, 318.5411, 1968.867, 450.654, 728.6635, 1237.262, 2044.355, 2076.925, 1953.05, 1930.789, 1716.719, 1577.185, 1444.307, 1272.898, 1125.569],
    'Temporal': [1232.945, 1103.744, -1026.49, 399.4216, 1078.278, -929.231, -670.947, -114.892, -69.1602, 1433.344, -46.5328, 1633.209, 95.39125, 78.72249, 48.02954, 40.52325, 42.0993, 13.94406, -34.8067, -101.108, -120.261, -59.8366, -120.475, -139.521],
    'Spatial': [704.2104, 601.9706, 577.1181, 561.7954, 560.7535, 533.3056, 2.385537, 174.0699, -695.23, -998.727, -1173.01, -1297.55, -1373.34, -1157.38, -666.12, 107.956, 96.85124, -12.8134, 48.48365, 1.822807, 1.702096, -131.763, -122.06, -110.822]
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

#%% FI
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
    'Total': [1111.421, 1032.692, 983.8102, 967.5011, 965.7293, 978.7449, 1015.384, 1101.222, 1236.693, 1273.468, 1223.041, 1175.113, 1131.228, 1093.59, 1058.292, 1030.761, 1014.134, 1024.901, 1073.011, 1186.834, 1264.382, 1237.987, 1226.789, 1188.697],
    'Flex_Final': [2791.17, 2305.89, 2190.389, 983.1465, 931.5652, 1249.94, 214.5717, 277.2628, 97.28477, 0, 0, 0, 0, 181.332, 192.9977, 551.2127, 23.28088, 430.6329, 1525.921, 1919.72, 2154.164, 2094.55, 3291.296, 3189.099],
    'Temporal': [1111.421, 1032.692, 977.4568, -16.3091, -1.77174, 13.01551, 36.63876, 85.83874, -117.688, -221.365, -212.6, -204.268, -196.64, -8.7654, 9.036223, 372.0367, -802.373, -791.606, -113.823, -77.5479, 26.39445, 11.19833, 1226.789, 1188.697],
    'Spatial': [568.3276, 240.5059, 229.1217, 31.9545, -32.3924, 258.1798, -837.451, -909.798, -1021.72, -1052.1, -1010.44, -970.845, -934.588, -903.493, -874.33, -851.585, -188.48, 197.338, 566.7332, 810.434, 863.3879, 845.3644, 837.7175, 811.7059]
}

# داده‌های پنل دوم
data2 = {
    'Total': [1048.411, 984.2872, 943.6507, 918.5964, 916.8928, 939.9709, 978.972, 1022.743, 1120.439, 1218.816, 1307.88, 1388.767, 1469.881, 1536.822, 1577.663, 1612.121, 1647.919, 1659.776, 1630.179, 1544.204, 1441.942, 1391.062, 1288.618, 1169.98],
    'Flex_Final': [0, 1697.048, 1613.08, 1547.567, 1519.918, 1542.833, 1603.696, 480.5405, 148.3226, 99.14546, 121.076, 133.3395, 160.0391, 400.8617, 42.36099, 3077.021, 1737.711, 2160.99, 2090.063, 3700.539, 2173.562, 1276.478, 1118.263, 2315.138],
    'Temporal': [-768.097, 40.63654, 25.05428, 1.7036, -23.0781, -39.0011, -43.7712, -97.6958, -98.3772, -89.0642, -80.8869, -81.1141, -66.9401, 163.5456, -238.845, 1612.121, -168.588, -156.731, -186.328, 1544.204, 409.3865, -425.446, -527.889, 681.3719],
    'Spatial': [-280.314, 672.1243, 644.3754, 627.267, 626.1037, 641.8627, 668.4947, -444.507, -873.739, -1030.61, -1105.92, -1174.31, -1242.9, -1299.51, -1296.46, -147.22, 258.3806, 657.9447, 646.2122, 612.1312, 322.2328, 310.8624, 357.5339, 463.7866]
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