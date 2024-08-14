import gspread
import pandas as pd
from scripts.load_data import load_data
from scripts.clean_sheets_leads import clean_sheets_leads

def main():

    # Establish client name and cutoff date (for cleaning outliers)
    client = 'tovuti'
    start_date = ''

    # Load the data
    data = load_data(client)

    # For each sheet, create a variable
    clean_sheets_leads(data, cutoff_date)



main()
