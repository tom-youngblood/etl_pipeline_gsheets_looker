import gspread
import pandas as pd

def load_data(client):
    '''
    Initializes an instance of gspread with the given client name. Creates a dictionary of format {<sheet_name>_df, data_values_for_sheet}

    Arguments
    _________
    client (str): Name of the client

    Returns
    ________
    sheet_dfs (dict): Dictionary of the format {<sheet_name>_df, data_values_for_sheet}
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

    return sheet_dfs

def load_dfs(client):
    '''
    Unpacks a dictionary of format {<sheet_name>_df, data_values_for_sheet}

    Arguments
    _________
    client (str): Name of the client

    Returns
    _________
    tuple(data.values()) (tuple): Tuple containing dataframes of all of the sheets
    '''
    # Load the data with the given client name
    data = load_data(client)

    # Unpack the dataframes
    return tuple(data.values())

def clean_sheets(client):
    pass

    
def main():

    # Establish client name and sheets
    client = 'tovuti'

    # For each sheet, create a variable

main()
