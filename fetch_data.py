import requests
import json
import pandas as pd
import os
from datetime import datetime,date

#configuration


def fetch_data_from_api(BASE_URL, API_KEY, series_list: list, start_year: int = 2011, end_year: int = date.today().year):
    """
    Fetches the data from BLS public data API in subsets of 20 years and merges the results.

    Args:
        BASE_URL (str): The base URL of the API.
        API_KEY (str): API key for authentication.
        series_list (list): List of series for which data is required.
        start_year (int, optional): Start year for the data fetch. Defaults to 2011.
        end_year (int, optional): End year for the data fetch. Defaults to current year.

    Returns:
        dict: Merged JSON data containing the results for all subsets.
    """
    headers = {'Content-type': 'application/json'}

    # Divide the years into subsets of 20 years
    current_start_year = start_year
    while current_start_year <= end_year:
        current_end_year = min(current_start_year + 19, end_year)
        print(f"Fetching data for years {current_start_year} to {current_end_year}...")
        # Make the API request for the current subset of years
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
        response_data = response.json()
 
        current_start_year = current_end_year + 1
        flatten_json_to_csv(response_data)
    return 0

def flatten_json_to_csv(json_data):
    """
    Flattens JSON data with multiple series into individual CSV files.

    Args:
      json_data: A dictionary representing the JSON data.
    """
    # print(json_data)
    if "Results" not in json_data or "series" not in json_data["Results"]:
        print("Error: Invalid JSON format. 'Results' and 'series' keys are missing.")
        return

    for series in json_data["Results"]["series"]:
        series_id = series["seriesID"]
        data = series["data"]
        file_path = f"data/{series_id}.csv"
        # Create a Pandas DataFrame
        df_new = pd.DataFrame(data)
        df_new["series_id"] = series_id    
        
        try:
            df_existing = pd.read_csv(file_path)
            combined_df = pd.concat([df_existing,df_new],ignore_index=True)
            combined_df.drop_duplicates(subset=['year','period'],keep='last',inplace=True)
            combined_df.sort_values(by=['year','period'],inplace=True)
            combined_df.to_csv(file_path,index=False)
        except:
            df_new.to_csv(file_path,index=False)

        # Save to CSV
        # df.to_csv(f"data/{series_id}.csv", index=False)
        print(f"CSV file '{series_id}.csv' created successfully.")
        

    
    