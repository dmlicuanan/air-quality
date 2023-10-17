# Air Quality Tracker
#### Video Demo:  https://youtu.be/62-WwWV-YZ0
#### Description:
Air Quality Tracker is a web-based application that returns current and historical air pollution data for a user-supplied location. A user may opt to input the location of interest by its city name or by geographical coordinates. The web app is powered by the Air Pollution API and Geocoding API of OpenWeather (https://openweathermap.org). An API key is required to use these services, which the user must input in the config.py file. To generate an API key, the user must sign up for an account through openweathermap.org. The free plan allows up to 60 API calls per minute. I found OpenWeather services suitable for the application since account sign-up does not require billing information, and OpenWeather is relatively well-established, having provided weather data services since 2014.

For current air pollution data, concentrations of common air pollutants (sulfur dioxide, nitrogen dioxide, particulates, ozone, carbon monoxide) are returned. The corresponding qualiative categories of the pollutant densities are also returned based on the OpenWeather scale for Air Quality Index (https://openweathermap.org/api/air-pollution). The overall air quality is also provided based on the same scale.

As I wanted to learn data visualization tools in Python (e.g.pandas and matplotlib), I also created an option that allows users to view historical air pollution data for a location. Average daily concentrations of air pollutants are plotted for a date range specified by the user, which cannot be earlier than November 27, 2020 and cannot be later than the current date. Regions of the plot are colored based on the qualitative categories (good, fair, moderate, poor, and very poor) of value ranges for each air pollutant.

Project files and directories:
- app.py contains the code for the Flask application. It defines which HTML pages are rendered for each route.
- helpers.py contains helper functions called in app.py.
    - geocoder() returns latitude, longitude, country, etc., given a city name, using the Geocoding API
    - current_ap() returns current measurements of air quality index, air pollution components, etc., given geographic coordinates, using the Air Pollution API
    - component_cat() categorizes the pollutant concentrations based on set value ranges
    - aqi_cat() returns the corresponding qualitative category of the air quality index
    - date_converter() converts a date string to unix time, which is needed for the API calls
    - historical_ap() calls the Air Pollution API for historical air pollution data; it also calls create_plots() which creates line plots for each pollutant gas
- config.py is where the user must specify their API key from https://openweathermap.org
- air-quality.ipynb, not required to run the web-app, is the Jupyter notebook where explored the OpenWeather APIs and first created plots
- templates directory
    - current_1.html and current_2.html structure the results pages for getting current air pollution information by city name and by coordinates, respectively 
    - historical_1.html and historical_2.html structure the results pages for getting historical air pollution data by city name and by coordinates, respectively
    - layout.html specifies the overall structure of all HTML pages
- static directory
    - styles.css is the CSS stylesheet for the HTML pages
    - co.png, no.png, o3.png, pm2_5.png, pm10.png, so2.png are the file names of the plots expected after historical_1.html and historical_2.html are accessed via POST.

***

Author's note:
This is my final project for Harvard University's CS50 (Introduction to Computer Science), which I completed on 2023-10-12. Codes last updated on 2023-10-13.