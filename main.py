import gspread
import pandas as pd
from datetime import datetime
from scripts.load_data import load_data, save_sheet, load_sheets_csv, drop_unnamed_columns
from scripts.clean_sheets_leads import clean_sheets_leads
from scripts.clean_sheets_metadata import clean_sheets_metadata
from scripts.push_data import push_data

def main():
    '''
    1. Establishes client name and start date, which are used to determine the
    Google Sheet to pull data from and the date parameters to establish 'Round'
    (week) columns.
    2. Loads the data (dictionary of the form {<sheet_name>_df, data_values_for_sheet})
    and spreadsheet with gspread.
    3. Unpacks the data and cleans its leads based on criteria specific to the
    client. The original Google Sheets lead data is from a schedulled hubspot
    pull.
    4. Cleans the metadata, adding a 'Round' column to allow for data segmentation
    by week in Looker Studio. The original Google Sheets metadata is from a
    schedulled supermetrics pull from each respective platform.
    5. Pushes the updated data to the original Google Sheet.
    _________

    Arguments
    _________
    None

    Returns
    _________
    None
    '''
    # Establish client name and cutoff date (for cleaning outliers)
    client = 'tovuti'                   # Replace with intended client
    start_date = datetime(2024, 6, 16)  # Replace with sprint start_date

    # Load the data and spreadsheet
    data, ss = load_data(client)

    # Save the sheets to data
    save_sheet(data)

    # Load the sheets (for testing purposes / to avoid redunant pulls)
    data = load_sheets_csv()

    # Drop the index if it exists
    drop_unnamed_columns(data)

    # Clean the leads related sheets create vars for flagged and leadDataClean_df
    leadDataClean_df, flagged_df = clean_sheets_leads(data, start_date)

    # Clean the metadata related sheets
    metadataFacebook_df, metadataGoogle_df, metadataLI_df = clean_sheets_metadata(data)

    # Establish sheets to push to Google Sheets
    sheets = {
        'leadDataClean_df': leadDataClean_df,
        'flagged_df': flagged_df,
        'metadataFacebook_df': metadataFacebook_df,
        'metadataGoogle_df': metadataGoogle_df,
        'metadataLI_df': metadataLI_df
    }

    # Final pass to clean sheets
    drop_unnamed_columns(sheets)

    print(sheets)
    push_data(sheets, ss)

main()
