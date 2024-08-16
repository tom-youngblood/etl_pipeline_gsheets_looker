import pandas as pd
from scripts.load_data import load_data
from datetime import datetime

def clean_sheets_leads(data, start_date):
    '''
    Main function of clean_sheets_leads Python script. Cleans and combines leads from the given spreadsheet based on specific client needs.
    _________

    Arguments
    _________
    data (dict): Dictionary of data from load_data function in load_data.py
    start_date (datetime): The cutoff date for adding leads to leadDataClean_df.

    Returns
    _________
    leadDataClean_df (pd.DataFrame): DataFrame containing cleaned lead data.
    flagged_df (pd.DataFrame): DataFrame containing flagged leads for further review.
    '''
    # Combine leads from leadData and outliers into leadDataClean
    leadDataClean_df, flagged_df = update_sheets(data, start_date)

    return leadDataClean_df, flagged_df

def update_sheets(data, start_date):
    '''
    Updates leadDataClean and flagged DataFrames by adding leads from leadData and outliers.

    Arguments
    _________
    data (dict): Dictionary containing the data for processing.
    start_date (datetime): The cutoff date for filtering leads.

    Returns
    _________
    leadDataClean_df (pd.DataFrame): DataFrame containing combined lead data.
    flagged_df (pd.DataFrame): DataFrame containing flagged leads for further review.
    '''
    # Extract necessary DataFrames
    leadData_df = data['leadData_df']
    outliers_df = data['outliers_df']
    flagged_df = data['flagged_df']
    leadDataClean_df = data['leadDataClean_df']

    # Convert 'Create Date' columns to datetime for comparison
    leadData_df['Create Date'] = pd.to_datetime(leadData_df['Create Date'], format="%m/%d/%y %H:%M")
    outliers_df['Create Date'] = pd.to_datetime(outliers_df['Create Date'], format="%m/%d/%y %H:%M")

    # Filter and add leads to leadDataClean_df
    for index, row in leadData_df.iterrows():
        is_in_outliers = not outliers_df[outliers_df['Record ID'] == row['Record ID']].empty
        is_in_flagged = not flagged_df[flagged_df['Record ID'] == row['Record ID']].empty

        # Add to flagged_df if lead was created before start_date and not in outliers or flagged
        if row['Create Date'] < start_date and not is_in_outliers and not is_in_flagged:
            flagged_df = pd.concat([flagged_df, row.to_frame().T], ignore_index=True)

        # Add to leadDataClean_df if lead was created after start_date and not in outliers or flagged
        if row['Create Date'] >= start_date and not is_in_outliers and not is_in_flagged:
            leadDataClean_df = pd.concat([leadDataClean_df, row.to_frame().T], ignore_index=True)

    # Add outliers to leadDataClean_df if not already present
    for index, row in outliers_df.iterrows():
        if row['Record ID'] not in leadDataClean_df['Record ID'].values:
            leadDataClean_df = pd.concat([leadDataClean_df, row.to_frame().T], ignore_index=True)

    return leadDataClean_df, flagged_df
