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
from flask import Flask
from suns_out import SunsOut

from slack_logger import SlackHandler, SlackFormatter

logger = logging.getLogger(__name__)

# app = App(
#     token = os.environ.get("SLACK_BOT_TOKEN"),
#     signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
# )


app = Flask(__name__)
# might need events adapter here
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def suns_out_bot_go():
    """
    instantiate SunsOut from other module, make it go
    """
    suns_out_bot = SunsOut()

    send_to_slack = suns_out_bot.schedule_weather_trigger()
     



def get_channel_id():
    """
    gets the channel ID of all your Slack channels.
    """
    channel_name = "general"

    try:

      for response in client.conversations_list():
        for channel in result["channels"]:
          if channel["name"] == channel_name:
            conversation_id = channel["id"]
            print(f"Found conversation ID: {conversation_id}")
            break
    except SlackApiError as e:
      print(f"Error: {e}")


# def check_weather():
#     """
#     Pings weatherbit API, and returns a JSON response of the weather description in the provided zipcode. JSON response gets converted to lowercase for easier handling.
#     """

#     key = os.environ.get('WEATHER_API_KEY')
#     zip_code = os.environ.get('ZIP_CODE')

#     url = f'https://api.weatherbit.io/v2.0/current?postal_code={zip_code}&country=US&key={key}'

#     response = requests.get(url)
#     json_info = response.json()
#     weather_desc = json_info["data"][0]["weather"]["description"]
#     if weather_desc.lower() == "clear sky":
#       print(weather_desc.lower())
#       return "clear skies"
#     print(weather_desc.lower())
#     return weather_desc.lower()

# def check_and_convert_temp():
#     """
#     Pings weatherbit API, returns a JSON response of the current temperatue, and converts it to Fahrenheit.
#     """
#     key = os.environ.get('WEATHER_API_KEY')
#     zip_code = os.environ.get('ZIP_CODE')

#     url = f'https://api.weatherbit.io/v2.0/current?postal_code={zip_code}&country=US&key={key}'

#     response = requests.get(url)
#     json_info = response.json()
#     celsius_temp = json_info["data"][0]["temp"]
#     fahrenheit_temp = int((celsius_temp * 9/5) + 32)
#     return fahrenheit_temp


# def send_weather_message():
#     """
#     Checks weather. If certain conditions are met, it will send a message saying the current weather conditions and temperature, and a prompt to go outside.
#     """
#     channel_id = os.environ.get('BOT_CHANNEL_ID')
#     today = date.today()
#     d3 = today.strftime("%m/%d/%y")

#     current_weather = check_weather()
#     current_temp = check_and_convert_temp()

#     acceptable_weather = ['overcast clouds', 'scattered clouds', 'clear skies', 'few clouds']

#     if current_weather in acceptable_weather:

#       try:
#         result = client.chat_postMessage(
#           channel = channel_id,
#           text = f"Good afternoon! According to my calculations, the outside world is {current_temp} degrees Fahrenheit and features {current_weather}. Maybe this would be a nice time to go outside."
#         )
#         print(result)

#       except SlackApiError as e:
#         print(f"Error: {e}")

# def schedule_weather_trigger():
#     """
#     Set to run in the background. Sleeps for a day, calls send_weather_message, which checks the weather and sends a message. 
#     """


#     schedule.every().day.at("16:55").do(send_weather_message)
#     while True:
#           schedule.run_pending()
#           #time.sleep(86399) #sleeps for a day minus a second, then runs. Cuts down on unnecessary up time
#           time.sleep(1) # for testing

# suns_out_bot_go()    
if __name__ == "__main__":
    # schedule_weather_trigger()
    # check_weather()
    # send_weather_message()
    # app.start(port=int(os.environ.get("PORT", 3000)))
    suns_out_bot_go()
    app.run(host='0.0.0.0', port=3000)



    # get_channel_id()