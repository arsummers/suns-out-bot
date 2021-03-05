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

  # this block grabs the channel ID
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
  Checks weather. If certain conditions are met, it will send a message saying the current weather conditions and temperate, and a prompt to go outside.
  """
  channel_id = os.environ.get('BOT_CHANNEL_ID')
  today = date.today()
  d3 = today.strftime("%m/%d/%y")

  current_weather = check_weather()
  current_temp = check_and_convert_temp()

  acceptable_weather = ['overcast clouds', 'scattered clouds', 'clear sky', 'few clouds', 'moderate rain']

  if current_weather in acceptable_weather:

    try:
      result = client.chat_postMessage(
        channel = channel_id,
        text = f"Good afternoon! According to my calculations, the outside world features {current_weather} and is {current_temp} degrees Fahrenheit. Maybe this would be a nice time to go outside."
      )
      print(result)

    except SlackApiError as e:
      print(f"Error: {e}")


# This will stay commented out until I can see if it can be used to check the weather as well as send a message. Doesn't seem to be a way to make this check weather on a schedule as well - probably won't be right for my needs, since weather check should happen right before message.
# def send_test_message_scheduled():
#   """
#   uses Slack's scheduleMessage function to check the weather and send a message at a specified time daily. 
#   """

#   today = datetime.date.today()
#   scheduled_time = datetime.time(hour=16, minute=23)
#   schedule_timestamp = datetime.datetime.combine(today, scheduled_time).strftime('%s')

#   channel_id = os.environ.get('BOT_CHANNEL_ID')

#     try:
#       result = client.chat_scheduleMessage(
#           channel=channel_id,
#           text=f"looking to the future",
#           post_at=schedule_timestamp
#       )
#       # Log the result
#       logger.info(result)

#     except SlackApiError as e:
#       logger.error("Error scheduling message: {}".format(e))


def schedule_weather_trigger():
  """
  Set to run in the background. Calls send_weather_message, which checks the weather and sends a message. Time can be adjusted
  """

  schedule.every().day.at("16:33").do(send_weather_message)
  while True:
        schedule.run_pending()
        time.sleep(1)



#################################
#        STRETCH GOAL           #
#################################
def send_test_dm():
  # should start a 1 one 1 conversation with a user when triggered. Should default to DM, since it's ableist to assume everyone in a channel is able to step outside.
  # will need to grab conversation ID
  # "provide the user's user ID as the channel value "
  # beware of channel_not_found errors

  pass






###################################################
# will need to study where to incorporate ack()
# def send_weather_message(client, message):
#   #TODO: get this to send a "Hello World" message to the slack channel as the bot user. say() function only triggers if it has a message to reply to, so won't be useful here. Will likely need to use client.chat_postMessage for this project



# @app.command("/mute")
# def mute_bot():
#   """
#   will mute bot upon receiving '/mute' command
#   """
#   pass

# @app.command("/unmute")
# def unmute_bot():
#   pass

    
if __name__ == "__main__":
    schedule_weather_trigger()
    # check_weather()
    # send_weather_message()
    # send_test_message_scheduled()
    app.start(port=int(os.environ.get("PORT", 3000)))


    # get_channel_id()