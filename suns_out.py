# imports up here!
import datetime
from datetime import date
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
import requests
import logging
import schedule
import time
from apscheduler.schedulers.background import BackgroundScheduler

class SunsOut:

    def __init__(self):
        pass

    def check_weather(self):
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

    def check_and_convert_temp(self):
        """
        Pings weatherbit API, returns a JSON response of the current temperatue, and converts it to Fahrenheit.
        """
        key = os.environ.get('WEATHER_API_KEY')
        zip_code = os.environ.get('ZIP_CODE')

        url = f'https://api.weatherbit.io/v2.0/current?postal_code={zip_code}&country=US&key={key}'

        response = requests.get(url)
        json_info = response.json()
        celsius_temp = json_info["data"][0]["temp"]
        fahrenheit_temp = int((celsius_temp * 9/5) + 32)
        return fahrenheit_temp

    def send_weather_message(self):
        """
        Checks weather. If certain conditions are met, it will send a message saying the current weather conditions and temperature, and a prompt to go outside.
        """

        client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


        channel_id = os.environ.get('BOT_CHANNEL_ID')
        today = date.today()
        d3 = today.strftime("%m/%d/%y")

        current_weather = self.check_weather()
        current_temp = self.check_and_convert_temp()

        acceptable_weather = ['overcast clouds', 'scattered clouds', 'clear skies', 'few clouds']

        if current_weather in acceptable_weather:

            try:
                result = client.chat_postMessage(
                channel = channel_id,
                text = f"Good afternoon! According to my calculations, the outside world is {current_temp} degrees Fahrenheit and features {current_weather}. Maybe this would be a nice time to go outside."
                )
                print(result)

            except SlackApiError as e:
                print(f"Error: {e}")

    def schedule_weather_trigger(self):
        """
        Set to run in the background. Sleeps for a day, calls send_weather_message, which checks the weather and sends a message. 
        """

        scheduler = BackgroundScheduler()
        job = scheduler.add_job(self.send_weather_message, 'cron', hour=12, minute=00)
        # job = scheduler.add_job(self.send_weather_message, 'interval', seconds=10)

        scheduler.start()