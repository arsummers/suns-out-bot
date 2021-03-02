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


# @app.event("app_home_opened")
# def update_home_tab(client, event, logger):
#   try:
#     # views.publish is the method that your app uses to push a view to the Home tab
#     client.views_publish(
#       # the user that opened your app's app home
#       user_id=event["user"],
#       # the view object that appears in the app home
#       view={
#         "type": "home",
#         "callback_id": "home_view",

#         # body of the view
#         "blocks": [
#           {
#             "type": "section",
#             "text": {
#               "type": "mrkdwn",
#               "text": "*Welcome to your _App's Home_* :tada:"
#             }
#           },
#           {
#             "type": "divider"
#           },
#           {
#             "type": "section",
#             "text": {
#               "type": "mrkdwn",
#               "text": " HEY TESTING TESTING DOES THIS TAKE EDITS This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
#             }
#           },
#           {
#             "type": "actions",
#             "elements": [
#               {
#                 "type": "button",
#                 "text": {
#                   "type": "plain_text",
#                   "text": "Click me!"
#                 }
#               }
#             ]
#           }
#         ]
#       }
#     )
  
#   except Exception as e:
#     logger.error(f"Error publishing home tab: {e}")

###########################################################
# testing sending a basic message here

def get_channel_id():


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
  # message should say something like "According to my calculations, it is {weather} and {} degrees outside. Today should be a good day to get outside for fresh air on your lunchbreak."
  # should check for "Clear sky" or "Few clouds" or "Scattered clouds"


    key = os.environ.get('WEATHER_API_KEY')
    zip_code = os.environ.get('ZIP_CODE')

    url = f'https://api.weatherbit.io/v2.0/current?postal_code={zip_code}&country=US&key={key}'

    response = requests.get(url)
    json_info = response.json()
    weather_desc = json_info["data"][0]["weather"]["description"]
    print(weather_desc)
    return weather_desc

def check_and_convert_temp():
    key = os.environ.get('WEATHER_API_KEY')
    zip_code = os.environ.get('ZIP_CODE')

    url = f'https://api.weatherbit.io/v2.0/current?postal_code={zip_code}&country=US&key={key}'

    response = requests.get(url)
    json_info = response.json()
    celsius_temp = json_info["data"][0]["temp"]
    fahrenheit_temp = int((celsius_temp * 9/5) + 32)
    return fahrenheit_temp


def send_weather_message():
  channel_id = os.environ.get('BOT_CHANNEL_ID')
  today = date.today()
  d3 = today.strftime("%m/%d/%y")

  current_weather = check_weather()
  current_temp = check_and_convert_temp()

  if current_weather == "Overcast clouds" or current_weather == "Overcast Clouds" or current_weather == "Scattered Clouds" or current_weather == "Clear sky" or current_weather == "Few clouds":

    try:
      result = client.chat_postMessage(
        channel = channel_id,
        text = f"Good afternoon! According to my calculations, the weather right now is {current_weather} and {current_temp} degrees Fahrenheit."
      )
      print(result)

    except SlackApiError as e:
      print(f"Error: {e}")


# This will stay commented out until I can see if it can be used to check the weather as well as send a message.
# def send_test_message_scheduled():
#   minute_from_now = datetime.date.today() + datetime.timedelta(days=1)
#   scheduled_time = datetime.time(hour=16, minute=36)
#   schedule_timestamp = datetime.datetime.combine(minute_from_now, scheduled_time).strftime('%s')

#   channel_id = "C01LBSKBRH7" #general channel

#   try:
#     result = client.chat_scheduleMessage(
#         channel=channel_id,
#         text="Looking towards the future",
#         post_at=schedule_timestamp
#     )
#     # Log the result
#     logger.info(result)

#   except SlackApiError as e:
#     logger.error("Error scheduling message: {}".format(e))


def schedule_weather_trigger():
  """
  Set to run in the background. Calls send_weather_message, which checks the weather and sends a message. Time can be adjusted

  """

  schedule.every().day.at("11:59").do(send_weather_message)
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

#   # if seattle weather == 'sunny' or 'clear', and time == 11AM PST, call this function
#   pass

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

    get_channel_id()