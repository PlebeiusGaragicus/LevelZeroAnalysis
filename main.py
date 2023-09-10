import pandas as pd

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('/Users/myca/Downloads/Unit Response Performance_09-01-2023-09-09-2023.csv')

# Display the first few rows of the dataset
# data.head()

# Convert 'arrival' column to datetime format for calculations
data['arrival'] = pd.to_datetime(data['arrival'])

# Filter out records corresponding to "AMR" and "PF&R"
amr_data = data[data['dispatchStation'] == "AMR"]
pfr_data = data[data['dispatchStation'].str.startswith("PF&R")]

# Group by 'incident' and get the earliest arrival time for each group
amr_min_arrival = amr_data.groupby('incident')['arrival'].min()
pfr_min_arrival = pfr_data.groupby('incident')['arrival'].min()

# Merge the two series on 'incident'
merged_arrivals = pd.concat([pfr_min_arrival, amr_min_arrival], axis=1, keys=['pfr_arrival', 'amr_arrival'])

# Calculate wait time for each incident
merged_arrivals['wait_time'] = (merged_arrivals['amr_arrival'] - merged_arrivals['pfr_arrival']).dt.total_seconds()
# If AMR arrived before PF&R or at the same time, set wait time to 0
merged_arrivals['wait_time'] = merged_arrivals['wait_time'].apply(lambda x: max(0, x))

# Filter out incidents where wait time is less than 600 seconds
# filtered_data = merged_arrivals[merged_arrivals['wait_time'] >= 600]
filtered_data = merged_arrivals[merged_arrivals['wait_time'] >= 600].copy()


# filtered_data['wait_time_minutes'] = filtered_data['wait_time'] / 60
# filtered_data['wait_time_minutes'] = filtered_data['wait_time_minutes'].round(1)
filtered_data.loc[:, 'wait_time_minutes'] = filtered_data['wait_time'] / 60
filtered_data.loc[:, 'wait_time_minutes'] = filtered_data['wait_time_minutes'].round(1)


# Drop the original 'wait_time' column in seconds
filtered_data = filtered_data.drop(columns=['wait_time'])


pd.set_option('display.max_rows', None)
print( filtered_data )

file_path = "./filtered_911_data.csv"
filtered_data.to_csv(file_path)


# Calculate statistics for wait times
# average_wait_time = merged_arrivals['wait_time'].mean()
# median_wait_time = merged_arrivals['wait_time'].median()
# max_wait_time = merged_arrivals['wait_time'].max()
# min_wait_time = merged_arrivals['wait_time'].min()
# total_incidents = len(merged_arrivals)

total_over_10 = len(filtered_data)

print( f"{total_over_10=}" )
