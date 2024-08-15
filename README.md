# ETL Pipeline for Google Sheets to Looker Studio

This project is an automated ETL (Extract, Transform, Load) pipeline designed to process data from HubSpot, clean and transform it using Python and Pandas, and prepare it for reporting in Looker Studio.

## Project Overview

- **Extract**: Data is automatically pulled from Google Sheets, where HubSpot populates new data every 12 hours, using gspread.
- **Transform**: The data is cleaned, reorganized, and enriched by adding necessary metadata using Pandas. The transformation process includes Hubspot lead cleaning based on client criteria, structural adaptations, and adding custom calculations.
- **Load**: The cleaned and transformed data is re-uploaded to Google Sheets, making it ready for dynamic reporting in Looker Studio.

## Key Features

- **Automation**: The pipeline is scheduled to run every 12 hours, ensuring that the data in Looker Studio is always up-to-date.
- **Customizable**: The transformation logic can be easily adapted to meet specific data requirements.
- **Scalable**: Built with modularity in mind, allowing for future expansion or integration with other data sources.

## Dependencies

- Python 3
- Pandas
- Google Sheets API / gspread
