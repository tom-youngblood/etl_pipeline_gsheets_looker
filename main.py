import gspread
import pandas as pd
from datetime import datetime
from scripts.load_data import load_data
from scripts.clean_sheets_leads import clean_sheets_leads
from scripts.clean_sheets_metadata import clean_sheets_metadata

def main():

    # Establish client name and cutoff date (for cleaning outliers)
    client = 'tovuti'                   # Replace with intended client
    start_date = datetime(2024, 6, 16)  # Replace with sprint start_date

    # Load the data
    data = load_data(client)

    # Clean the leads related sheets create vars for flagged and leadDataClean_df
    flagged_df, leadDataClean_df = clean_sheets_leads(data, start_date)

    # Clean the metadata related sheets;
    clean_sheets_metadata(data)

    

main()
