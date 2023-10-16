from flask import Flask, render_template, request
from datetime import date

from helpers import geocoder, current_ap, component_cat, aqi_cat, date_converter, historical_ap

# Configure application
app = Flask(__name__)

# Define default page
@app.route("/")
def index():
    return render_template("current_1.html")

# Get CURRENT air pollution data by CITY NAME
@app.route("/current_1", methods=['GET', 'POST'])
def current_1():
    if request.method == "POST":
        # Catch if form is empty
        if not request.form.get("city"):
            api_result = {"code": 400, "message": 'Enter a location'}
        else:
            # Get coordinates of user-supplied location
            location = request.form.get("city")
            geocoder_response = geocoder(location)

            # Pass coordinates to air pollution API
            if len(geocoder_response) > 2:
                # Get dictionary of results from current air pollution API
                current_ap_response = current_ap(lat = geocoder_response['lat'], lon = geocoder_response['lon'])

                # Store variables to be printed in response
                current_result_vars = {
                    'location': geocoder_response['name'],
                    'country': geocoder_response['country'],
                    'lat': current_ap_response['lat'],
                    'lon': current_ap_response['lon'],
                    'dt': current_ap_response['dt'],
                    'aqi': current_ap_response['aqi'],
                    'aqi_cat': aqi_cat(current_ap_response['aqi'])
                }

                # Get air pollution components and categories from API result
                components_list = component_cat(current_ap_response)

                return render_template("current_1.html", api_result = current_ap_response, components_list = components_list, current_result_vars = current_result_vars)
            else:
                api_result = geocoder_response
        return render_template("current_1.html", api_result = api_result)                
    else:
        return render_template("current_1.html")
    
# Get CURRENT air pollution data by COORDINATES
@app.route("/current_2", methods=['GET', 'POST'])
def current_2():
    if request.method == "POST":
        # Catch if form is empty
        if not request.form.get("lat") or not request.form.get("lon"):
            api_result = {"code": 400, "message": 'All fields required'}
        else:
            # Check if input is float
            try:
                lat = float(request.form.get("lat"))
                lon = float(request.form.get("lon"))
                # Check if coordinates are valid
                if lat <= 90 and lat >= -90 and lon <= 180 and lon >= -180:
                    # Get dictionary of results from current air pollution API
                    current_ap_response = current_ap(lat = lat, lon = lon)

                    # Store variables to be printed in response
                    current_result_vars = {
                        'lat': current_ap_response['lat'],
                        'lon': current_ap_response['lon'],
                        'dt': current_ap_response['dt'],
                        'aqi': current_ap_response['aqi'],
                        'aqi_cat': aqi_cat(current_ap_response['aqi'])
                    }

                    # Get air pollution components and categories from API result
                    components_list = component_cat(current_ap_response)

                    return render_template("current_2.html", api_result = current_ap_response, components_list = components_list, current_result_vars = current_result_vars)
                else:
                    api_result = {"code": 400, "message": 'Latitude must be within [-90, 90] degrees. Longitude must be within [-180, 180] degrees'}
            except ValueError:
                api_result = {"code": 400, "message": 'Invalid input'}
        return render_template("current_2.html", api_result = api_result)
    else:
        return render_template("current_2.html")
    
# Get HISTORICAL air pollution data by CITY NAME
@app.route("/historical_1", methods=['GET', 'POST'])
def historical_1():
    if request.method == "POST":
        # Catch if form is empty
        if not request.form.get("city") or not request.form.get("start") or not request.form.get("end"):
            api_result = {"code": 400, "message": 'All fields required'}
        else:
            # Get coordinates of user-supplied location
            location = request.form.get("city")
            geocoder_response = geocoder(location)

            # Get dates (unix time)
            start = date_converter(request.form.get("start"))
            end = date_converter(request.form.get("end"))
            # Get date now and min date
            min = date_converter('2020-11-27')
            today = date_converter(date.today().strftime('%Y-%m-%d'))

            # Pass variables to historical air pollution API  
            if (len(geocoder_response) > 2) and (start < end) and (start >= min) and (end <= today):
                historical_ap_response = historical_ap(lat = geocoder_response['lat'], lon = geocoder_response['lon'], start = start, end = end)

                # Store variables to be printed in response
                current_result_vars = {
                    'location': geocoder_response['name'],
                    'country': geocoder_response['country'],
                    'lat': historical_ap_response['lat'],
                    'lon': historical_ap_response['lon'],
                    'start': historical_ap_response['start'],
                    'end': historical_ap_response['end']
                }

                # Render page
                return render_template("historical_1.html", 
                                       api_result = historical_ap_response, 
                                       current_result_vars = current_result_vars)
            elif len(geocoder_response) == 2:
                api_result = geocoder_response
            elif (start >= end):
                api_result = {"code": 400, "message": 'Invalid date range'}
            elif (start < min):
                api_result = {"code": 400, "message": 'Start date cannot be earlier than November 27, 2020'}
            elif (end > today):
                api_result = {"code": 400, "message": 'End date cannot be past the date today'}
        return render_template("historical_1.html", api_result = api_result)
    else:
        return render_template("historical_1.html")
    
# Get HISTORICAL air pollution data by COORDINATES
@app.route("/historical_2", methods=['GET', 'POST'])
def historical_2():
    if request.method == "POST":
        # Catch if form is empty
        if not request.form.get("lat") or not request.form.get("lon") or not request.form.get("start") or not request.form.get("end"):
            api_result = {"code": 400, "message": 'All fields required'}
        else:
            # Check if input is float
            try:
                lat = float(request.form.get("lat"))
                lon = float(request.form.get("lon"))
                # Check if coordinates are valid
                if lat <= 90 and lat >= -90 and lon <= 180 and lon >= -180:
                    # Get dates (unix time)
                    start = date_converter(request.form.get("start"))
                    end = date_converter(request.form.get("end"))
                    # Get date now and min date
                    min = date_converter('2020-11-27')
                    today = date_converter(date.today().strftime('%Y-%m-%d'))

                    # Pass variables to historical air pollution API  
                    if (start < end) and (start >= min) and (end <= today):
                        historical_ap_response = historical_ap(lat = lat, lon = lon, start = start, end = end)

                        # Store variables to be printed in response
                        current_result_vars = {
                            'lat': historical_ap_response['lat'],
                            'lon': historical_ap_response['lon'],
                            'start': historical_ap_response['start'],
                            'end': historical_ap_response['end']
                        }

                        # Render page
                        return render_template("historical_2.html",
                                               api_result = historical_ap_response,
                                               current_result_vars = current_result_vars)
                    elif (start >= end):
                        api_result = {"code": 400, "message": 'Invalid date range'}
                    elif (start < min):
                        api_result = {"code": 400, "message": 'Start date cannot be earlier than November 27, 2020'}
                    elif (end > today):
                        api_result = {"code": 400, "message": 'End date cannot be past the date today'}
                else:
                    api_result = {"code": 400, "message": 'Latitude must be within [-90, 90] degrees. Longitude must be within [-180, 180] degrees'}
            except ValueError:
                api_result = {"code": 400, "message": 'Invalid input'}
        return render_template("historical_2.html", api_result = api_result)
    else:
        return render_template("historical_2.html")