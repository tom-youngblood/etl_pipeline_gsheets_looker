import pandas as pd
from scripts.load_data import load_data

def clean_sheets_metadata(data):
    '''
    Cleans the metadata related sheets in the Spreadsheet.
    _________

    Arguments
    _________
    data (dictionary): Dictionary of the format {<sheet_name>_df, data_values_for_sheet}

    Returns
    _________
    Cleaned_metadata_dfs (dict): A dictionary of the cleaned metadata dataframes
    of the format {<sheet_name>_df, data_values_for_sheet}
    '''
    # Load the neccessary sheets
    metadataFacebook_df = data['metadataFacebook_df']
    metadataGoogle_df = data['metadataGoogle_df']
    metadataLI_df = data['metadataLI_df']
    settings_df = data['settings_df']

    # Trim excess hubspot scrape (conversion table) from metadataGoogle_df
    metadataGoogle_df = metadataGoogle_df.loc[:, :'Clicks'].copy()

    # Convert the dates to datetime
    metadataFacebook_df.loc[:, 'Date'] = pd.to_datetime(metadataFacebook_df['Date'], errors='coerce')
    metadataGoogle_df.loc[:, 'Date'] = pd.to_datetime(metadataGoogle_df['Date'], errors='coerce')
    metadataLI_df.loc[:, 'Date'] = pd.to_datetime(metadataLI_df['Date'], errors='coerce')
    settings_df.loc[:, 'Start'] = pd.to_datetime(settings_df['Start'], errors='coerce')
    settings_df.loc[:, 'End'] = pd.to_datetime(settings_df['End'], errors='coerce')

    # Add a round row to metadata columns
    for sheet in [metadataFacebook_df, metadataGoogle_df, metadataLI_df]:
        # If the columns does not exist
        if 'Round' not in sheet.columns:
            # Add the round column
            add_round_column(sheet, settings_df)
            # Add the round column's values
            add_round_column_values(sheet, settings_df)

def add_round_column(sheet, settings):
    '''
    Adds a round column to the given sheet based on the client's settings.
    _________

    Arguments
    _________
    sheet (pd.DataFrame): DataFrame containing the sheet to operate on
    settings (pd.DataFrame): DataFrame containing start and end dates for rounds.

    Returns
    _________
    None
    '''
    # Insert the column, 'Round', at the beggining of the sheet
    sheet.insert(0, 'Round', '')

    # Set start date
    start_date = settings.iloc[0]['Start']

    return None

def add_round_column_values(sheet, settings):
    '''
    Adds the correct round values to the round column of the sheet. Round column
    values are based on dates in the 'settings' sheet.
    _________

    Arguments
    _________
    sheet (pd.DataFrame): DataFrame containing the sheet to operate on
    settings (pd.DataFrame): DataFrame containing start and end dates for rounds

    Returns
    _________
    sheet (pd.DataFrame): The updated sheet
    '''
    # Iterate through the sheet
    for sht_index, sht_row in sheet.iterrows():
        date = sht_row['Date']
        # Iterate through the settings
        for set_index, set_row in settings.iterrows():
            # If the sheet's 'Date' column is within the date range in settings
            if set_row['Start'] <= date <= set_row['End']:
                # Set that sheet entry's round to the round in settings
                sheet.at[sht_index, 'Round'] = set_row['Round']

    return None
