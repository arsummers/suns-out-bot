Separate document for stretch goals

[-] If possible, incorporate the weather check into Slack's reminder/message scheduling functionality
```
def send_test_message_scheduled():
  """
  uses Slack's scheduleMessage function to check the weather and send a message at a specified time daily. 
  """

  today = datetime.date.today()
  scheduled_time = datetime.time(hour=16, minute=23)
  schedule_timestamp = datetime.datetime.combine(today, scheduled_time).strftime('%s')

  channel_id = os.environ.get('BOT_CHANNEL_ID')

    try:
      result = client.chat_scheduleMessage(
          channel=channel_id,
          text=f"looking to the future",
          post_at=schedule_timestamp
      )
      # Log the result
      logger.info(result)

    except SlackApiError as e:
      logger.error("Error scheduling message: {}".format(e))
```
[-] Create `/mute` `/unmute` abilities
[-] Make this send a message to a DM instead of a channel