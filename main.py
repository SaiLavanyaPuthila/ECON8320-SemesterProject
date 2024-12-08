import os
import json
from fetch_data import fetch_data_from_api, flatten_json_to_csv


def main():
    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    API_KEY = "13bcdc9f4f604f0bacdd80ed16f2386f"
    start_year = 2020
    end_year = 2024
    series_list = ["CES0000000001"]
    
    # series_list = ["LNS11000000", "LNS12000000", "LNS13000000", "LNS14000000", "CES0000000001", "CES0500000002", "CES0500000007", "CES0500000003", "CES0500000008", "PRS85006092", "PRS85006112", "PRS85006152", "MPU4910012", "CUUR0000SA0", "CUUR0000AA0", "CWUR0000SA0", "CUUR0000SA0L1E", "CWUR0000SA0L1E", "WPSFD4", "WPUFD4", "WPUFD49104", "WPUFD49116", "WPUFD49207", "EIUIR", "EIUIQ", "CIU1010000000000A", "CIU2010000000000A", "CIU2020000000000A"]

    if not os.path.exists("data/"):
        os.makedirs("/data")

    fetch_data_from_api(
        BASE_URL, API_KEY, series_list, start_year, end_year
    )



if __name__ == "__main__":
    main()
