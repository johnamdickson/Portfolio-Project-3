from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import os
from termcolor import colored, cprint
import main
from os import system
from time import sleep
import functions as f


def get_user_coordinates():
    """
    Prompt user to input latitude and longitude and then perform
    error checking before returning both in a list.
    """
    while True:

        # Taking multiple inputs in one command solution found here:
        # https://www.geeksforgeeks.org/taking-multiple-inputs-from-user-in-python/

        # apply color formatting to strings to be highlighted to user.
        colored_latitude = f.format_data_strings("-90 and 90,", 'green')
        colored_longitude = f.format_data_strings("-180 and 180.", 'green')
        colored_whitespace = f.format_data_strings("separated by a space.\n",
                                                   'green')
        print("Please enter your chosen location's latitude and longitude "
              f"{colored_whitespace}")
        print(f"Note, latitude must be between {colored_latitude} longitude"
              f" between {colored_longitude}\n")
        print("Latitudes west of the Prime Meridian(Greenwich, London) and "
              "longitudes south of the equator should be negative.\n")
        try:
            # capture both values in one input using .spilt method.
            latitude, longitude = input(f"Please enter coordinates "
                                        "below:\n").split()
        except ValueError as e:
            # handle value errors from entering too many or too few entries.
            if e.args[0] == "not enough values to unpack (expected 2, got 1)":
                f.print_error_message("You only made one entry or did not "
                                      "include a space.\nPlease make two "
                                      "entries, one for latitude and another"
                                      " for longitude.", 3.5)
            elif e.args[0] == "too many values to unpack (expected 2)":
                f.print_error_message("You made too many entries.\nPlease "
                                      "make two entries, one for latitude and"
                                      " another for longitude.", 3.5)
            continue
        try:
            # convert user coordinates into discrete floats.
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            # handle value errors whereby coordinates can not be formatted as
            # floats.
            f.print_error_message("Invalid entry, please enter a number "
                                  "between -90 to 90 for latitude and -180 to"
                                  " 180 for longitude. ", 3)
            continue
        else:
            # check if latitude and longitude are within the allowable range.
            if latitude < -90 or latitude > 90:
                f.print_error_message("Invalid entry, please enter a latitude"
                                      " between -90 and 90", 3)
                continue
            elif longitude < -180 or longitude > 180:
                f.print_error_message("Invalid entry, please enter a longitude"
                                      " between -180 and 180", 3)
                continue
            break
    return [latitude, longitude]


def get_weather_forecast(coordinates):
    """
    Function to retrieve weather forecast data from coordinates specified
    by user.
    """
    # Maintaining API Key secrecy for deployment to Heroku via environment
    # variable. Solution found in Stack Overflow:
    # https://stackoverflow.com/questions/47949022/git-heroku-how-to-hide-my-secret-key

    # Deploympent to Heroku requires access to environment variable on
    # line below:
    API_KEY = os.getenv('API_KEY')

    # Use of pyowm library to utilise Open weather API
    # via documentation below:
    # https://pyowm.readthedocs.io/en/latest/

    # Deploympent to Heroku requires access to environment variable on
    # line below
    owm = OWM(API_KEY)
    latitude = coordinates[0]
    longitude = coordinates[1]
    # instantiate weather manager
    mgr = owm.weather_manager()

    # insantiate geocoding manager.
    geo_mgr = owm.geocoding_manager()
    # obtain forecast and location from Open Weather using coordinates.
    try:
        one_call = mgr.one_call(latitude, longitude, exclude='alerts')
        forecast_weather_dictionary = ([weather.to_dict() for weather
                                       in one_call.forecast_daily])
        location = geo_mgr.reverse_geocode(latitude, longitude)
        location_dict = [location.to_dict() for location in location]
    # Following code to handle any errors coming back from OWM API
    # Tutorial below used for Exceptions:
    # https://docs.python.org/3/tutorial/errors.html
    except Exception as err:
        return False, err.args
    else:
        return True, forecast_weather_dictionary, location_dict
