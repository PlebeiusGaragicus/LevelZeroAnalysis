import logging

from pipeline.logger import setup_logging
log = logging.getLogger()

from pipeline.main import main


if __name__ == "__main__":
    setup_logging()
    try:
        main()
    except KeyboardInterrupt:
        log.info("Shutting down...")
        exit(0)











# # TODO: documentation: https://docs.taipy.io/en/latest/

# from taipy import Gui, Config
# import pandas as pd

# # Existing code to load and process data...

# # Set up Taipy GUI to display the DataFrame in a nice table
# def display_table(df):
#     return df

# # Create a Taipy configuration for the GUI
# Config.configure_gui(page_title="Data Analysis Dashboard")

# # Create a Taipy GUI
# gui = Gui(page=display_table(data))

# # Run the GUI
# gui.run()