import logging
log = logging.getLogger()

import pandas as pd
import numpy as np

from pipeline.config import *


def load_data(path: str, filename: str) -> pd.DataFrame:
    full_path = f"{path}/{filename}.csv"
    log.debug("loading dataset: %s", full_path)

    data = pd.read_csv(full_path, parse_dates=['incidentDate', 'alarm', 'dispatch', 'enroute', 'arrival', 'enrouteFacility', 'cleared'])
    # data['arrival'] = pd.to_datetime(data['arrival'])

    log.debug(data.head())

    return data



# def filter_out_incidents_without_amr(data: pd.DataFrame) -> pd.DataFrame:
#     # Check for rows where the 'agency' is AMR and there is a dispatch time
#     has_amr_dispatched = data['juris4'].str.contains('AMR') & data['dispatch'].notnull()
    
#     # Keep only incidents where an AMR was dispatched
#     return data[has_amr_dispatched.groupby(data['incident']).transform('any')]


def filter_out_incidents_without_amr(data: pd.DataFrame) -> pd.DataFrame:
    # Check for rows where the 'agency' is AMR and there is a dispatch time
    has_amr_dispatched = data['juris4'].str.contains('AMR') & data['dispatch'].notnull()
    
    # Determine the incidents with AMR dispatched
    incidents_with_amr = has_amr_dispatched.groupby(data['incident']).transform('any')

    # Log incidents without AMR dispatch
    incidents_without_amr = data[~incidents_with_amr]
    incidents_without_amr.to_csv(f'{CURRENT_PATH}/incidents_without_amr.csv', index=False)  # Exporting to a CSV for review
    log.info(f"Logged {len(incidents_without_amr)} incidents without AMR dispatch")

    print("KEEPING THESE RECORDS GOING FORWARD:")
    print(data[incidents_with_amr])

    # Keep only incidents where an AMR was dispatched
    return data[incidents_with_amr]




def filter_out_incidents_without_pfr(data: pd.DataFrame) -> pd.DataFrame:
    # Check for rows where the 'agency' is PF&R and there is a dispatch time
    has_pfr_dispatched = data['juris4'].str.contains('PF&R') & data['dispatch'].notnull()
    
    # Determine the incidents with PF&R dispatched
    incidents_with_pfr = has_pfr_dispatched.groupby(data['incident']).transform('any')

    # Log incidents without PF&R dispatch
    incidents_without_pfr = data[~incidents_with_pfr]
    incidents_without_pfr.to_csv(f'{CURRENT_PATH}/incidents_without_pfr.csv', index=False)  # Exporting to a CSV for review
    log.info(f"Logged {len(incidents_without_pfr)} incidents without PF&R dispatch")

    print("KEEPING THESE RECORDS GOING FORWARD:")
    print(data[incidents_with_pfr])

    # Keep only incidents where PF&R was dispatched
    return data[incidents_with_pfr]



# def merge_arrivals(data: pd.DataFrame) -> pd.DataFrame:
#     # Filter AMR and PF&R data
#     amr_data = data[data['juris4'] == "AMR"]
#     pfr_data = data[data['juris4'] == "PF&R"]

#     # Group by 'incident' to find the minimum 'arrival' and take the 'incidentType' as well
#     amr_min_arrival = amr_data.groupby('incident').agg({'arrival': 'min', 'incidentType': 'first'})
#     pfr_min_arrival = pfr_data.groupby('incident').agg({'arrival': 'min', 'incidentType': 'first'})

#     # Merge the two DataFrames on the 'incident' column while keeping all columns
#     merged = pd.merge(pfr_min_arrival, amr_min_arrival, on=['incident', 'incidentType'], how='outer', suffixes=('_pfr', '_amr'))

#     # Calculate 'wait_seconds' making sure that we handle NaT values
#     merged['wait_seconds'] = (merged['arrival_amr'] - merged['arrival_pfr']).dt.total_seconds().fillna(0)
#     merged['wait_seconds'] = merged['wait_seconds'].apply(lambda x: max(0, x))

#     log.debug("MERGED ARRIVALS")
#     log.debug(merged.head())

#     return merged


def merge_arrivals(data: pd.DataFrame) -> pd.DataFrame:
    # Filter AMR and PF&R data
    amr_data = data[data['juris4'] == "AMR"]
    pfr_data = data[data['juris4'] == "PF&R"]

    # Group by 'incident' to find the minimum 'arrival' and take the 'incidentType' and 'cleared' as well
    amr_min_arrival = amr_data.groupby('incident').agg({'arrival': 'min', 'cleared': 'first', 'incidentType': 'first'})
    pfr_min_arrival = pfr_data.groupby('incident').agg({'arrival': 'min', 'cleared': 'first', 'incidentType': 'first'})

    # Merge the two DataFrames on the 'incident' column while keeping all columns
    merged = pd.merge(pfr_min_arrival, amr_min_arrival, on='incident', how='outer', suffixes=('_pfr', '_amr'))

    # Define a function to calculate wait time
    def calculate_wait_time(row):
        if pd.isna(row['arrival_pfr']) or pd.isna(row['arrival_amr']):
            # If either agency was cleared before arrival, set wait time to NaN or another placeholder
            return np.nan
        else:
            # If both agencies arrived, calculate the wait time normally
            return (row['arrival_amr'] - row['arrival_pfr']).total_seconds()

    # Calculate 'wait_seconds' for each row
    merged['wait_seconds'] = merged.apply(calculate_wait_time, axis=1)

    # Replace negative wait times with 0
    merged['wait_seconds'] = merged['wait_seconds'].apply(lambda x: max(0, x))

    log.debug("MERGED ARRIVALS")
    log.debug(merged.head())

    return merged


# def calculate_wait_times(merged: pd.DataFrame) -> pd.DataFrame:
#     merged['wait_time_minutes'] = (merged['wait_seconds'] / 60).round(1)
#     merged['year_week'] = merged['arrival_pfr'].dt.isocalendar().year.astype(str) + '-W' + \
#                           merged['arrival_pfr'].dt.isocalendar().week.astype(str).str.zfill(2)
    
#     log.debug("WAIT TIMES")
#     log.debug(merged.head())
#     return merged



def calculate_wait_times(merged: pd.DataFrame) -> pd.DataFrame:
    # Check if 'arrival_amr' is NaT and use 'cleared_amr' if that's the case
    merged['effective_amr_arrival'] = merged.apply(
        lambda row: row['cleared_amr'] if pd.isna(row['arrival_amr']) else row['arrival_amr'],
        axis=1
    )
    
    # Calculate 'wait_seconds' based on 'effective_amr_arrival' instead of 'arrival_amr'
    merged['wait_seconds'] = (merged['effective_amr_arrival'] - merged['arrival_pfr']).dt.total_seconds().fillna(0)
    merged['wait_seconds'] = merged['wait_seconds'].apply(lambda x: max(x, 0))
    
    # Calculate 'wait_time_minutes' based on updated 'wait_seconds'
    merged['wait_time_minutes'] = (merged['wait_seconds'] / 60).round(1)
    
    # Generate 'year_week' based on 'arrival_pfr'
    merged['year_week'] = merged['arrival_pfr'].dt.isocalendar().year.astype(str) + '-W' + \
                          merged['arrival_pfr'].dt.isocalendar().week.astype(str).str.zfill(2)
    
    log.debug("WAIT TIMES")
    log.debug(merged.head())
    return merged




def filter_incidents(merged: pd.DataFrame, min_wait: int) -> pd.DataFrame:
    return merged[merged['wait_time_minutes'] >= min_wait]


def incidents_by_week(merged: pd.DataFrame) -> pd.DataFrame:
    counts = merged.groupby('year_week').size()
    return counts.reset_index(name='incidents')


def export_data(df: pd.DataFrame, path: str, filename: str):
    export_path = f"{path}/{filename}"
    print(f">> exporting to: {export_path}")
    df.to_csv(export_path, index=False)


def print_analysis(merged: pd.DataFrame):
    # print(merged.columns)
    # print(merged.head())

    # total_incidents = len(merged)
    # total_unique_incidents = merged['incident'].nunique()
    # NOTE: 'incident' is not a column but the DataFrame's index. 
    total_unique_incidents = merged.index.nunique()
    # average_wait_time = merged['wait_seconds'].mean().round(1)
    average_wait_time = round(merged['wait_seconds'].mean(), 1)
    print(f"Total Incidents: {total_unique_incidents}")
    print(f"Average Wait Time: {average_wait_time} seconds")



def main():
    pd.set_option('display.max_rows', DISPLAY_MAX_ROWS)
    data = load_data(CURRENT_PATH, DATASET_FILENAME)

    # Filter out incidents without any AMR unit dispatched
    data_with_amr = filter_out_incidents_without_amr(data)

    data_with_amr = filter_out_incidents_without_amr(data)
    data_with_amr_and_pfr = filter_out_incidents_without_pfr(data_with_amr)

    merged_arrivals = merge_arrivals(data_with_amr_and_pfr)
    wait_times = calculate_wait_times(merged_arrivals)

    for min_wait in [1, 5, 10, 15]:
        incidents = filter_incidents(wait_times, min_wait)
        export_data(incidents, CURRENT_PATH, f"export_wait_times_{min_wait}_min.csv")

    weekly_incidents = incidents_by_week(wait_times)
    export_data(weekly_incidents, CURRENT_PATH, "export_incidents_by_week.csv")
    print_analysis(merged_arrivals)