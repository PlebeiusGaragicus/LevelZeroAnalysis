import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the CSV file into a pandas DataFrame
def load_data(file_path):
    return pd.read_csv(file_path)

# Convert necessary columns to datetime format
def convert_to_datetime(df):
    df['incidentDate'] = pd.to_datetime(df['incidentDate'])
    df['dispatch'] = pd.to_datetime(df['dispatch'])
    df['cleared'] = pd.to_datetime(df['cleared'])
    return df

# Function to plot the timeline for a given unit
def plot_unit_timeline(ax, unit_data, unit_name, start_time, end_time):
    last_cleared_time = start_time
    unit_data = unit_data.sort_values(by="dispatch")
    for _, row in unit_data.iterrows():
        start_green = max(last_cleared_time, start_time)
        end_green = min(row['dispatch'], end_time)
        ax.barh(unit_name, (end_green - start_green).total_seconds() / 3600, left=start_green, color='green')
        
        start_red = max(row['dispatch'], start_time)
        end_red = min(row['cleared'], end_time)
        ax.barh(unit_name, (end_red - start_red).total_seconds() / 3600, left=start_red, color='red')
        
        last_cleared_time = row['cleared']

    if last_cleared_time < end_time:
        ax.barh(unit_name, (end_time - last_cleared_time).total_seconds() / 3600, left=last_cleared_time, color='green')

# Main function to visualize the timeline
def visualize_timeline(file_path, units: list, date: str, start_time: str = '00:00:00', end_time: str = '23:59:59'):
    # Load and preprocess data
    data = load_data(file_path)
    data = convert_to_datetime(data)
    
    # Filter data for the date 2023-09-12 and units PSR1 and PSR3, and drop entries without a cleared time
    filtered_activity = data[
        (data['incidentDate'].dt.date == pd.to_datetime(date).date()) & 
        (data['unit'].isin(units))
    ].dropna(subset=['cleared'])

    # Set the start and end times for the visualization
    start_time = pd.Timestamp(f'{date} {start_time}')
    end_time = pd.Timestamp(f'{date} {end_time}')

    # Initialize the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot timelines for PSR1 and PSR3 using the filtered data
    for unit in units:
        plot_unit_timeline(ax, filtered_activity[filtered_activity['unit'] == unit], unit, start_time, end_time)
    # plot_unit_timeline(ax, filtered_activity[filtered_activity['unit'] == 'PSR1'], 'PSR1', start_time, end_time)
    # plot_unit_timeline(ax, filtered_activity[filtered_activity['unit'] == 'PSR3'], 'PSR3', start_time, end_time)

    # Set title and format the x-axis
    ax.set_title(f"Activity Timeline on {date} ({start_time} - {end_time})")
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim(start_time, end_time)
    ax.set_xlabel("Time")
    plt.xticks(rotation=45)

    # Show the plot
    # plt.tight_layout()
    # plt.show()
    plt.savefig(f"./Timeline {date}", bbox_inches='tight', dpi=300)




# visualize_timeline("/Users/myca/My Drive/DATA/INTTERRA/condensed-large.csv", ['E19', 'E11', 'E1', 'E3', 'T3'], '2023-06-11')
visualize_timeline("/Users/myca/My Drive/DATA/INTTERRA/condensed-large.csv", ['M304', 'M309', 'M306', 'M311', 'M329', 'M348'], '2021-06-11')
