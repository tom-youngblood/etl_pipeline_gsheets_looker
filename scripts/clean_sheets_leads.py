import pandas as pd
from scripts.load_data import load_data

def clean_sheets_leads(data, cutoff_date):
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
    None
    '''
    # Update the outliersClean sheet
    update_outliersClean(data, cutoff_date)

def update_outliersClean(data, cutoff):
    '''
    Updates the outliersClean sheet. If the lead's create date in leadData is
    after the given cutoff date, add the lead to outliersClean.

    Arguments
    _________
    data (dict): Dictionary of the form {<sheet_name>_df, data_values_for_sheet}

    Returns
    _________
    outliersClean_cleaned (df): The cleaned sheet
    '''
    # Get the outliersClean sheet
    outliersClean_df = data['outliersClean_df']

    #
