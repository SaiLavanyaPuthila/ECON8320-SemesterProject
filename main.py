import os
import json
from fetch_data import fetch_data_from_api, flatten_json_to_csv


def main():
    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    API_KEY = "13bcdc9f4f604f0bacdd80ed16f2386f"
    start_year = 2014
    end_year = 2024

    series_list = [
        "LNS13000000",
        "LNS12000000",
        "CES0000000001",
        "LNS14000000",
        "CES0500000003",
        "CES0500000002",
        "LNS11000000",
        "CUUR0000SA0",
    ]
    if not os.path.exists("data/"):
        os.makedirs("/data")

    fetch_data_from_api(BASE_URL, API_KEY, series_list, start_year, end_year)


if __name__ == "__main__":
    main()
