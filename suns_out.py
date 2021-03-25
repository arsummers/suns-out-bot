# going to try moving all the weather testing functions here, then importing it into the Flask app.

# imports up here!
import datetime
from datetime import date
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from slack_sdk import WebClient
# from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
import requests
import logging
import schedule
import time


class SunsOut:
    def __init__(self, channel):
        self.channel = channel

    def check_weather():
        """
        Pings weatherbit API, and returns a JSON response of the weather description in the provided zipcode. JSON response gets converted to lowercase for easier handling.
        """

        key = os.environ.get('WEATHER_API_KEY')
        zip_code = os.environ.get('ZIP_CODE')

        url = f'https://api.weatherbit.io/v2.0/current?postal_code={zip_code}&country=US&key={key}'

        response = requests.get(url)
        json_info = response.json()
        weather_desc = json_info["data"][0]["weather"]["description"]
        if weather_desc.lower() == "clear sky":
            print(weather_desc.lower())
            return "clear skies"
        print(weather_desc.lower())
        return weather_desc.lower()

    
    if __name__ == "__main__":
        check_weather()