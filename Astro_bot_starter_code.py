#Contains partially completed code with sections for you to complete
#IT IS MANDATORY TO USE THE RESOURCE PROVIDED
#The starter code is structured into functions and modules. You are required to complete the missing sections while maintaining this modular design.  Further step by step instructions can be found in the appendix A of this assignment brief. 
#For extended features implement it within the existing modular structure. The new feature must be triggered using a new command (e.g., /stars, /moon, /sky) and follow the same approach 
#Use Git for version control. Maintain a repository on GitHub to track your project’s progress and changes. Ensure regular commits for each step with meaningful messages that document your step by stepdevelopment process. 

# =========================
# REQUIRED LIBRARIES
# =========================

import requests #lets python communicate with websites and APIs
import json #lets python language convert into JSON text so the API can understand it
import time #makes sure the bot waits before checking Webex for new messages rather than repeatedly making requests
from datetime import datetime

# =========================
# CONFIGURATION FUNCTIONS
# =========================
def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ")
        return f"Bearer {token}"
    else:
        return "Bearer YOUR_WEBEX_TOKEN"

def get_api_key(prompt, hardcoded_key):
    choice = input(f"use hard-coded {prompt}? (y/n): ").lower() #asks user if they are using a hard-coded key or not
    return input(f"Enter your {prompt}: ")  #gets API key if not using hard-coded, 'return' sends the inputed value back to where the function is called
    if choice == "n" else hardcoded_key #checks to see if the hard-coded key is being used or not and returns the hardcoded-key if it is

# =========================
# WEBEX FUNCTIONS
# =========================
def get_rooms(token):
    url = "https://webexapis.com/v1/rooms" #webex endpoint for getting rooms
    headers = {"Authorization": token} #tells webex which token is making the request
    response = requests.get(url, headers=headers) #sends a GET request to webex and stores the result in 'response' which contains status code, returned data, and JSON information

    if response.status_code != 200: #!= 200 means does not equal 200, so this means if the get requests http code does not equal 200 (success) something is wrong
        print("Error fetching rooms:", response.status_code)
        return []

    return response.json().get("items", [])


def print_rooms(rooms):
    for room in rooms:
        print(f"{room['title']} - {room['id']}") #this displays the Astrobots room title and ID using {} brackets as placeholders due to the f string and [] brackets as a key to grab values from the words inside


def select_room(rooms):
    while True:
        name = input("Enter room name: ") #enter the name of the room
        for room in rooms:
            if name.lower() in room["title"].lower():
                print(f"Selected room: {room['title']}") #prints the title of the room selected
                return room["id"]
        print("Room not found, please try again") #if the name entered in 'name' dosent exit this message will be printed


def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages" #webex messages API endpoint
    params = {"roomId": room_id, "max": 1} #room_id identifies the room via its ID, to webex and '"max": 1' tells webex only return one message from the room
    headers = {"Authorization": token} #supplies the webex access token again to webex knows who is making the request

    response = requests.get(url, headers=headers, params=params) #sends the request to webex, params is included so webex knows the room ID and maximum number of messages

    if response.status_code != 200:
        return None, None

    data = response.json().get("items", [])

    if not data:
        return None, None

    latest = data[0]
    return latest.get("id"), latest.get("text", "")


def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages" #same API endpoint as 'get' but instead sending (post) rather than retrieving
    headers = {"Authorization": token, "Content-Type": "application/jsons"} #2 headers: Authorization identifies the user, Content-type tells webex the data being sent is JSON
    data = {
        "roomId": room_id,
        "text": message
    }
    requests.post(url, headers=headers, data=json.dumps(data)) #post is used instead of get as data is being sent, json.dumps(data) = used to convert the pyhton dictionary into JSON

# =========================
# WEATHER FUNCTIONS
# =========================
def get_city_coordinates(city, api_key):
    url = "https://api.openweathermap.org/geo/1.0/direct" #openweathermap API endpoint (converts a city name into coordinates providing you have an API key)
    params = {"q": city, "limit": 1, "appid": api_key} #3 params, q= city being searched for, limit= tells the API how many locations to return, appid= gives the API the key
    response = requests.get(url, params=params) #sends the request to openweather using 'get'

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_weather(city, api_key):
    location = get_city_coordinates(city, api_key)

    if not location:
        return "city not found" #if no location is found the bot will recieve this message rather than continuously giving missing coordinates

    url = "https://api.openweathermap.org/data/2.5/weather" #this is the API where the weather comes from
    params = {"lat": location["lat"], "lon": location["lon"], "units": "metric", "appid": api_key} # {} create a dictionary while [] brackets look up values for the variables given
    #lat= gets the latitude, lon= gets the longitude, units requests metric measurements, and appid gets the API key which was previously entered

    response = requests.get(url, params=params) #sends the request to openweather using 'get'

    if response.status_code != 200:
        return "unable to retrieve weather data" #if the API dosent return status code 200 (success) the function gives this message to the bot

    weather = response.json()

    return (
        f"Weather in {weather['name']}, {weather['sys']['country']}:" #'name' gets the name of the city from a preexisting dictionary. 'sys' accesses a dictory and 'country' gives the value stored as 'country' e.g. GB for the city London
        f"{weather['main']['temp']}°C," #'main' accesses a dictionary storing the temperature and 'temp' gets the value stored for temperature in the 'main' dictionary
        f"{weather['weather'][0]['description']}."#works the same way, 'weather' accesses a dictionary and 'description' acceses the value but '0' gives the first item stored in the list as a list is used     
        f"Humidity: {weather['main']['humidity']}%." #'main' accesses the same dictionary as before but 'humidity' gets the value stored for humidity in the 'main' dictionary
        f"Wind speed: {weather['wind']['speed']} m/s" #'wind' accesses a dictionary storing the speed and 'speed' gets the value stored for speed in the 'wind' dictionary
    )

# =========================
# ISS FUNCTIONS
# =========================
def reverse_geocode(lat, lon, api_key):
    url = "https://api.openweathermap.org/geo/1.0/reverse" #url link for reverse geocode
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key} #supplies the latitude, longitude, maximum results (1), and the API key

    response = requests.get(url, params=params) #uses a get request to get the openweathermap API to find a location near the international space station coordinates

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_iss_location(api_key):
    url = "http://api.open-notify.org/iss-now.json" #open notify API endpoint

    response = requests.get(url) #request does not have params due to no API key 

    if response.status_code != 200:
        return "error, Unable to retrieve ISS location"

    data = response.json()

    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"] #gets the ISS latitude and longitude from the JSON data provided by the API

    location = reverse_geocode(lat, lon, api_key) #sends ISS coordinates to reverse-geocoding function

    place = "Over Ocean / No Nearby City"

    if location: #checks if reverse geocoding has returned data
        place = location.get("name", "Over Ocean / No Nearby City") #place = location.get("name", = gets the name of the location the ISS is in, if there is no data, over ocean/no nearby city is used
#
    return (
        f"ISS location: latitude {lat}, longitude {lon}. Nearby place: {place}" 
    )

# =========================
# MAIN BOT LOGIC
# =========================
def main():

    token = get_webex_token()

    weather_key = get_api_key(
        "Weather API key",
        "YOUR_OPENWEATHER_API_KEY"
    )

    rooms = get_rooms(token)

    if not rooms:
        print("no webex rooms found or unable to get rooms.") #if webex cant find any rooms the program tells the user this message
        return

    print_rooms(rooms)
    room_id = select_room(rooms)

    last_message_id, _ = get_latest_message(token, room_id)

    while True:

        message_id, message_text = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id:

            last_message_id = message_id
 
            print(f"Received {message_text}") #every time the bot revieves a message this is printed to let the user know the message has been recieved

            if not message_text.startswith("/"): #checks to see if the message sent into the bot is a command (beginning with /)
                continue

            if message_text.lower() == "/help":
                send_message(
                    token,
                    room_id,
                    "/weather <city>\n/iss\n/help\n/quit"
                )

            elif message_text.lower().startswith("/weather"): #checks to see if the messages starts with /weather 

                parts = message_text.split(maxsplit=1)

                if len(parts) < 2:
                    send_message(token, room_id, "Usage: /weather <city>")
                else:
                    city = parts[1]
                    send_message(token, room_id, get_weather(city, weather_key))

            elif message_text.lower() == "/iss":
                send_message(token, room_id, get_iss_location(weather_key)) #checks to see if the user typed /iss and if so, the bot runs 'get_iss_location(weather_key)' and sends the result to Webex

            elif message_text.lower() == "/quit":
                send_message(token, room_id, "AstroBot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help")

        time.sleep(5)


if __name__ == '__main__':
    main()
