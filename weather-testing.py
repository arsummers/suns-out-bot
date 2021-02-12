import requests

def check_weather():
  # should return a weather object from an external API. The bot should should the weather, then, for now, send a message with the current weather.
  # message should say something like "According to my calculations, it is {weather} and {} degrees outside. Today should be a good day to get outside for fresh air on your lunchbreak."

    url = "http://api.open-notify.org/astros.json" #will change to weather once I decide on one
    response = requests.get(url)
    json_info = response.json()
    people_obj = json_info["people"]

    for item in people_obj:
        print(item['name'])


    print(f'Response JSON: {json_info}') #returns a json response for the basic API info
    # print(f'Exact: {people_obj')

 




check_weather()