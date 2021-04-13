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
 
if __name__ == "__main__":
    # schedule_weather_trigger()
    # check_weather()
    # send_weather_message()
    suns_out_bot_go()
    app.run(host='0.0.0.0', port=8080)



    # get_channel_id()