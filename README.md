# suns-out-bot
Slack bot that lets you know when it is sunny outside, so you can take a walk or otherwise step outside during your lunch break.

IMPORTANT!
- will need to run `ngrok http 3000` command and `python app.py` in separate windows for this to start working. Then will need to update ngrok url under event subscriptions tag



## Core functionality

- [x] app should ping a weather API for local weather

- [x] if weather is sunny or otherwise dry, if should send a message that it's sunny out, and maybe you should step outside

- [x] it should send the message at 10:30 or 11:00 AM, so that the user has time to decide if they want to go outside on a break later in the day

- [x] The app should know the local time

- [ ] should send messages to DMs, so that entire channels won't have to have the reminders if they don't want them - DEBATABLE. Might be best to send to bot channel.

- [ ] should have ability to mute for set periods of time, if possible

- [ ] should have ability to configure the number of notifications per week. Checks weekly weather on Monday morning. If the whole week should be sunny, it can send out only 3 messages/week. Sunny day notifs are more important when they aren't regular.

- [ ] some ability to opt in to the bot on the user's company Slack. As in, add it to your personal DMs, but not have it message everyone. Maybe something like "@suns-out-bot /unmute or /unmute"


## Stretch goals

- [ ] make the API easily access other cityies upon setup in a workspace

## Use cases
- [ ] People in offices with limited window access
- [ ] Gives more time to plan lunch breaks
- [ ] Saves time having to check the weather

## Limitations
- [ ] The weather report can be wrong

## Testing
- [ ] It should send a message at the right time

- [ ] It should send certain messages under certain conditions

- [ ] If those conditions aren't met, it shouldn't send any messages

- [ ] make sure it can have different responses based on user import. If user A tells it to mute, it should stay mute for user A if user B tells it to unmute


## Steps
- [x] finish base bolt tutorial
- [x] make the bot print a "hello world" to a channel
- [ ] make the bot print a "hello world" as a DM - PENDING
- [ ] write tests
    - [ ] test for API response
    - [ ] test for timing
    - [ ] test that message is accurate
- [x] make the bot print at a certain time, day to day
- [x] make bot print according to conditionals
- [x] make bot consume weather API
    - [x] user weatherbit API - I know it works
    - [x] test file can read weather description 
- [x] make bot react to weather API
- [ ] add pause/mute functions

## APIs
- Slack's Socket Mode
- Weather API
- chat.PostMessage API
- 


# How to add to your workspace
- Fork and clone this repo
- Sign up with weatherbit and grab your API key. Doublecheck that you have a `.gitignore` file.
- In your `.env` file, add these elements:
    - `SLACK_BOT_TOKEN`
        - needed for setting up the basic development Slack server
        - Detailed instructions on grabbing it here: 
    - `SLACK_SIGNING SECRET`
        - also needed to set up your Slack development server
        - Detailed instructions on grabbing it here:
    - `BOT_CHANNEL_ID`
        - Enter `https://slack.com/api/conversations.list` into Postman, or ping it from your terminal. It will call the `get_channel_id` function, and return a JSON response with information about the channel. Then, you can copy the value in the `id` section into your `.env` file.
    - `WEATHER_API_KEY`
        - needed to access the weather report. You can change the city/zip code as needed.
        - Found at Weatherbit here: 
- Deployment incoming
- Don't forget to invite `suns-out-bot` to the channel you want it to post to, otherwise you will get an error.

# Change Log

2/16 : upon calling "schedule_weather_trigger", the app will call the function to send a message at the given time. When send_message is called, it will call "check_weather" at that moment, so that the weather report will be as accurate as the API can make it. If the weather is nice enough, a message will be sent to the "general" channel. Next up: make it work as a DM

2/19: Added temperatue to the message the bot sends, so users can have a better sense of whether or not they actually want to go outside.


