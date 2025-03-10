# Earthquake Risk Logic 

## Overview 

This project helps clients understand earthquake risks across US states by;
1 - Counting earthquakes per state
2 - Checking how many quakes happened near the clients locations and calculate a risk score 

Aim is to deliver a proof-of-value to the client where we can show we utilise data to guide insurance decisions. 

## Requirements 

Python  

Python Libraries - requests & geopy (to measure distance between quakes and buildings)

## Setup

Clone the repository 
Create a virtual environment (optional)
Install dependancies using `pip install -r requirements.txt`

## Project Struture 

`Readme.md`
- Summary of project
`data.py`
- Holds constant data such as the ISO codes for US States and the client building locations 
`earthquake_risk_logic.py`
- logic to fetch data, analyse state risks, check building risks and print results 
`tests.py`
- tests to verify the codes works 
`requirements.txt`
- list of the python libraries needed to run this logic successfully 

## Notes
- Logic skips Hawaii as requested from the client (the task)
- Uses USGS’s 7-day summary feed (all_week.geojson). Therefore the results will change daily.
- Risk score is calculated by multiplying count and the magnitude. THis is a fairly basic way of calculating risk as many more factors that can be taken into account when deciding insurance risk (building structure, weather etc.)

## Future Improvements 
Use long term data / more detailed data to determine risk  

Add a visual element to the logic  

Better error handling / having a backup data source or using slightly older data  

If using the 7 day model - have some logic to compare it to historical averages & trends to show if the weekly count is high/ low /abnormal etc. 

## Credits 
USGS data from https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson 
