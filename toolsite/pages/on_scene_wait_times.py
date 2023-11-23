import os
import logging
log = logging.getLogger()

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    df = df[df["Activity Type"] != "M"] # messages
    df = df[df["Activity Type"] != "C"] # more messages?
    df = df[df["Activity Type"] != "L"] # LOGOFF remarks (duplicative - use #TODO for actual logoff tracking)
    df = df[df["Activity Type"] != "S"] # "signal" (eg. AUTO RADIO ALERTED PERSONNEL: MD208515 -  (22824))

    # with st.expander("Rows with Activity Type: M, C, L, S are dropped"):
        # st.write(df.head(n=20))

    #NOTE: this step works to both re-arrange AND drop columns not listed
    df = df[[
        "Activity Date",
        "Apparatus ID",
        "Apparatus Status",
        "Activity Code",
        "Call Number",
        "Call Type",
        "Remarks"
    ]]

    # sort by 'Activity Date' column
    df = df.sort_values(by=['Activity Date'])

    # reset index
    df = df.reset_index(drop=True)

    with st.expander("Show cleaned data"):
        st.write(":arrow_forward: Rows with Activity Type: M, C, L, S are dropped")
        st.write(":arrow_forward: Dropping un-needed columns and re-arranging the rest")
        # st.write(df.head(n=20))
        # st.write(df.head())
        st.write(df)

    return df
