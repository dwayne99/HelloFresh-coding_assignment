import pandas as pd
from meteostat import Point, Daily
from datetime import datetime

# Global variables
UK_weath_station_ID = '03779'   # ID for London Weather Station - fetched from Meteostat.Stations
OUTPUT_PATH = 'output.csv'


## Utils functions
def get_packs_count(temp_bands,temp, size):
    """
    INPUT:
        temp_bands (Pandas.DataFrame): dataset with Temperature Bands range and Number of ice packs
        temp (Float): temperature in C
        size (String): Size of pack could be ['S','M','L']
        
    OUTPUT:
        returns - the number of ice packs based on temperature range
    """

    # iterate over the temperature bands
    for i, row in temp_bands.iterrows():
        if temp >= row['temperature_min'] and temp <= row['temperature_max']: # check in what range the temperature falls in
            return row[size]

        
## LOAD orders data and process it
orders_dataset_path = 'data/Boxes.csv'
orders = pd.read_csv(orders_dataset_path)
orders['delivery_date'] = pd.to_datetime(orders['delivery_date'])  # change dtype of delivery_date column to date type
orders['num_ice_packs'] = 0 # Add a column to the dataset to store the number of ice-packs required

## INPUT the temperature_bands_dataset
temperature_bands_path = input('Enter the path of the Temperature bands CSV: ')  # INPUT path from user
temp_bands = pd.read_csv(temperature_bands_path)

## Iterate over all the orders and compute the ice packs requirements
for i,order in orders.iterrows():
    # get the year, month and construct date in required format for API
    year, month, day = int(order['delivery_date'].strftime('%Y')),int(order['delivery_date'].strftime('%m')),int(order['delivery_date'].strftime('%d'))
    start_date = datetime(year,month,day)
    # get temperature for the specific date
    temp = Daily(UK_weath_station_ID, start_date, start_date).fetch().tavg[0]
    size = order['Cool Pouch Size']
    orders.at[i,'num_ice_packs'] = get_packs_count(temp_bands,temp,size) # modify the num_ice_packs counts
    
## Export the new CSV
orders.to_csv('out.csv',index=False)