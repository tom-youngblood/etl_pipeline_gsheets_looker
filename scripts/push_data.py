import gspread
import pandas as pd

def push_data(sheets, ss):
    '''
    Pushes pandas dataframes into
    _________

    Arguments
    _________
    sheets (dict of pd.DataFrames): dictionary of sheets to push to Google Sheets
    '''

    # Mapping of sheet names to DataFrames
    sheet_mapping = {
        #'leadDataClean_df': 'leadDataClean',
        #'flagged_df': 'flagged',
        'metadataFacebook_df': 'metadataFacebook',
        'metadataGoogle_df': 'metadataGoogle',
        'metadataLI_df': 'metadataLI'
    }


    # Convert timestamp columns back to str
    for sheet_name, sheet in sheets.items():
        print(f"Processing {sheet_name}: {sheet}")
        if sheet is None:
            print(f"Warning: {sheet_name} is None and will be skipped.")
            continue

        # If the sheet has a 'Create Date' column, convert it to str
        if 'Create Date' in sheet.columns:
            sheet['Create Date'] = sheet['Create Date'].astype(str)
        # If the sheet has a 'Date' column, convert it to str
        if 'Date' in sheet.columns:
            sheet['Date'] = sheet['Date'].astype(str)

    # Iterate through the dataframes
    for df_name, df in sheets.items():
        # Get the corresponding sheet name in Google Sheets
        sheet_name = sheet_mapping.get(df_name)
        # Upload the dataframe to Google Sheets if it exists
        if sheet_name:
            worksheet = ss.worksheet(sheet_name)

            # Clear existing content in the worksheet
            worksheet.clear()

            # Convert DataFrame to list of lists
            values = [df.columns.values.tolist()] + df.values.tolist()

            # Update the worksheet with the new values
            worksheet.update(values)
            print(f"Updated {sheet_name} with {len(values)-1} rows.")

    return None
