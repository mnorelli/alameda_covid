# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:28:12 2020

@author: Mei
"""
import sys
import pandas as pd
from geopandas.tools import geocode
from geopy.geocoders import ArcGIS

def geo_code(df):
    df_new = df.copy()
    address = df.Address + ', ' + df.City + ', ' + df.State + ' ' + df.Zip.map(str)
    try:
        geo = geocode(address, provider='arcgis')
    except:
        print('Error geocoding address. Aborting script')
        sys.exit()
    
    df_new['Longitude'] = geo.geometry.x
    df_new['Latitude'] = geo.geometry.y
    df_new['AddressFound'] = geo.address
    
    return df_new

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('SYNTAX: python covid.py yesterday_file today_file')
        sys.exit()
    
    yesterday = sys.argv[1]
    today = sys.argv[2]
    output = "output.txt"
    
    df_yesterday = pd.read_csv(yesterday, sep='\t')
    print('{} record(s) read from {}'.format(df_yesterday.shape[0], yesterday))
    
    df_today = pd.read_csv(today, sep='\t')
    print('{} record(s) read from {}'.format(df_today.shape[0], today))

    df_yesterday.set_index('IncidentID', inplace=True)
    df_today.set_index('IncidentID', inplace=True)

    # new rows are indices in today's which are not in yesterday's
    new_rows = ~df_today.index.isin(df_yesterday.index)
    print('{} new record(s) found'.format(df_today[new_rows].shape[0]))    

    print('Geocoding new records...')    
    df_new = geo_code(df_today[new_rows])

    # merge new rows with yesterday's    
    df_out = pd.concat([df_yesterday, df_new])    
    df_out.to_csv(output, sep='\t')
    
    print('Merged data written to {}'.format(output))