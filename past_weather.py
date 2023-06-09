import gspread
from google.oauth2.service_account import Credentials
from time import sleep
import sys
from termcolor import colored, cprint
import datetime as d
from os import system
from main import run_past_weather
import functions as f

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('historical-weather-data')

WEATHER_ARCHIVE_SHEET = SHEET.worksheet('archive')


def find_date_range():
    """
    Calculate date range in worksheet to display to user before making
    their entry.
    """
    # obtain earliest date by reading cell value at top most date entry
    # excluding header.
    earliest_date = WEATHER_ARCHIVE_SHEET.cell(2, 1).value
    row_count = len(WEATHER_ARCHIVE_SHEET.get_all_values())
    # obtain latest date by passing row count into cell method and returning
    # value.
    latest_date = WEATHER_ARCHIVE_SHEET.cell(row_count, 1).value
    return [earliest_date, latest_date]


def find_historical_data_row(date, date_range):
    """
    Function to find row in historical data spreadsheet and return data from
    row as list.
    """
    # Solution to selecting cell from Stack Overflow:
    # https://stackoverflow.com/questions/65234180/how-to-find-a-row-based-on-an-id-and-then-edit-the-row-with-gspread-python
    try:
        # look for cell in spreadsheet that matches the date entered
        # and return row data for the cell's row.
        cell = WEATHER_ARCHIVE_SHEET.find(date, in_column=1)
        weather_data = WEATHER_ARCHIVE_SHEET.row_values(cell.row)
        return True, weather_data
    except AttributeError:
        # Handle error by informing user of exception and then re-running the
        # main() function.
        error_message = (f"The date you selected is not available. You entered"
                         f" {date}\nDate should be between {date_range[0]}"
                         f" and {date_range[1]}.\n")
        return False, error_message


def get_date(sheet_dates):
    """
    Request date from user to locate historical weather data.
    """
    system('clear')
    while True:
        # Solution to highlighting text found in stack overflow:
        # https://www.studytonight.com/python-howtos/how-to-print-colored-text-in-python
        earliest_date = f.format_data_strings(sheet_dates[0], 'green')
        latest_date = f.format_data_strings(sheet_dates[1], 'green')
        print(f"Please enter the date to check the historical weather data for"
              " Dublin Airport.\n")
        print(f"Available dates between {earliest_date} and {latest_date}. \n")
        print("The date format should be: DD/MM/YYYY e.g 30/04/1978 \n")
        date = input("Enter your date below:\n")
        if validate_date(date):
            # Clear console for loading screen and break from
            # While loop to return date.
            system('clear')
            break
    return date


def validate_date(date):
    """Inside the try, creates a date object using datetiem class strptime
    method. Raises ValueError if date does not conform to date format.
    """
    # The following tutorial was used to determine the correct date format.
    # https://www.tutorialspoint.com/How-to-do-date-validation-in-Python

    # giving the date format
    date_format = '%d/%m/%Y'

    # using try-except blocks for handling the exceptions
    try:
        # formatting the date using strptime() function
        d.datetime.strptime(date, date_format)
        return True

    # If the date validation goes wrong
    except ValueError:
        # printing the appropriate text if ValueError occurs
        f.print_error_message(f"Incorrect data format, you entered '{date}' "
                              "\nDate should be in the format DD/MM/YYYY "
                              "e.g. 30/04/1978\n", 3)
        return False
    else:
        return True
