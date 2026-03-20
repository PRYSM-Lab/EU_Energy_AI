#%%
import pandas as pd
import numpy as np
from numpy import unravel_index
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
from scipy.stats import gaussian_kde
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


# Load the data
data = pd.read_csv('NewDataEurope.csv') 
yeardays = 365
num_rows = len(data)

# Generate a datetime range that matches the number of rows in your data
date_range = pd.date_range(start='2018-01-01 00:00:00', periods=num_rows, freq='60min')


# Create a copy of the original data and add the datetime index
df = data.copy()
df['datetime'] = date_range
df = df.set_index('datetime')

# Display the first few rows to confirm
print(df.head())
print(df.tail())


#%%


# find peak electricity and gas day(s)
def find_peak_day(data, column):
    """
    Find the index of the peak day for a given column.
    """
    peak_day_index = df[column].idxmax()
    return peak_day_index

def find_peak_day_for_gas(data, gas_columns):
    """
    Find the index of the peak day for gas usage given a list of gas columns.
    """
    peak_day_index = df[gas_columns].sum(axis=1).idxmax()
    return peak_day_index

def find_peak_day_for_multiple_gas_types(data, demand_country):
    """
    Find the peak day index for multiple types of gas (Domestic, Services, Industrial).
    """
    peak_days = {}
    for demand_country, columns in demand_country.items():
        peak_days[demand_country] = find_peak_day_for_gas(df, columns)
    return peak_days

def remove_peak_day(data, peak_day_index):
    """
    Remove rows for the peak day from the DataFrame.
    """
    df_nopeak = df.copy()
    peak_date = peak_day_index.date()
    df_nopeak = df_nopeak.loc[df_nopeak.index.date != peak_date]
    return df_nopeak


# Define the columns for different gas types
demand_country_cols = ['AL',	'AT',	'BE',	'BA',	'BG',
                       'CZ',	'DK',	'EE',	'FI',	'FR',	'DE',
                      'HU'	,'IE',	'IT',	'LV',	'LT',	'LU',	
                      'ME'	,'NL',	'MK',	'NO',	'PL',	'PT',	'RO',
                      'SI',	'SK',	'ES'	,'SE'	,'CH'	,'UK'
]


# Find the peak day for electricity
electricity_peak_day = find_peak_day(data, 'Elec')
print('Electricity peak day index =', electricity_peak_day)

# Find the peak day for gas types
demand_country = {
    'demand_country': demand_country_cols

}

peak_days = find_peak_day_for_multiple_gas_types(df, demand_country)
for demand_country, peak_day in peak_days.items():
    print(f'{demand_country} peak day index =', peak_day)

# Remove the peak day from the DataFrame
df_nopeak = remove_peak_day(data, electricity_peak_day)




# take only one peak day out from clustering-electricity peak day

def find_peak_date(df, column):
    """
    Find the date of the peak value for a given column.
    """
    peak_datetime = pd.to_datetime(df[column].idxmax())
    peak_date = peak_datetime.date()
    return peak_date

# Assuming df is your DataFrame and 'Elec' is the column name
electricity_peak_date = find_peak_date(df, 'Elec')
print('Electricity peak date =', electricity_peak_date)

#%%


# Reshape each column of the DataFrame into a (yeardays, 24) array (days x 24 hours)
days = [data[col].values.reshape(yeardays, 24) for col in data]


# Find the index of the peak electricity day
peakELEC = unravel_index(data['Elec'].values.reshape(yeardays, 24).argmax(), 
                         data['Elec'].values.reshape(yeardays, 24).shape)[0]

# Remove the peak electricity day from the dataset
DaysNoPeak = np.delete(days, peakELEC, axis=1)

# Find the maximum non-peak day value for each attribute
DaysMax = [DaysNoPeak[i].max() for i in range(len(days))]

# Normalize the attributes for all remaining days (0, 1)
DaysNormalised = [DaysNoPeak[i] / DaysMax[i] for i in range(len(DaysNoPeak))]

# Output the number of days in the DaysNoPeak/DaysNormalised array
print('# of days in DaysNoPeak/DaysNormalised =', len(DaysNormalised[0]))






#Array with rows each day and columns each hour of each attribute (yeardays, 24*70)
def concatenate_normalized_days(DaysNormalised):
    
    return np.concatenate(DaysNormalised, axis=1)

def concatenate_days(days):
    
    return np.concatenate(days, axis=1)
# Assuming 'days' and 'days_normalized' are already defined
# Concatenate normalized days
data_new = concatenate_normalized_days(DaysNormalised)

# Concatenate non-normalized days
days_new = concatenate_days(days)

# Output the shapes of the concatenated arrays
print('data_new shape:', data_new.shape)
print('days_new shape:', days_new.shape)





#%%

# set number of clusters
# Calling the Kmeans Clustering 

n_clusters = int(input("Press Input number of cluster: ")) 

def run_kmeans_clustering(data, n_clusters=n_clusters, max_iter=2000, random_state=40):
    """
    Run KMeans clustering on the given data.
    """
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=max_iter, random_state=random_state).fit(data)
    centroids = kmeans.cluster_centers_
    print('inertia=', kmeans.inertia_)  # Print inertia
    return kmeans, centroids

def count_days_in_clusters(kmeans):
    """
    Count the number of days in each cluster using KMeans labels.
    """
    nDays = Counter(kmeans.labels_)
    return sorted(nDays.items())  # Sort the days by cluster label

def get_days_per_cluster(kmeans):
    """
    Get the days (indices) that belong to each cluster.
    """
    return {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}

def calculate_cluster_weights(nDays):
    """
    Calculate the weights for each cluster based on the number of days.
    """
    weights = [nDays[v][1] for v in range(len(nDays))]
    return weights

def extract_daily_centroids(centroids, days_no_peak_length):
    """
    Extract daily centroids from the full centroid array. """
    return [centroids[:, i*24:24*(1+i)] for i in range(days_no_peak_length)]



# Run KMeans clustering
kmeans, centroids = run_kmeans_clustering(data_new)

#  Count the number of days in each cluster
nDays = count_days_in_clusters(kmeans)

# Get the days in each cluster
z = get_days_per_cluster(kmeans)

# Calculate the weights for each cluster
weights = calculate_cluster_weights(nDays)

# 5. Extract daily centroids
DaysCentroids = extract_daily_centroids(centroids, len(DaysNoPeak))

# Output the number of days in each cluster
print("Number of days in each cluster:", nDays)
print("Weights for each cluster:", weights)
print("Days in each cluster:", z)

#%%
#Calculate the centroids means and item means for non- peak days

def calculate_centroids_means(days_centroids, days_no_peak_length):
    
    return np.vstack([days_centroids[i].mean(axis=1) for i in range(days_no_peak_length)])

def calculate_items_mean(days_normalized, days_no_peak_length):
    
    return np.vstack([days_normalized[i].mean(axis=1) for i in range(days_no_peak_length)])


centroids_means = calculate_centroids_means(DaysCentroids, len(DaysNoPeak))
items_mean = calculate_items_mean(DaysNormalised, len(DaysNoPeak))

print(centroids_means.shape, items_mean.shape)






#Find representative days and weights

def representative_day(centroid_means, items_mean, z, n_clusters):
    """
    Find the representative day for each cluster by comparing the centroid means with the actual daily data.
    """
    rep_days = []
    
    for clu in range(n_clusters):
        # Extract the mean centroid values for the current cluster (transpose to match day-wise comparison)
        centroid_cluster = centroid_means.transpose()[clu]
        
        # Select the actual days assigned to this cluster from the items_mean array
        cluster_days_data = items_mean.transpose()[z[clu]]
        
        # Focus on gas columns (7 to 20) and calculate the difference with centroid
        gas_diff = centroid_cluster[7:20] - cluster_days_data[:, 7:20]
        
        # Find the day with the smallest positive sum of differences
        # Use np.inf for negative values to ensure they're not selected
        positive_sum_diff = np.where(gas_diff.sum(axis=1) > 0, gas_diff.sum(axis=1), np.inf)
        
        # Find the index of the day with the smallest positive difference and append to the result list
        representative_day_idx = np.argmin(positive_sum_diff)
        rep_days.append(z[clu][representative_day_idx])
    
    return rep_days

rep_days = representative_day(centroids_means, items_mean, z, n_clusters)

# Output the representative days
print("Representative days for each cluster:", rep_days)
print("Weights for each cluster:", weights)






# Find cluster, representative days and weights
def add_peak_day(rep_days, weights, peak_elec, n_clusters):
    """
    Add the peak electricity day to the representative days and adjust weights.
    """
    # Insert peak electricity day at the beginning of representative days list
    rep_days.insert(0, peak_elec)
    
    # Insert a weight of 1 for the peak electricity day at the beginning of weights list
    weights.insert(0, 1)
    
    # Create a DataFrame with cluster IDs, representative days, and weights
    clusters_df = pd.DataFrame({
        "Cluster_iD": range(n_clusters + 1),  # Including peak electricity day
        "Repres_Days": rep_days,
        "Weights": pd.Series(weights)
    })
    
    return clusters_df

clusters_df = add_peak_day(rep_days, weights, peakELEC, n_clusters)


print(clusters_df)




clusters_df["Cluster_iD"]=range(n_clusters+1)
DaysFinal= [pd.DataFrame(days_new[rep_days,i*24:24*(1+i)], 
                         index=range(len(rep_days)),columns=range(24)) for i in range(0,len(DaysNormalised))]





# Build the cluster profile
def select_representative_day(Cluster_iD, clusters_df, df, df_nopeak, peak_ids):
    """
    Select the representative day data based on cluster ID and whether it is a peak day or not.
    """
    rep_day = clusters_df.loc[clusters_df['Cluster_iD'] == Cluster_iD, 'Repres_Days'].values[0]
    if Cluster_iD in peak_ids:
        return df.iloc[rep_day * 24:(rep_day + 1) * 24]
    else:
        return df_nopeak.iloc[rep_day * 24:(rep_day + 1) * 24]

def create_clustered_profiles(clusters_df, df, df_nopeak, peak_ids, n_clusters):
    """
    Create a DataFrame with clustered profiles.
    
    """
    M_profiles = []
    
    for iD in clusters_df['Cluster_iD']:
        M_profiles.append(select_representative_day(iD, clusters_df, df, df_nopeak, peak_ids))
    
    index_tuples = list(zip(np.array([np.repeat(i, 24) for i in range(n_clusters + 1)]).ravel(),
                            np.tile(range(24), n_clusters + 1)))
    
    df_clustered_profiles = pd.DataFrame(
        index=index_tuples,
        columns=df.columns,
        data=pd.concat(M_profiles, axis=0).values
    )
    
    return df_clustered_profiles

peak_ids = [0]  # Only one peak
df_clustered_profiles = create_clustered_profiles(clusters_df, df, df_nopeak, peak_ids, n_clusters)

# Output the resulting DataFrame
print(df_clustered_profiles)








##Save the clusters profile in the new excel file
def save_to_excel(clusters_df, clustered_profiles_df, year_range, n_clusters):
    """
    Save the clusters and clustered profiles DataFrames to an Excel file.
    
    """
    # Define the file name
    file_name = f"{year_range}Cluster_{n_clusters}.xlsx"
    
    # Create an ExcelWriter object
    with pd.ExcelWriter(file_name) as writer:
        # Write the clusters DataFrame to a sheet named 'NDaysCluster'
        clusters_df.to_excel(writer, sheet_name='NDaysCluster', index=False)
        
        # Write the clustered profiles DataFrame to a sheet named 'ClusteredProfiles'
        clustered_profiles_df.to_excel(writer, sheet_name='ClusteredProfiles', index=True)
        
    print(f"Data has been saved to {file_name}")

save_to_excel(clusters_df, df_clustered_profiles, 'Cluster for EU', n_clusters)



#%%

