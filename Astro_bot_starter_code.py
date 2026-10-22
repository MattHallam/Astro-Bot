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
import base64 #needed as the astronomy API expects the ID and secret to be encoded for the header
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
    return input(f"Enter your {prompt}: ")  if choice == "n" else hardcoded_key 
#gets API key if not using hard-coded, 'return' sends the inputed value back to where the function is called. checks to see if the hard-coded key is being used or not and returns the hardcoded-key if it is

def get_astronomy_auth():
    astronomy_id = 437cc773-eebf-44ab-bc13-531b37e85e12
    astronomy_secret = input("Enter your Astronomy API secret: ")

userpass = f"{astronomy_id}:{astronomy_secret}"
auth_String = base64.b64encode(userpass.encode()).decode()

return f"basic {auth_string}"
    
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

    timestamp = time.time() #gets current epoch timestamp
    human_time = time.ctime(timestamp) #converts epoch timestamp into readable time

    location = reverse_geocode(lat, lon, api_key) #sends ISS coordinates to reverse-geocoding function

    place = "Over Ocean / No Nearby City"

    if location: #checks if reverse geocoding has returned data
        place = location.get("name", "Over Ocean / No Nearby City") #place = location.get("name", = gets the name of the location the ISS is in, if there is no data, over ocean/no nearby city is used
#
    return (
        f"ISS location: latitude {lat}, longitude {lon}. Nearby place: {place}. Time: {human_time}" 
    )

# ========================
# ASTRONOMY API (ADDITIONAL TASK)
# ========================
def get_sky_info(city, weather_api_key, astronomy_auth):

    location = get_city_coordinates(city, weather_api_key)
    if not location:
        return "city not found."

    latitude = location ["lat"]
    longitude = location ["lon"] 

    timestamp = time.time() #gets current epock timestap
    human_time = time.ctime(timestamp) #converts timestamp into readable time
    date = time.strftime("%Y-%m-%d", time.localtime(timestamp)) #strftime converts the date into a string and the format '%y-%m-%d' seperates it into year, month, and day
    current_time = time.strftime("%H:%M:%S", time.localtime(timestamp)) #strftime does the same thing but with the time and the format '%H:%M:%S' seperates it into hour, minute, and second
    #these values are needed later on in the code to give to the API so it knows what information to give from the time and date given
    
    url = "https://api.astronomyapi.com/api/v2/bodies/positions" #astronomy API endpoint 
    headers = {"Authorization": astronomy_auth} #tells the API who is making the request, authorization tells the API authentication details are included, and astronomy_auth contains the authentication from the configurations
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "elevation": 0,
        "from_date": date,
        "to_date": date,
        "time": current_time,
        "output": "rows" #requests the response in a rows format
    } #these set parameters tells the API what information you want from it which includes the coordinates, locations height above sea level, the start and end date of the calculate, and the time for the calculation
  
    response = requests.get(url, headers=headers, params=params) #sends a GET request to the API using the url to find the destination, the headers to authenticate the requst, and the params include the information requested

    if response.status_code == 403:
        return "Astronomy API authentication failed. Check your Application ID and Secret." #if the authentication is incorrect it is due to code 403, so this provides an explaination for a common issue
    elif response.status_code != 200:
        return f"Unable to retrieve astronomy data. Status code: {response.status_code}" #checks the response code to see if the API has been successful or not

    data = response.json() #converts the APIs data (JSON) into python so the program can understand the data
    rows = data.get("data", {}).get("rows", [])  #looks for 'data' key and uses an empty dictionary {} if it doesnt exist, then looks for 'rows' inside the dictionary and uses and empty list [] if it dosent exist
    if not rows: #checks if the rows are empty
        return "No astronomy information was returned."  #if there are no rows, this message is returned

    message = f"Sky information for {city}:\n" #this is the format for the message printed by the bot, \n gives a new line for new information

    for row in rows: #for loop allows the program to process each row of the APIs response one at a time
        body = row.get("body", {}) #uses a get request to get data about the celestial body (e.g. star, moon, plant)
        positions = row.get("positions", []) #uses the same request to get a list of positins related to the body from the API

        if not positions:
            continue #if there are no positions the loop is skipped as to not create an infinite loop

        position = positions[0] #select the fist item in the positions list

        name = body.get("name", "unknown") #gets the name of the celestial body, if the key is missing ("name") it defaults to "unknown"

        horizontal = position.get("position", {}).get("horizontal", {}) #extrats the 2 values (position and horizontal) from the JSON data
        altitude = horizontal.get("altitude", {}).get("degrees", "N/A") 
        azimuth = horizontal.get("azimuth", {}).get("degrees", "N/A") #looks for the further data and if it is missing N/A is used instead

        message += ( #adds the information to the existing message from line 221 using += 
            f"{name}: "
            f"Altitude {altitude}°, "
            f"Azimuth {azimuth}°\n" 
        )

    return message #returns the finished message with all the data added after getting it from the JSON data

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

            elif message_text.lower().startswith("/sky"):#checks to see if the message type starts with /sky (a correct command)
                parts = message_text.split(maxsplit=1) #splits message into parts and creates a list out of the 2 items

                if len(parts) < 2: #checks to see if there are 2 items in the list
                    send_message(token, room_id, "Usage: /sky <city>") #sends a prompt to enter a city after /sky if only /sky is intered
                else:
                    city = parts[1] #stores index 1, the second item in the list, as the variable city

                    send_message( #calls the function from the webex functions
                        token, #provides the webex access token
                        room_id, #checks for a room_id
                        get_sky_info( #calls the function for the astronomy API
                            city, #provides the city entered
                            weather_key, #provides the weather api key as this is used to get the lon and lat
                            astronomy_auth #provides the astronomy api key
                        )
                    )#
            
            elif message_text.lower() == "/quit":
                send_message(token, room_id, "AstroBot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help")

        time.sleep(5)

if __name__ == '__main__':
    main()
