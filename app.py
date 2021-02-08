import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App

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

def send_test_message():
  channel_id = "C01LBSKBRH7"

  try:
    result = client.chat_postMessage(
      channel = channel_id,
      text = "Hello from suns out bot on 2/8/21!"
    )
    print(result)

  except SlackApiError as e:
    print(f"Error: {e}")








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
    send_test_message()
    app.start(port=int(os.environ.get("PORT", 3000)))
    # get_channel_id()