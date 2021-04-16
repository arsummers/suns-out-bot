# suns-out-bot
Slack bot that lets you know when it is sunny outside, so you can take a walk or otherwise step outside during your lunch break.

## Core functionality

- [x] app should ping a weather API for local weather

- [x] if weather is sunny or otherwise dry, if should send a message that it's sunny out, and maybe you should step outside

- [x] it should send the message around lunch time, so that the user has accurate information

- [x] The app should know the local time

## Stretch goals

- [ ] should send messages to DMs, so that entire channels won't have to have the reminders if they don't want them - DEBATABLE. Might be best to send to bot channel.

- [ ] should have ability to mute for set periods of time, if possible


- [ ] some ability to opt in to the bot on the user's company Slack. As in, add it to your personal DMs, but not have it message everyone. Maybe something like "@suns-out-bot /unmute or /unmute"

- [ ] make the API easily access other cities upon setup in a workspace

## Use cases
-  People in offices with limited window access
-  Gives people accurate weather reports on their lunch breaks
-  Saves time having to check the weather

## Limitations
- The weather report can be wrong
- The timing on the scheduler syncs up with Greenwich Standard Time when deployed, so the time will have to be adjusted manually.
- Can't currently support multiple locations per bot instance

## Testing
- [ ] It should send a message at the right time

- [ ] It should send certain messages under certain conditions

- [ ] If those conditions aren't met, it shouldn't send any messages

- [ ] make sure it can have different responses based on user import. If user A tells it to mute, it should stay mute for user A if user B tells it to unmute

## APIs and Major Libraries
- Slack's Bolt library
- Weatherbit API
- chat.PostMessage API
- APScheduler
    - docs [here](https://apscheduler.readthedocs.io/en/stable/faq.html)

# How to add to your workspace
- Fork and clone this repo
- Sign up with Slack as a developer
- Add these scopes to your bot:
    - chat:write
    - channels:read
    - incoming-webhook

- Sign up with weatherbit and grab your API key [here](https://www.weatherbit.io/).
- Doublecheck that you have a `.gitignore` file.
- create a `.env` file for your secret keys
- In your `.env` file, add these elements:
    - `SLACK_BOT_TOKEN`
        - needed for setting up the basic development Slack server
        - Detailed instructions on setting up and grabbing your bot user token [here](https://api.slack.com/authentication/token-types)
    - `SLACK_SIGNING SECRET`
        - also needed to set up your Slack development server
        - Instructions on grabbing that [here](https://api.slack.com/authentication/verifying-requests-from-slack#signing_secrets_admin_page):
    - `BOT_CHANNEL_ID`
        - comment `get_channel_id` back in at the bottom of `app.py`
        - run `python app.py`
        - Enter `https://slack.com/api/conversations.list` into Postman, or ping it from your terminal. It will call the `get_channel_id` function, and return a JSON response with information about the channel. Then, you can copy the value in the `id` section into your `.env` file.
    - `WEATHER_API_KEY`
        - needed to access the weather report. You can change the city/zip code as needed.
        - Found at Weatherbit [here](https://www.weatherbit.io/)
    - `ZIP_CODE`
        - This is needed so that the weatherbit API can know which location to check. Zip code is more exact and handles duplicates better than a city name.

- While in development mode, you will need to run `export YOUR_ENV_KEY=YOUR_ENV_VALUE` in the terminal for each item in the list above, e.g. `export ZIP_CODE=12345`

- Don't forget to invite `suns-out-bot` to the channel you want it to post to, otherwise you will get an error.

## Deploy on Digital Ocean
- Copy the contents of these files, and move them to your github repo so they can be deployed
    - app.py
    - suns_out.py
    - requirements.txt
    - Pipfile.lock
    - .gitignore
- run `pipenv install` for good measure
- log in or create an account and go to the green **Create** tab
- Create a new app
- Follow the steps to link up your repo up to digital ocean
- You should be fine on the $5/month plan
- When prompted, fill in your `env` values and continue to the final screen to deploy
- Then you should be good to go! 


- If you want to easily test that this is working, I've left in some commented out code that will run every minute, so you won't have to wait until your specified time for a reaction. It is under the `schedule_weather_trigger` function inside `suns_out.py`

# Change Log

2/16 : upon calling "schedule_weather_trigger", the app will call the function to send a message at the given time. When send_message is called, it will call "check_weather" at that moment, so that the weather report will be as accurate as the API can make it. If the weather is nice enough, a message will be sent to the "general" channel.

2/19: Added temperatue to the message the bot sends, so users can have a better sense of whether or not they actually want to go outside.

3/1: Functionality is all here. Updated weatherbit API URL to take zipcodes instead of cities. Will give a more accurate weather report, and handles cities that share names with other cities, such as Portland, Oregon vs Portland, Maine.

3/15: Still not happy with how the scheduler runs. Might have to look into cron jobs, or some type of recursive scheduling. Best way might be to just make it sleep for 1 day between calls.

3/30: have testing loop ready for scheduler, ready to try deploying. If successful, can bring in daily loop on next deploy push

### Various sources and references

- [Getting started with Slack and Python](https://api.slack.com/start/building/bolt-python)
- [Additional tutorial for Slack and Python](https://www.digitalocean.com/community/tutorials/how-to-build-a-slackbot-in-python-on-ubuntu-20-04)
- [Deploying Slackbot to Digital Ocean - video](https://www.youtube.com/watch?v=FdXS-NpxtSo)