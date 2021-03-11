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

from slack_logger import SlackHandler, SlackFormatter

logger = logging.getLogger(__name__)

app = App(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
)

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


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

def check_and_convert_temp():
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


def send_weather_message():
    """
    Checks weather. If certain conditions are met, it will send a message saying the current weather conditions and temperature, and a prompt to go outside.
    """
    channel_id = os.environ.get('BOT_CHANNEL_ID')
    today = date.today()
    d3 = today.strftime("%m/%d/%y")

    current_weather = check_weather()
    current_temp = check_and_convert_temp()

    acceptable_weather = ['overcast clouds', 'scattered clouds', 'clear skies', 'few clouds', 'light rain']

    if current_weather in acceptable_weather:

      try:
        result = client.chat_postMessage(
          channel = channel_id,
          text = f"Good afternoon! According to my calculations, the outside world is {current_temp} degrees Fahrenheit and features {current_weather}. Maybe this would be a nice time to go outside."
        )
        print(result)

      except SlackApiError as e:
        print(f"Error: {e}")

# https://realpython.com/python-sleep/
def sleep(timeout, retry=3):
    def decorator(function):
      def wrapper(*args, **kwargs):
          retries = 0



def schedule_weather_trigger():
    """
    Set to run in the background. Calls send_weather_message, which checks the weather and sends a message. Time can be adjusted.
    """
    # may have to comment out  while testing webhook - don't want to get rid of it entirely until I know it can be replaced

    schedule.every().day.at("16:24").do(send_weather_message)
    while True:
          schedule.run_pending()
          time.sleep(1)

# def weather_webhook():
#     url = os.environ.get("WEBHOOK_URL")
#     webhook = WebClient(url)

#     response = webhook.send(text="webhook text!!")
#     assert response.status_code == 200
#     assert response.body == "ok"

    # while True:
    #     current_time = datetime.datetime.now()
    #     current_hour = current_time.hour
    #     current_minute = current_time.minute
    #     hour = 13
    #     minute = 40

    #     # https://medium.com/the-andela-way/how-to-build-a-task-notification-bot-for-slack-with-python-part-2-eebf2b329422 is doing the math here for me
    #     if current_hour - hour > minute:
    #         sleep_time = 24 - current_hour + hour - (current_minute/60)
    #     elif current_hour - hour < minute:
    #         sleep_time = hour - current_hour - (current_minute/60)
    #     elif current_hour == hour:
    #         if current_minute == minute:
    #             sleep_time = minute
    #         else:
    #             sleep_time = 24 - current_hour + hour - (current_minute/60)

    #     print('hello webhook world')
    #     send_weather_message()

    #     time.sleep(sleep_time * 3600)



    
if __name__ == "__main__":
    schedule_weather_trigger()
    # weather_webhook()
    # check_weather()
    # send_weather_message()
    app.start(port=int(os.environ.get("PORT", 3000)))


    # get_channel_id()