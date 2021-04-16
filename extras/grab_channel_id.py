
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

get_channel_id()