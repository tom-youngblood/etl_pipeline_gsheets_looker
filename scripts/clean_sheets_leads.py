import pandas as pd
from scripts.load_data import load_data
from datetime import datetime

def clean_sheets_leads(data, start_date):
    '''
    Main function of clean_sheets_leads Python script. Runs the functions of
    clean_sheets_leads.py to clean the leads of the given spreadsheet based on
    specific client needs.
    _________

    Arguments
    _________
    client (str): Name of the client
    data (dict): Dictionary of data from load_data function in load_data.py

    Returns
    _________
    (flagged_df, leadDataClean_df) (tuple): Tuple containing the flagged
    dataframe and the leadDataClean dataframe.
    '''
    # Update the outliersClean sheet
    flagged_df, leadDataClean_df = update_sheets(data, start_date)

    # Clean the columns of leadDataClean_df
    leadDataClean_df = add_cleaned_outliers_leadDataClean_df(data, leadDataClean_df)

    # Return the flagged df and the cleaned lead data df
    return (flagged_df, leadDataClean_df)

def update_sheets(data, start_date):
    '''
    Updates the leadDataClean (and thus, leadSummaryStats) and flagged sheets.

    If the lead's create date in leadData is after the given cutoff date, the
    lead is added to leadDataClean. If the lead does not meet the criteria,
    and it is not already in outliers, it is added to flagged for further
    review.

    Arguments
    _________
    data (dict): Dictionary of the form {<sheet_name>_df, data_values_for_sheet}

    Returns
    _________
    (flagged_df, leadDataClean_df) (tuple): Tuple containing flagged_df and leadDataClean_df
    '''
    # Load the neccessary sheets into variables
    leadData_df = data['leadData_df']
    outliers_df = data['outliers_df']
    flagged_df = data['flagged_df']
    leadDataClean_df = data['leadDataClean_df']

    # Convert columns to datetime
    leadData_df['Create Date'] = pd.to_datetime(leadData_df['Create Date'], format="%m/%d/%y %H:%M")
    outliers_df['Create Date'] = pd.to_datetime(outliers_df['Create Date'], format="%m/%d/%y %H:%M")
    leadDataClean_df['Create Date'] = pd.to_datetime(leadDataClean_df['Create Date'], format="%m/%d/%Y %H:%M:%S")

    # Iterate through the leadData sheet, ignoring header row
    for index, row in leadData_df.iterrows():

        # Create criteria
        is_in_outliers = not outliers_df[outliers_df['Record ID'] == row['Record ID']].empty
        is_in_flagged = not flagged_df[flagged_df['Record ID'] == row['Record ID']].empty

        # If the lead was generated before the start date and the row is not in outliers_df and is not in flagged_df
        if row['Create Date'] < start_date and not is_in_outliers and not is_in_flagged:
            # Add to flagged_df
            flagged_df.loc[index] = row

        # If the lead was generated after the start date and the the row is not in outliers_df and is not in flagged_df
        elif row['Create Date'] >= start_date and not is_in_outliers and not is_in_outliers and not is_in_flagged:
            leadDataClean_df.loc[index] = row

    return (flagged_df, leadDataClean_df)

def add_cleaned_outliers_leadDataClean_df(data, leadDataClean_df):
    '''
    Append cleaned outliers to leadDataClean_df

    Arguments
    _________
    data (dict): Used to get outliers_df
    leadDataClean_df (pd.DataFrame): Lead data

    Returns
    _________
    leadDataClean_df_final (pd.DataFrame): Lead data with replaced columns
    '''
    # Get neccessary variables
    outliers_df = data['outliers_df']

    # For all records in outliers_df
    for index, row in outliers_df.iterrows():
        # If the cleaned outlier is not in the lead data
        if row['Record ID'] not in leadDataClean_df['Record ID']:
            # Add the outlier to the lead data
            leadDataClean_df.loc[len(leadDataClean_df): row['Record ID']]
