import requests
import json
import pandas as pd
import os
from datetime import datetime, date
import logging

# Configuration
LOG_DIR = "logs"


def setup_logger():
    """Sets up a logger that writes to a new log file daily."""
    os.makedirs(LOG_DIR, exist_ok=True)  # Ensure log directory exists

    log_file = os.path.join(LOG_DIR, f"app_{date.today().strftime('%Y%m%d')}.log")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler which logs even debug messages
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()  # Initialize the logger



def fetch_data_from_api(BASE_URL, API_KEY, series_list: list, start_year: int = 2011,
                         end_year: int = date.today().year):
    """
    Fetches the data from BLS public data API in subsets of 20 years and merges the results.

    Args:
        BASE_URL (str): The base URL of the API.
        API_KEY (str): API key for authentication.
        series_list (list): List of series for which data is required.
        start_year (int, optional): Start year for the data fetch. Defaults to 2011.
        end_year (int, optional): End year for the data fetch. Defaults to current year.

    Returns:
        int: 0 if success, -1 if error.
    """
    headers = {'Content-type': 'application/json'}
    logger.info(f"Starting API data fetch for series: {series_list}, from {start_year} to {end_year}.")


    # Divide the years into subsets of 20 years
    current_start_year = start_year
    while current_start_year <= end_year:
        current_end_year = min(current_start_year + 19, end_year)
        logger.info(f"Fetching data for years {current_start_year} to {current_end_year}...")
        # Make the API request for the current subset of years
        try:
          response = requests.post(
              BASE_URL,
              data=json.dumps({
                  "seriesid": series_list,
                  "startyear": current_start_year,
                  "endyear": current_end_year,
                  "registrationkey": API_KEY
              }),
              headers=headers
          )
          response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
          response_data = response.json()
          logger.debug(f"API response for years {current_start_year}-{current_end_year}: {response_data}")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for years {current_start_year}-{current_end_year}: {e}")
            return -1  # Indicate failure

        current_start_year = current_end_year + 1
        flatten_json_to_csv(response_data)
    logger.info("Completed API data fetching and CSV processing successfully.")
    return 0


def flatten_json_to_csv(json_data):
    """
    Flattens JSON data with multiple series into individual CSV files.

    Args:
      json_data: A dictionary representing the JSON data.
    """
    if "Results" not in json_data or "series" not in json_data["Results"]:
        logger.error("Invalid JSON format. 'Results' and 'series' keys are missing.")
        return

    for series in json_data["Results"]["series"]:
        series_id = series["seriesID"]
        data = series["data"]
        file_path = f"data/{series_id}.csv"
        # Create a Pandas DataFrame
        df_new = pd.DataFrame(data)
        df_new["series_id"] = series_id
        logger.info(f"Processing data for series {series_id}...")
        try:
            df_existing = pd.read_csv(file_path)
            combined_df = pd.concat([df_existing, df_new], ignore_index=True)
            combined_df.drop_duplicates(subset=['year', 'period'], keep='last', inplace=True)
            # combined_df.sort_values(by=['year','period'],inplace=True) # Removed unused line
            combined_df.to_csv(file_path, index=False)
            logger.debug(f"Combined and updated data for series {series_id} to {file_path}.")
        except FileNotFoundError:
            df_new.to_csv(file_path, index=False)
            logger.info(f"Created new CSV file for series {series_id} at {file_path}.")

        except Exception as e:
            logger.error(f"Error processing data for series {series_id}: {e}")
        
        logger.info(f"CSV file '{series_id}.csv' created/updated successfully.")



# if __name__ == "__main__":
#     BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
#     API_KEY = os.environ.get("BLS_API_KEY")
#     series_list = ['LAUCN040010000000005','LAUCN040010000000006']  # Replace with your series IDs
    
#     if not API_KEY:
#         logger.error("BLS_API_KEY environment variable is not set. Exiting.")
#     else:
#         status = fetch_data_from_api(BASE_URL, API_KEY, series_list)
#         if status == 0:
#           logger.info("Data fetch and processing completed successfully.")
#         else:
#           logger.error("Data fetch and processing failed.")