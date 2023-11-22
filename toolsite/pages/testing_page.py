import streamlit as st

def page():
    st.write("# Testing purposes only")

    st.warning('This is a warning', icon="⚠️")
    # with st.spinner('Wait for it...'):
    #     time.sleep(5)

    import time
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.02)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
