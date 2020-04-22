# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:28:12 2020

@author: Mei
"""
import sys
import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode

def geo_code(df):
    df_new = df.copy()
    address = df.Address + ', ' + df.City + ', ' + df.State + ' ' + df.Zip.map(str)
    geo = geocode(address, provider='nominatim')
    long = geo.geometry.x
    lat = geo.geometry.y
    df_new['Longitude'] = long
    df_new['Latitude'] = lat
    return df_new

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('SYNTAX: python covid.py yesterday_file today_file')
        sys.exit()
    
    yesterday = sys.argv[1]
    today = sys.argv[2]
    output = "output.txt"
    
    df_yesterday = pd.read_csv(yesterday, sep='\t')
    df_today = pd.read_csv(today, sep='\t')

    df_yesterday.set_index('IncidentID', inplace=True)
    df_today.set_index('IncidentID', inplace=True)

    # new rows are indices in today's which are not in yesterday's
    new_rows = ~df_today.index.isin(df_yesterday.index)    
    df_new = geo_code(df_today[new_rows])

    # merge new rows with yesterday's    
    df_out = pd.concat([df_yesterday, df_new])    
    df_out.to_csv(output, sep='\t')
    
    print('{} new row(s) found'.format(df_new.shape[0]))    
    print('Done')    