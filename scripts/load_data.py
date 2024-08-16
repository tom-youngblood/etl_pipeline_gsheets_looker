import gspread
import pandas as pd
import os

def load_data(client):
    '''
    Initializes an instance of gspread with the given client name. Creates a dictionary of format {<sheet_name>_df, data_values_for_sheet}
    _________

    Arguments
    _________
    client (str): Name of the client

    Returns
    ________
    sheet_dfs (dict): Dictionary of the format {<sheet_name>_df, data_values_for_sheet}
    ss (gspread object): The spreadsheet to operate on
    '''
    # Initialize Service Account
    sa = gspread.service_account()

    # Open Spreadsheet
    ss = sa.open(f"{str(client)} - dashboard - script data")

    # Establish Worksheets
    sheets = list(map(lambda x: x.title, ss.worksheets()))

    # Establish dictionaries containing all sheet data and sheet dfs
    sheet_data = {}
    sheet_dfs = {}

    # Open All Worksheets
    for ws in sheets:

        # Get titles
        ws_data_title = str(ws) + "_data"
        ws_df_title = str(ws) + "_df"

        # Append the data the data dictionary
        sheet_data[ws_data_title] = ss.worksheet(ws).get_all_values()
        data = sheet_data[ws_data_title][1:]
        columns = sheet_data[ws_data_title][0]

        # Append the df to the df dictionary
        sheet_dfs[ws_df_title] = pd.DataFrame(data, columns = columns)

    return sheet_dfs, ss

def save_sheet(data):
    '''
    Saves all sheets as .csv to data folder.
    _________

    Arguments
    _________
    data (dict): Dictionary of the format {<sheet_name>_df, data_values_for_sheet}

    Returns
    ________
    None
    '''
    # Save the sheets to data
    for sheet_name, sheet in data.items():
        # Save the sheets to csv
        print(sheet_name)
        sheet.to_csv(f'./data/{sheet_name}.csv')

    return None

def load_sheets_csv():
    '''
    Loads the saved .csv's. Used to avoid redundant pulls.
    _________

    Arguments
    _________
    data (dict): Dictionary of the format {<sheet_name>_df, data_values_for_sheet}

    Returns
    ________
    data (dict): Dictionary of the format {<sheet_name>_df, data_values_for_sheet}
    '''
    # Dictionary to hold DataFrames with filenames as keys
    data = {}

    # Path to data
    path = './data'

    # Iterate over all files in the directory
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file_path = os.path.join(path, filename)
            # Read the CSV file into a DataFrame
            data[str(filename.replace('.csv', ''))] = pd.read_csv(file_path, index_col=False)

    return data
