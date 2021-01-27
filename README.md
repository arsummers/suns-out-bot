# suns-out-bot
Slack bot that lets you know when it is sunny outside, so you can take a walk or otherwise step outside during your lunch break.

## Core functionality

- [ ] app should ping a weather API for local weather

- [ ] if weather is sunny, if should send a message that it's sunny out, and maybe you should step outside

- [ ] if the weather is any variant of dry, it should send a different message about going out

- [ ] it should send the message at 10:30 or 11:00 AM, so that the user has time to decide if they want to go outside on a break later in the day

- [ ] The app should know the local time

- [ ] should send messages to DMs, so that entire channels won't have to have the reminders if they don't want them

- [ ] should have ability to mute for set periods of time, if possible

- [ ] should have ability to configure the number of notifications per week. Checks weekly weather on Monday morning. If the whole week should be sunny, it can send out only 3 messages/week. Sunny day notifs are more important when they aren't regular.

- [ ] some ability to opt in to the bot on the user's company Slack. As in, add it to your personal DMs, but not have it message everyone. Maybe something like "@suns-out-bot unmute"


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
- [ ] make the bot print a "hello world"
- [ ] write tests
- [ ] make the bot print at a certain time, day to day
- [ ] make bot print according to conditionals
- [ ] make bot consume weather API
- [ ] make bot react to weather API
- [ ] add pause/mute functions

## APIs
- Slack's Socket Mode
- Weather API
- chat.PostMessage API
- 


# How to add to your workspace

Coming soon!

# Change Log

