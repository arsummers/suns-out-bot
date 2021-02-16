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


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": " HEY TESTING TESTING DOES THIS TAKE EDITS This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

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
  # should check for "clear sky" or "few clouds" or "scattered clouds"


    key = os.environ.get('WEATHER_API_KEY')

    url = f'https://api.weatherbit.io/v2.0/current?city=seattle&key={key}'

    response = requests.get(url)
    json_info = response.json()
    seattle_weather_desc = json_info["data"][0]["weather"]["description"]
    print(seattle_weather_desc)
    return seattle_weather_desc


def send_test_message():
  channel_id = "C01LBSKBRH7"
  today = date.today()
  d3 = today.strftime("%m/%d/%y")

  current_weather = check_weather()

  if current_weather == "Light Snow":

    try:
      result = client.chat_postMessage(
        channel = channel_id,
        text = f"Hello from suns out bot on {d3}! The weather is {current_weather}"
      )
      print(result)

    except SlackApiError as e:
      print(f"Error: {e}")


def send_test_message_scheduled():
  minute_from_now = datetime.date.today() + datetime.timedelta(days=1)
  scheduled_time = datetime.time(hour=11, minute=0)
  schedule_timestamp = datetime.datetime.combine(minute_from_now, scheduled_time).strftime('%s')

  channel_id = "C01LBSKBRH7" #general channel

  try:
    result = client.chat_scheduleMessage(
        channel=channel_id,
        text="Looking towards the future",
        post_at=schedule_timestamp
    )
    # Log the result
    logger.info(result)

  except SlackApiError as e:
    logger.error("Error scheduling message: {}".format(e))


# def check_weather():
#   # should return a weather object from an external API. The bot should should the weather, then, for now, send a message with the current weather.
#   # message should say something like "According to my calculations, it is {weather} and {} degrees outside. Today should be a good day to get outside for fresh air on your lunchbreak."

#     key = os.environ.get('WEATHER_API_KEY')

#     url = f'https://api.weatherbit.io/v2.0/current?city=seattle&key={key}'

#     response = requests.get(url)
#     json_info = response.json()
#     seattle_weather_desc = json_info["data"][0]["weather"]["description"]
#     print(seattle_weather_desc)
#     return seattle_weather_desc

def schedule_tester():
  print('THIS MESSAGE IS SCHEDULED')

def schedule_weather_trigger():
  # should be used to call check_weather on a schedule, so I won't have to rely on the next day forecast. It should call check_weather at 11 AM, then call send_message right after if the weather is satisfactory

  # will need to use at(time_str) method to get this to trigger at the same time each day

  # will need to use class schedule.Job(interval, schedule-None)
  schedule.every().day.at("12:57").do(schedule_tester)


def send_test_dm():
  # should start a 1 one 1 conversation with a user when triggered. Should default to DM, since it's ableist to assume everyone in a channel is able to step outside.
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
    # schedule_weather_trigger()
    check_weather()
    # send_test_message()
    # send_test_message_scheduled()
    app.start(port=int(os.environ.get("PORT", 3000)))
    # get_channel_id()