# Import API key
from config import *
# Can also input API key (from openweathermap.org) with this format:
# API_KEY = " "

import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re 
from datetime import datetime

def geocoder(location):
    """Get the corresponding longitude and latitude of the user-supplied location."""

    # Prepare API request
    url = "http://api.openweathermap.org/geo/1.0/direct?"
    q = location
    payload = {'q': q, 'appid': API_KEY, 'limit': 1}

    # Query Geocoding API
    r = requests.get(url, params=payload)
    json = r.json()
    code = r.status_code

    # If request is successful:
    if code == 200 and len(json) > 0:
        # Assign first element of list to variable
        dict = json[0]
        # Return dictionary
        return {
            "code": code,
            "name": dict['name'],
            "lat": dict['lat'],
            "lon": dict['lon'],
            "country": dict['country']
        }
    # If list is empty
    elif code == 200 and len(json) == 0:
        return {
            "code": code,
            "message": 'Invalid location'
        }
    # If some other error has occurred
    else: 
        return {
            "code": code,
            "message": json['message']
        }

def current_ap(lat, lon):
    """Retrieve current air pollution data."""

    # Prepare API request
    url = "http://api.openweathermap.org/data/2.5/air_pollution?"
    payload = {'lat': lat, 'lon': lon, 'appid': API_KEY}

    # Query Air Pollution API
    r = requests.get(url, params=payload)
    json = r.json()
    code = r.status_code

    # If request is successful:
    if code == 200 and len(json) == 2:
        # Extract components of AQI 
        dict = json.get('list')[0].get('components')
        # Append AQI to dictionary
        dict['aqi'] = json.get('list')[0].get('main').get('aqi')
        # Get timestamp and format to human-readable local time
        ts = json.get('list')[0].get('dt')
        dict['dt'] = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # Add status code
        dict['code']: code
        # Get coordinates and merge with existing dictionary
        dict = dict | json.get('coord')
    
        return dict
    # If error has occurred
    else:
        return {
            "code": code,
            "message": json['message']
        }

def component_cat(ap_dict):
    """Get qualitative category per air pollution component and return list"""

    # Components of interest
    comps = ['so2', 'no2', 'pm10', 'pm2_5', 'o3', 'co']
    # Cut-off values per category
    bounds = {
        'so2': [0, 20, 80, 250, 350],
        'no2': [0, 40, 70, 150, 200],
        'pm10': [0, 20, 50, 100, 200],
        'pm2_5': [0, 10, 25, 50, 75],
        'o3': [0, 60, 100, 140, 180],
        'co': [0, 4400, 9400, 12400, 15400]
        }
    # Qualitative categores
    cats = ['good', 'fair', 'moderate', 'poor', 'very poor']

    # Empty list
    list = []

    for component in comps:
        # For every component of interest, get current value and relevant cut-offs
        bds = bounds[component]
        value = ap_dict[component]

        # For categories from good to poor
        for i in range(4):
            if value >= bds[i] and value < bds[i + 1]:
                category = cats[i]
        # For very poor category
        if value >= bds[4]:
            category = cats[4]

        # Compile in dictionary and add to list
        d = {'component' : component, 'value': value, 'category': category}
        list += [d]
    return list

def aqi_cat(aqi):
    """Get qualitative category of AQI"""

    # Qualitative categories
    cats = ['good', 'fair', 'moderate', 'poor', 'very poor']
    index = [1, 2, 3, 4, 5]

    for i in range(5):
        if aqi == index[i]:
            return cats[i]
    return 'NA'

def date_converter(datestring):
    """Convert datestring to unix time, UTC time zone"""

    date = datetime.strptime(datestring, '%Y-%m-%d')
    date = date.timestamp()
    date = int(date)
    return date

def create_plots(df):
    """Create plots for air pollutants"""

    # Set style of plot
    plt.style.use('seaborn-v0_8-pastel')
    plt.rcParams['figure.figsize'] = (8, 5)

    # Remove "components." string from column names
    df.columns = [re.sub("components.", "", x) for x in df.columns]
    # Set category bounds per component; an upper bound is added to limit the y-axis 
    bounds = {
        'so2': [0, 20, 80, 250, 350, 370],
        'no2': [0, 40, 70, 150, 200, 240],
        'pm10': [0, 20, 50, 100, 200, 220],
        'pm2_5': [0, 10, 25, 50, 75, 85],
        'o3': [0, 60, 100, 140, 180, 240],
        'co': [0, 4400, 9400, 12400, 15400, 19800]
    }
    # Set title names
    titles = {
        'so2': "$SO_2$",
        'no2': "$NO_2$",
        'pm10': "$PM_{10}$",
        'pm2_5': "$PM_{2.5}$",
        'o3': "$O_3$",
        'co': "$CO$"
    }
    # Set colors of regions from bottom to top (green to red)
    color = ['#1a9641', '#a6d96a', '#ffffbf', '#fdae61', '#d7191c']
    # Set transparency of color regions
    ALPHA = 0.3

    # Create plot for every component:
    for k in range(len(df.columns)):
        # Set column of interest
        comp = df.columns[k]
        # Plot values
        ax = df[comp].plot(color='black')
        # Set the upper limit of the y axis 
        bounds[comp][5] = max([bounds[comp][5], max(df[comp])])
        # Remove margins and set limits of y axis based on ranges of categories
        ax.margins(0)
        ax.set_ylim(bounds[comp][0], bounds[comp][5])
        # Color regions
        for i in range(5):
            ax.axhspan(bounds[comp][i], bounds[comp][i + 1], facecolor=color[i], alpha=ALPHA)
        # Set labels
        plt.xlabel("Date")
        plt.ylabel("$μg/m^3$")
        plt.title(titles[comp])
        plt.savefig('./static/' + comp + '.png')
        plt.close()

def historical_ap(lat, lon, start, end):
    """Retrieve current air pollution data."""

    # Prepare API request
    url = "http://api.openweathermap.org/data/2.5/air_pollution/history?"
    payload = {'lat': lat, 'lon': lon, 'start': start, 'end': end, 'appid': API_KEY}

    # Query historical API
    r = requests.get(url, params=payload)
    json = r.json()
    code = r.status_code

    # If request is successful:
    if code == 200 and len(json) == 2:
        # Get longitude and latitude of result
        dict = json.get('coord')

        # Get flat table 
        df = pd.json_normalize(json.get('list'))
        # Convert timestamp to human-readable datetime
        df.dt = df.dt.apply(lambda x: datetime.fromtimestamp(x))
        df['dt'] = pd.to_datetime(df['dt'])

        # Add start and end dates of results to dictionary
        dict['start'] = min(df['dt']).strftime("%B %d, %Y")
        dict['end'] = max(df['dt']).strftime("%B %d, %Y")

        # Set columns of interest
        cols = ['components.co', 'components.no2', 'components.o3', 'components.so2', 'components.pm2_5', 'components.pm10']
        # Group by date 
        grouped = df.groupby(pd.to_datetime(df['dt'].dt.date))
        # Save daily averages to dataframe
        daily = grouped[cols].mean()
        # Generate plots
        create_plots(daily)        
        return dict
    else:
        return {
            "code": code,
            "message": json['message']
        }




