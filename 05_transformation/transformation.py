import pandas as pd
from datetime import datetime, timedelta

# Part A: Read the csv file into a DataFrame
df = pd.read_csv("bc_trip259172515_230215.csv")

# Part B: Filtering
# Drop the unneeded columns
df = df.drop(['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP'], axis=1)

# Part C: Decoding
# Define a function to convert OPD_DATE and ACT_TIME into a timestamp
def convert_to_timestamp(row):
    date = datetime.strptime(row['OPD_DATE'], '%Y%m%d')
    time = timedelta(seconds=int(row['ACT_TIME']))
    return date + time

# Apply the function to each row to create the TIMESTAMP column
df['TIMESTAMP'] = df.apply(convert_to_timestamp, axis=1)

# Part D: More Filtering
# Drop the unneeded columns
df = df.drop(['OPD_DATE', 'ACT_TIME'], axis=1)

# Part E: Enhance
# Calculate the differences in METERS and TIMESTAMP
df['dMETERS'] = df['METERS'].diff()
df['dTIMESTAMP'] = df['TIMESTAMP'].diff().dt.total_seconds()

# Calculate the SPEED column
df['SPEED'] = df.apply(lambda row: row['dMETERS'] / row['dTIMESTAMP'] if row['dTIMESTAMP'] != 0 else 0, axis=1)

# Drop the unneeded columns
df = df.drop(['dMETERS', 'dTIMESTAMP'], axis=1)

