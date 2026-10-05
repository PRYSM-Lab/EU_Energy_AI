import pandas as pd
import os

# پیدا کردن مسیر پوشه‌ای که همین کد در آن قرار دارد
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'EuropeWinter.xlsx')

desired_order = [
    "Nuclear", "Hydro", "CCGTCCS", "CCGT", "Biomass", 
    "BiomasCCS", "H2CCGT", "WindOn", "WindOff", "Solar"
]

# بارگذاری فایل
df = pd.read_excel(file_path)

existing_cols = [col for col in desired_order if col in df.columns]
df_ordered = df[existing_cols]

existing_cols = [col for col in desired_order if col in df.columns]
df_ordered = df[existing_cols]
import numpy as np

bad_rows = df[df['Generation'].isna() | np.isinf(df['Generation'])]
print(bad_rows)
# تمیز کردن ستون ساعت
df['h'] = df['h'].replace({'h': ''}, regex=True).astype(int)

# ۲. فیلتر کردن داده‌ها
filtered_df = df[  
    (df['t'] == 6) & 
    (df['k'] == 'k11')
]

# ۳. ایجاد Pivot Table
# استفاده از pivot_table برای جمع زدن مقادیر بر اساس تکنولوژی (j) و ساعت (h)
pivot_df = filtered_df.pivot_table(
    index='h', 
    columns='j', 
    values='Generation', 
    aggfunc='sum'
).reset_index()

# ۴. اطمینان از وجود تمام ستون‌های لیست در دیتای نهایی
# اگر تکنولوژی در داده‌ها نباشد، ستون آن با مقدار 0 ایجاد می‌شود تا در نمودار خطا ندهد
for tech in desired_order:
    if tech not in pivot_df.columns:
        pivot_df[tech] = 0

# ۵. مرتب‌سازی ستون‌ها بر اساس لیست دلخواه (به علاوه ستون h)
pivot_df = pivot_df[['h'] + desired_order]

# ۶. مرتب‌سازی سطرها بر اساس ساعت
pivot_df = pivot_df.sort_values(by='h')

# ۷. ایجاد ستون h_label برای نمایش در نمودار
#pivot_df['h_label'] = 'h' + pivot_df['h'].astype(str)

# ۸. ذخیره فایل اکسل نهایی
pivot_df.to_excel('Europe without flex winter.xlsx', index=False)

print("فایل اکسل با ترتیب ستون‌های درخواستی ایجاد شد.")

#%%
import pandas as pd

# ۱. خواندن فایل اکسل
df_demand = pd.read_excel('demand_europe.xlsx')

# ۲. تمیزکاری مقادیر متنی و فاصله‌های خالی
df_demand['k'] = df_demand['k'].astype(str).str.strip()
df_demand['h'] = df_demand['h'].astype(str).str.replace('h', '').str.strip().astype(int)

# ۳. اطمینان از عددی بودن ستون Base Demand برای جمع ریاضی
df_demand['Base Demand'] = pd.to_numeric(df_demand['Base Demand'], errors='coerce')

# ۴. فیلتر کردن (برای k11 و t=6)
filtered_demand = df_demand[
    (df_demand['t'] == 6) & 
    (df_demand['k'] == 'k1')  # اگر k1 مد نظرتان است این را به 'k1' تغییر دهید
]

# ۵. جمع‌بندی مجموع تقاضای همه کشورها به ازای هر ساعت
demand_summary = filtered_demand.groupby('h', as_index=False)['Base Demand'].sum()

# ۶. مرتب‌سازی
demand_summary = demand_summary.sort_values(by='h')

# ۷. ذخیره در فایل
demand_summary.to_excel('demand_with_winter.xlsx', index=False)

print("تعداد ردیف‌های پیدا شده بعد از فیلتر:", len(filtered_demand))
print(demand_summary.head())

#%%
import pandas as pd

# ۱. خواندن فایل اکسل داده‌های تقاضا
df_demand = pd.read_excel('demand_europe.xlsx')

# ۲. تمیز کردن ستون ساعت
df_demand['h'] = df_demand['h'].replace({'h': ''}, regex=True).astype(int)

# ۳. فیلتر کردن داده‌ها بر اساس سال ۵ و کلاستر c1
filtered_demand = df_demand[
    (df_demand['t'] == 6) & 
    (df_demand['k'] == 'k11')
]

# ۴. جمع‌بندی داده‌ها بر اساس ساعت
# اگر چندین منطقه (g) دارید و می‌خواهید مجموع تقاضا را داشته باشید
demand_summary = filtered_demand.groupby('h')['Base Demand'].sum().reset_index()

# ۵. مرتب‌سازی نهایی
demand_summary = demand_summary.sort_values(by='h')

# ۶. ذخیره در فایل نهایی
demand_summary.to_excel('demand_with winter.xlsx', index=False)

print("فایل تقاضا با موفقیت پردازش شد.")

#%%
import pandas as pd

# لیست ترتیب ستون‌ها از پایین به بالا برای نمودار
desired_order = [
    "LeadBat"
]

# ۱. بارگذاری داده‌ها
df = pd.read_csv('your_file.csv') 

# تمیز کردن ستون ساعت
df['h'] = df['h'].replace({'h': ''}, regex=True).astype(int)

# ۲. فیلتر کردن داده‌ها
filtered_df = df[ (df['g']=='NT')& 
    (df['t'] == 4) & 
    (df['c'] == 'c1')
]

# ۳. ایجاد Pivot Table
# استفاده از pivot_table برای جمع زدن مقادیر بر اساس تکنولوژی (j) و ساعت (h)
pivot_df = filtered_df.pivot_table(
    index='h', 
    columns='j', 
    values='Storage DisCharge', 
    aggfunc='sum'
).reset_index()

# ۴. اطمینان از وجود تمام ستون‌های لیست در دیتای نهایی
# اگر تکنولوژی در داده‌ها نباشد، ستون آن با مقدار 0 ایجاد می‌شود تا در نمودار خطا ندهد
for tech in desired_order:
    if tech not in pivot_df.columns:
        pivot_df[tech] = 0

# ۵. مرتب‌سازی ستون‌ها بر اساس لیست دلخواه (به علاوه ستون h)
pivot_df = pivot_df[['h'] + desired_order]

# ۶. مرتب‌سازی سطرها بر اساس ساعت
pivot_df = pivot_df.sort_values(by='h')

# ۷. ایجاد ستون h_label برای نمایش در نمودار
#pivot_df['h_label'] = 'h' + pivot_df['h'].astype(str)

# ۸. ذخیره فایل اکسل نهایی
pivot_df.to_excel('processed_data_WithoutDC.xlsx', index=False)

print("فایل اکسل با ترتیب ستون‌های درخواستی ایجاد شد.")


#%%
import pandas as pd

# لیست ترتیب ستون‌ها از پایین به بالا برای نمودار
desired_order = [
    "Nuclear", "Hydro", "CCGTCCS", "CCGT", "Biomass", 
    "BECCS", "H2CCGT", "FC", "WindOn", "WindOff", "Solar", "FC", "SMRCCS", "ATRCCS", "BGCCS", "WE"
]

# ۱. بارگذاری داده‌ها
df = pd.read_csv('your_file.csv') 
import numpy as np

bad_rows = df[df['Generation'].isna() | np.isinf(df['Generation'])]
print(bad_rows)
# تمیز کردن ستون ساعت
df['h'] = df['h'].replace({'h': ''}, regex=True).astype(int)

# ۲. فیلتر کردن داده‌ها
filtered_df = df[ 
    (df['t'] == 4) & 
    (df['c'] == 'c1')
]

# ۳. ایجاد Pivot Table
# استفاده از pivot_table برای جمع زدن مقادیر بر اساس تکنولوژی (j) و ساعت (h)
pivot_df = filtered_df.pivot_table(
    index='h', 
    columns='j', 
    values='Generation', 
    aggfunc='sum'
).reset_index()

# ۴. اطمینان از وجود تمام ستون‌های لیست در دیتای نهایی
# اگر تکنولوژی در داده‌ها نباشد، ستون آن با مقدار 0 ایجاد می‌شود تا در نمودار خطا ندهد
for tech in desired_order:
    if tech not in pivot_df.columns:
        pivot_df[tech] = 0

# ۵. مرتب‌سازی ستون‌ها بر اساس لیست دلخواه (به علاوه ستون h)
pivot_df = pivot_df[['h'] + desired_order]

# ۶. مرتب‌سازی سطرها بر اساس ساعت
pivot_df = pivot_df.sort_values(by='h')

# ۷. ایجاد ستون h_label برای نمایش در نمودار
#pivot_df['h_label'] = 'h' + pivot_df['h'].astype(str)

# ۸. ذخیره فایل اکسل نهایی
pivot_df.to_excel('processed_data_WithoutDC.xlsx', index=False)

print("فایل اکسل با ترتیب ستون‌های درخواستی ایجاد شد.")