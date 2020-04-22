# Alameda County COVID Dashboard

Python script for data processing COVID-19 data for Alameda County Health Department.

## Installation
Requires Python 3.6

Additional libraries:
- pandas
- geopandas

## How to run
Call the script with yesterday's datafile and today's datafile
<pre> python covid.py yesterday_file today_file</pre>

## Output
- The output file is a tab separated file which contains the merged rows from yesterday's file with the new rows from today. 
- Longitude and Latitude are looked up using a concatination of address, city, state, and zip fields.
