import os
import logging
log = logging.getLogger()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import streamlit as st


EXPLANATION = """

## :mag: About

This tool can be used to analyse CAD apparatus status updates in order to determine how long fire crews wait on-scene before AMR transport units arrive.

## :bulb: Why

In this re-make of the "On-Scene Wait Times" tool, we will be collating incident responces ourselves using raw remote CAD data instead of using Intterra-exported data.  This approach will allow us to reduce reliance on external tools and establish a more robust data pipeline.

## :wrench: How it works

Remote CAD exports data with columns in this order:

    Activity Date
    Activity Type
    Apparatus Status
    Activity Code
    Remarks
    Apparatus ID
    Station Jurisdiction
    Station
    Call Jurisdiction
    Call Number
    Call Date
    Call Type
    Call priority
    Updated by Operator Jurisdiction
    Updated by Operator Code
    Updated by Desk ID

When we load the datafile, we ensure necessary columns exist and are of the correct data type.

    load_validate(file, delimiter)

Next, we clean the data by removing rows that are not relevant to the analysis.

:warning: R31 and E31 are cross-staffed between agencies, but have inconsidtent/non-matching 'Station Jurisdiction' values depending on the day.  This is a problem and will sway results slightly.

"""



##############################################################################
#
#
#
#
def page():
    """
        This is the page code and entry-point for this module.
    """
    st.write("# Fire Crew on-scene wait times")

    with st.expander("Explanation"):
        st.write(EXPLANATION)

    # uploaded_file = None
    # wait_time = None

    upload_col, opts_col = st.columns( 2 )
    with upload_col:
        uploaded_file = st.file_uploader("Choose a file")

    with opts_col:
        wait_time = st.selectbox('Wait time (minutes)', ["0.1", '2', '5', '12'], index=3)
        delimiter = st.selectbox('Delimiter', ['comma', 'tab', 'space'], index=1)
        if delimiter == 'comma':
            delimiter = ','
        elif delimiter == 'tab':
            delimiter = '\t'
        elif delimiter == 'space':
            delimiter = ' '

    st.divider()
    process_data_action = st.button("Process data :point_left:")

    if process_data_action:
        process_data(uploaded_file, wait_time, delimiter)


##############################################################################
#
#
#
#
def process_data(uploaded_file, wait_time, delimiter):
    """
    This function processes the data and displays the results.

    Args:
        uploaded_file (str): The file uploaded by the user.
        wait_time (int): The wait time in minutes.
        delimiter (str): The delimiter used in the file.
    """

    if uploaded_file is not None:
        data = load_validate(uploaded_file, delimiter)
    else:
        st.warning('No file uploaded!', icon="⚠️")
        return

    # st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:') # TODO
    # with st.expander("### :technologist: cleaning data"):
        # st.write("place holder...")
    
    data = drop_and_arrange(data)

    incident_resp = create_incident_responses(data)

    late_arrivals = incident_resp[incident_resp["MD OS"] > incident_resp["RP OS"] + pd.Timedelta(minutes=int(wait_time))]
    st.write(f"### :fire_engine: {len(late_arrivals):,} late arrivals")

    incident_resp = calculate_wait_times(incident_resp, int(wait_time))



##############################################################################
#
#
#
#
def load_validate(file, delimiter):
    """
    Load and validate the data from a CSV file.

    Args:
        file (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file.

    Returns:
        pandas.DataFrame: The loaded and validated data.

    Raises:
        KeyError: If the file does not have the expected column names.
    """

    data = pd.read_csv(file, delimiter=delimiter, encoding='utf-8', encoding_errors='replace')

    try:
        #NOTE: truncate miliseconds in "Activity Date" column (eg. 2023-11-01 00:07:16.553600 to 2023-11-01 00:07:16)
        data['Activity Date'] = data['Activity Date'].astype(str).str[:-5]
        data['Activity Date'] = pd.to_datetime(data['Activity Date'])

        data['Apparatus ID'] = data['Apparatus ID'].astype(str)
        data['Apparatus Status'] = data['Apparatus Status'].astype(str)
        data['Activity Code'] = data['Activity Code'].astype(str)
        data['Call Number'] = data['Call Number'].astype('Int64')
        data['Call Type'] = data['Call Type'].astype(str)
        data['Remarks'] = data['Remarks'].astype(str)
    except KeyError as e:
        st.error("The file you uploaded does not have the expected column names. Please check the file and try again.")
        st.warning(f"KeyError: {e}")
        st.stop()
        return

    st.divider()
    st.write("### dataset loaded :ok:")
    st.caption(f"Loaded {len(data):,} rows and {len(data.columns)} columns")
    with st.expander("Click to show truncated header of loaded data"):
        st.write(data.head())

    return data



##############################################################################
#
#
#
#
def drop_and_arrange(df: pd.DataFrame) -> pd.DataFrame:

    # NOTE: In order to keep the code clean, we will use a "with" statement on the whole section in order to keep data manipulation steps together with explanation text.
    with st.expander("Show cleaned data"):
        st.write(":arrow_forward: Rows with Activity Type: M, C, L, S are dropped")
        df = df[df["Activity Type"] != "M"] # messages
        df = df[df["Activity Type"] != "C"] # more messages?
        df = df[df["Activity Type"] != "L"] # LOGOFF remarks (duplicative - use #TODO for actual logoff tracking)
        df = df[df["Activity Type"] != "S"] # "signal" (eg. AUTO RADIO ALERTED PERSONNEL: MD208515 -  (22824))


        st.write(":arrow_forward: Only keep 'RP' and 'MD' rows")
        # keep rows with "Station Jurisdiction" == "RP" or "MD"
        df = df[df["Station Jurisdiction"].isin(["RP", "MD"])]

        st.write(":arrow_forward: Drop BLS units and CHD units")
        df = df[df["Station"] != "715B"]
        df = df[df["Station"] != "CHD"]

        st.write(":arrow_forward: Create an 'Incident Number' column from 'Call Jurisdiction' and 'Call Number' columns")
        # incident number column should combine "Call Jurisdiction" and "Call Number" columns and ensure call number has leading zeros to make it 8 digits
        df["Call Number"] = df["Call Number"].astype(str).str.zfill(8)
        df["Incident Number"] = df["Call Jurisdiction"] + df["Call Number"]
        # df = df.drop(columns=["Call Jurisdiction", "Call Number"])

        st.write(":arrow_forward: Drop un-needed columns and rearrange remaining columns")
        df = df[[
            "Activity Date",
            "Incident Number",
            "Apparatus ID",
            "Apparatus Status",
            "Activity Code",
            "Call Type",
            "Station Jurisdiction",
            "Remarks",
            "Call Jurisdiction",
            "Call Number"
        ]]


        st.write(":arrow_forward: Sort by 'Activity Date' column")
        # sort by 'Activity Date' column
        df = df.sort_values(by=['Activity Date'])

        st.write(":arrow_forward: Reset the index")
        # reset index
        df = df.reset_index(drop=True)

        # st.write(df.head(n=20))
        st.write(df)

        # st.stop()

    return df


def create_incident_responses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a dataframe of incident responses.

    Args:
        df (pandas.DataFrame): The dataframe to create incident responses from.

    Returns:
        pandas.DataFrame: The incident responses.
    """

    # Creating a pivot table with 'Incident Number' as index and combinations of 'Station Jurisdiction' and 'Apparatus Status' as columns
    pivot_columns = df['Station Jurisdiction'] + ' ' + df['Apparatus Status']
    pivot_table = df.pivot_table(index='Incident Number',
                                    columns=pivot_columns,
                                    values='Activity Date',
                                    aggfunc='min')

    # Resetting index to make 'Incident Number' a column and renaming the columns for clarity
    pivot_table.reset_index(inplace=True)
    pivot_table.columns.name = None  # Remove the name of the columns level

    # Filtering for the specified columns
    # filtered_columns = ['Incident Number', 'RP DP', 'RP ER', 'RP OS', 'RP AV', 'MD DP', 'MD ER', 'MD OS']
    filtered_columns = ['Incident Number', 'RP DP', 'RP ER', 'RP OS', 'MD DP', 'MD ER', 'MD OS']
    final_incident_response_df = pivot_table[filtered_columns]

    # Filtering the dataframe to include only those rows with at least one RP and one MD response
    # rp_columns = ['RP DP', 'RP ER', 'RP OS', 'RP AV']
    rp_columns = ['RP DP', 'RP ER', 'RP OS']
    md_columns = ['MD DP', 'MD ER', 'MD OS']

    # Applying the filter
    filtered_incident_df = final_incident_response_df.dropna(subset=rp_columns, how='all').dropna(subset=md_columns, how='all')

    #  df[df["Activity Type"] != "S"]
    # filtered_incident_df = filtered_incident_df[ filtered_incident_df['Incident Number'] != ' 0000<NA>']


    # drop rows with "RP OS" or "MD OS" values are blank (This is when they clear before arrival on scene)
    filtered_incident_df = filtered_incident_df[filtered_incident_df["RP OS"].notna()]
    filtered_incident_df = filtered_incident_df[filtered_incident_df["MD OS"].notna()]

    # if "RP OS" is after "MD OS" then drop the row
    filtered_incident_df = filtered_incident_df[filtered_incident_df["RP OS"] < filtered_incident_df["MD OS"]]

    filtered_incident_df.reset_index(drop=True, inplace=True)

    with st.expander("Show final incident response dataframe"):
        st.write("Creating a 'pivot table' to collate incident responces...")
        st.write("Dropping rows where either RP or MD cleared prior to arrival...") # TODO - what if we waited on scene for 12 minutes and then CLEARED THE AMUBLANCE?
        st.write("Dropping rows where RP arrived AFTER MD...")
        st.write(filtered_incident_df)

    return filtered_incident_df



def calculate_wait_times(df: pd.DataFrame, wait_time: int) -> pd.DataFrame:

    # add a row called "Wait Time" that is the difference between "MD OS" and "RP OS"
    df["Wait Time"] = pd.to_datetime(df["MD OS"]) - pd.to_datetime(df["RP OS"])

    # convert the "Wait Time" column to seconds
    df["Wait Time"] = df["Wait Time"].dt.total_seconds()

    # drop rows with a wait time less than wait_time seconds
    df = df[df["Wait Time"] >= wait_time * 60]

    # convert "Wait Time" column to minutes and round to 1 decimal place
    df["Wait Time"] = (df["Wait Time"] / 60).round(1)

    df = df[[
        "Incident Number",
        "RP OS",
        "MD OS",
        "Wait Time"
    ]]

    # reset index
    df.reset_index(drop=True, inplace=True)

    with st.expander("Show final dataframe with wait times"):
        st.write("Adding a 'Wait Time' column that is the difference between 'MD OS' and 'RP OS'...")
        st.write(f"### :fire_engine: {len(df):,} late arrivals")
        st.write(df)

    return df










prompts = """
I need to take this datafile of 911 system apparatus status updates, and convert it into a dataframe of "incident responses."

Each row in the incident response dataframe should have a unique incident number as well as the earliest timestamp for each "Station Jurisdictions" status.

RP = portland fire apparatus
MD = AMR ALS ambulance

DP - dispatched
ER - en route
OS - on scene
OG - staged nearby (consider same as on scene)
TR - transporting ( ambulance only )
TC - transport complete (at hospital)
AV - available in service (call cleared)
IQ - in quarters (at station, available for calls)

---

The resulting dataframe should have columns of "call number" "RP DP" "RP ER" "RP OS" "RP AV" "MD DP" "MD ER" "MD OS"

Each row should have a unique call number.  As in, each status update should be summarized into a single row representing a single call in its entirety

---

This looks great so far.  Let's add it to by removing every call number row where there is no RP response or no MD response.  In other words, I only want to show rows that include BOTH RP and MD units.
"""



example_calls = """

118432 - orig dispatched as a gresham call, but E31 eventually added.  Therefore, no dispatch time.

117662 - no ER time for PFR - why?  They didn't push En Route on MDT

RP00116255 - No DP or ER times, apparently E1 was on-scene already and just requested an ambulance?

RP00118513 - E18 went from OS to IQ.  They didn't clear from call, they drove while OS to the station.

RP00118093 - E17 had a FF go with AMR and drove to EM while in OS status.

"""