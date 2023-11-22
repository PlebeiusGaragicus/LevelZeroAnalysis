import os
import logging

from pipeline import logger
logger.setup_logging()
log = logging.getLogger()

import dotenv
dotenv.load_dotenv()

import streamlit as st


class Pages:
    TESTING_PAGE = "Testing Page"
    AMR_SYSTEM_LEVELS = "AMR system levels"
    ON_SCENE_WAIT_TIMES = "on-scene wait times"
    UNIT_HOUR_UTILIZATION = "Unit Hour Utilization"



def main():
    logging.getLogger("fsevents").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)

    with st.sidebar:
        st.title("Portland Fire and Rescue Data Analysis Tools")

        page = st.selectbox("What data do you want to analyze? :point_down:",
                    (
                        'Select a tool',
                        Pages.AMR_SYSTEM_LEVELS,
                        Pages.ON_SCENE_WAIT_TIMES,
                        Pages.UNIT_HOUR_UTILIZATION,
                    ),
                    index=2 # TODO: Comment out in production... otherwise set to tool you're working on
                    )

    if page == Pages.AMR_SYSTEM_LEVELS:
        from toolsite.pages.amr_system_levels import page as amr_system_levels
        amr_system_levels()
    elif page == Pages.ON_SCENE_WAIT_TIMES:
        from toolsite.pages.on_scene_wait_times import page as on_scene_wait_times
        on_scene_wait_times()
    elif page == Pages.UNIT_HOUR_UTILIZATION:
        from toolsite.pages.unit_hour_utilization import page as unit_hour_utilization
        unit_hour_utilization()
    else:
        info_page() #TODO



def info_page():
    st.markdown("# Welcome to your personal Data Analysis Suite")
    st.write("Select an Analysis method from the sidebar on the left.")

    image_column, text_column = st.columns ( (1, 2) )

    with image_column:
        st.image("https://picsum.photos/200")
    
    with text_column:
        st.write("This is a column of text")



############## DEBUG TESTING ONLY ##############
    if not os.getenv("DEBUG", False):
        return

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

    st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:') # TODO
