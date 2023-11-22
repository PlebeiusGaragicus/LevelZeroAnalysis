import os
import logging
log = logging.getLogger()

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def load_validate(file, delimiter):
    """
    This function both loads
    """
    data = pd.read_csv(file, delimiter=delimiter, encoding='utf-8', encoding_errors='replace')

    # truncate miliseconds in "Activity Date" column (eg. 2023-11-01 00:07:16.553600 to 2023-11-01 00:07:16)
    data['Activity Date'] = data['Activity Date'].astype(str).str[:-5]
    data['Activity Date'] = pd.to_datetime(data['Activity Date'])

    data['Apparatus ID'] = data['Apparatus ID'].astype(str)
    data['Apparatus Status'] = data['Apparatus Status'].astype(str)
    data['Activity Code'] = data['Activity Code'].astype(str)
    data['Call Number'] = data['Call Number'].astype('Int64')
    data['Call Type'] = data['Call Type'].astype(str)
    data['Remarks'] = data['Remarks'].astype(str)


    st.divider()
    st.write("### :ok: dataset loaded")
    st.caption(f"Loaded {len(data):,} rows and {len(data.columns)} columns")
    with st.expander("Click to show truncated data header"):
        st.write(data.head(n=20))

    # st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:') # TODO

    return data



#
#
#
#
def page():
    """ This is the page code and entry-point for this module """
    st.write("# Fire Crew on-scene wait times")

    with st.expander("Instructions"):
        st.write("place holder...")

    uploaded_file = None
    options = None

    upload_col, opts_col = st.columns((1,1))
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




#
#
#
#
def process_data(uploaded_file, wait_time, delimiter):

    if uploaded_file is not None:
        data = load_validate(uploaded_file, delimiter)
    else:
        st.warning('No file uploaded!', icon="⚠️")
        return

    st.divider()
    with st.expander("### :technologist: cleaning data"):
        st.write("place holder...")
