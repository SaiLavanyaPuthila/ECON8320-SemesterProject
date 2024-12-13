import pandas as pd
import os

series_list = ["LNS11000000", "LNS12000000", "LNS13000000", "LNS14000000", "CES0000000001", 
               "CES0500000002", "CES0500000007", "CES0500000003", "CES0500000008", 
               "PRS85006092", "PRS85006112", "PRS85006152", "MPU4910012", "CUUR0000SA0", 
               "CUUR0000AA0", "CWUR0000SA0", "CUUR0000SA0L1E", "CWUR0000SA0L1E", "WPSFD4", 
               "WPUFD4", "WPUFD49104", "WPUFD49116", "WPUFD49207", "EIUIR", "EIUIQ", 
               "CIU1010000000000A", "CIU2010000000000A", "CIU2020000000000A",]


# Initialize variables to None
df_LNS11000000 = None
df_LNS12000000 = None
df_LNS13000000 = None
df_LNS14000000 = None
df_CES0000000001 = None
df_CES0500000002 = None
df_CES0500000007 = None
df_CES0500000003 = None
df_CES0500000008 = None
df_PRS85006092 = None
df_PRS85006112 = None
df_PRS85006152 = None
df_MPU4910012 = None
df_CUUR0000SA0 = None
df_CUUR0000AA0 = None
df_CWUR0000SA0 = None
df_CUUR0000SA0L1E = None
df_CWUR0000SA0L1E = None
df_WPSFD4 = None
df_WPUFD4 = None
df_WPUFD49104 = None
df_WPUFD49116 = None
df_WPUFD49207 = None
df_EIUIR = None
df_EIUIQ = None
df_CIU1010000000000A = None
df_CIU2010000000000A = None
df_CIU2020000000000A = None

# Load the CSVs into separate variables
for series in series_list:
    try:
        df = pd.read_csv(f"data/{series}.csv")
        if series == "LNS11000000":
             df_LNS11000000 = df
        elif series == "LNS12000000":
             df_LNS12000000 = df
        elif series == "LNS13000000":
             df_LNS13000000 = df
        elif series == "LNS14000000":
             df_LNS14000000 = df
        elif series == "CES0000000001":
             df_CES0000000001 = df
        elif series == "CES0500000002":
             df_CES0500000002 = df
        elif series == "CES0500000007":
            df_CES0500000007 = df
        elif series == "CES0500000003":
             df_CES0500000003 = df
        elif series == "CES0500000008":
             df_CES0500000008 = df
        elif series == "PRS85006092":
            df_PRS85006092 = df
        elif series == "PRS85006112":
            df_PRS85006112 = df
        elif series == "PRS85006152":
            df_PRS85006152 = df
        elif series == "MPU4910012":
            df_MPU4910012 = df
        elif series == "CUUR0000SA0":
             df_CUUR0000SA0 = df
        elif series == "CUUR0000AA0":
             df_CUUR0000AA0 = df
        elif series == "CWUR0000SA0":
            df_CWUR0000SA0 = df
        elif series == "CUUR0000SA0L1E":
            df_CUUR0000SA0L1E = df
        elif series == "CWUR0000SA0L1E":
            df_CWUR0000SA0L1E = df
        elif series == "WPSFD4":
            df_WPSFD4 = df
        elif series == "WPUFD4":
            df_WPUFD4 = df
        elif series == "WPUFD49104":
            df_WPUFD49104 = df
        elif series == "WPUFD49116":
            df_WPUFD49116 = df
        elif series == "WPUFD49207":
            df_WPUFD49207 = df
        elif series == "EIUIR":
            df_EIUIR = df
        elif series == "EIUIQ":
           df_EIUIQ = df
        elif series == "CIU1010000000000A":
           df_CIU1010000000000A = df
        elif series == "CIU2010000000000A":
             df_CIU2010000000000A = df
        elif series == "CIU2020000000000A":
             df_CIU2020000000000A = df
    except FileNotFoundError:
        print(f"File not found for series: {series}. Make sure the csv file exists in the 'data' directory.")


# Example of checking if a dataframe was loaded before using it
if df_LNS11000000 is not None:
    print("Displaying head of df_LNS11000000:")
    print(df_LNS11000000.head())
else:
    print("df_LNS11000000 was not loaded.")

if df_CIU2020000000000A is not None:
    print("Displaying head of df_CIU2020000000000A:")
    print(df_CIU2020000000000A.head())
else:
    print("df_CIU2020000000000A was not loaded.")