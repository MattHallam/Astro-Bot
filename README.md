# 🚀 Space Bot API Investigation Sheet

**Total Marks: 40**  
**TASK 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, **Weather API** and a **Geocoding API** , plus the Python time module. Also furhter investigate the application of Web Architecture and MVC design pattern in development of the Bot

---

##  Webex Messaging API (4 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `An authorization HTTP header is used to identify the requesting user. The header must include an access token which may be personal, a bot token, or an Authorisation token from an integration` |
| Endpoint to list rooms | `GET https://webexapis.com/v1/rooms` |
| Endpoint to get messages | `GET https://webexapis.com/v1/messages>` |
| Endpoint to send message | `POST https://webexapis.com/v1/messages` |
| Required headers | `{"Authorization": token, "Content-Type": "application/jsons"}` |
| Sample full GET or POST request | `requests.get(url, headers=headers)` |

---

##  ISS Current Location API (2 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org/iss-now.json` |
| Endpoint for current ISS location | `get http://api.open-notify.org/iss-now.json` |
| Sample response format (example JSON) |  
```
{
    "message": "success",
    "timestamp": 1720000000,
    "iss_position": {
        "latitude": "51.5074",
        "longitude": "-0.1278"
    }
}
```
|

---

##  Geocoding API (4 marks)

| Criteria | Details |
|---------|---------|
| Provider used (Choose one) | 'OpenWeatherMap' |
| API Base URL | `https://api.openweathermap.org` |
| Endpoint for geocoding | `https://api.openweathermap.org/geo/1.0/direct` |
| Endpoint for reverse geocoding | `https://api.openweathermap.org/geo/1.0/reverse` |
| Authentication method | `API key using the 'appid' parameter` |
| Required query parameters | `direct:q, limit, appid. reverse: lat,lon, limit, appid` |
| Sample request with latitude/longitude | `requests.get("https://api.openweathermap.org/geo/1.0/reverse"), params ={"lat": 51.5074, "lon": -0.1278, "limit": 1, "appid": api_key} ` |
| Sample JSON response (formatted example) |  
```
[
    {
        "name": "London",
        "local_names": {
            "en": "London"
        },
        "lat": 51.5074,
        "lon": -0.1278,
        "country": "GB",
        "state": "England"
    }
]
```
|

---


##  Weather API (3 marks)

| Criteria | Details |
|---------|---------|
| API Provider (Choose one) | 'OpenWeatherMap' |
| API Base URL | `https://api.openweathermap.org` |
| Endpoint for current weather | `https://api.openweathermap.org/data/2.5/weather` |
| Authentication method | `api key using the appid paramter` |
| Required query parameters | `lat, lon,units, appid` |
| Sample JSON response (formatted example) |  
```
{
    "name": "London",
    "sys": {
        "country": "GB"
    },
    "main": {
        "temp": 15.5,
        "humidity": 72
    },
    "weather": [
        {
            "description": "light rain"
        }
    ],
    "wind": {
        "speed": 4.1
    }
}
```
|

---

##  Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `time` |
| Function used to convert epoch | `time.ctime()` |
| Sample code to convert timestamp | `time.ctime(timestamp)` |
| Output (human-readable time) | `Mon Oct 19 12:00:00 2026` |

---

##  Extended Feature API ( 3 marks)

| Criteria | Details |
|---------|---------|
| API Provider | 'Astronomy API' |
| API Base URL | `https://api.astronomyapi.com` |
| Endpoint | `https://api.astronomyapi.com/api/v2/bodies/position` |
| Authentication method | `HTTP Basic using API application ID and secret, encoded using import base64` |
| Required query parameters | `latitude, longitude, elevation, from_date, to_date, time, output` |
| Sample JSON response (formatted example) |  
```
{
    "data": {
        "rows": [
            {
                "body": {
                    "name": "Sun"
                },
                "positions": [
                    {
                        "position": {
                            "horizontal": {
                                "altitude": {
                                    "degrees": "25.5"
                                },
                                "azimuth": {
                                    "degrees": "180.2"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }
}
```
|

--- 

##  Evaluation – Web Architecture, MVC Design & Security 

In this section, evaluate how web technologies, architecture, and design patterns have been applied in your **AstroBot**. Your responses must relate directly to your implementation and include reflection on your design decisions.

---

###  Web Architecture – Client–Server Model (3 marks)

Explain how the client–server model applies to your AstroBot:

- Client: The user using the program to interact with the Astrobot through the Webex messaging room.  
- Servers: The Webex API server, OpenWeatherMap server, Open Notify ISS server, and Astronomy API server, which process requests and return data
- Data flow: user sends a command in the webex chat room, Astrobot retrieves the message using a GET request, the command is process and the appropriate API is contact, providing all checks have passed (status code and authorisation) the JSON data is processed into a message that can be returned back to the webex chat room using the POST request

<img width="317" height="479" alt="block diag" src="https://github.com/user-attachments/assets/128497cd-7477-4ab8-a811-6ca3b446174f" />


####  Security Considerations: (3 marks )
- Secure Handling of API tokens and keys: the bot gets the webex token, weather API key and Astronomy API secret using get_webex_token(), get_api_key(), and get_astronomy_auth() aswell as giving the option for hard-coded credentials. In real life, credentials shoupld be stored securely and should never been shared.
- Api rate limiting: the code uses time.sleep(5) to wait 5 seconds between message checks so constant messages arent being sent. this stops http code 429 which would mean to many requests.
- input validation: the code checks the commands in different ways such as for /weather and /sky it makes sure there are 2 words. if the message sent is invalid it returns an error message suggesting to use /help.

---

###  RESTful API Usage in Your Application (3 marks )

Explain how REST APIs are used in your AstroBot: 

- HTTP methods used: GET = retrieves information from an API. e.g. get_weather() gets current weather data from OpenWeatherMap using requests.get(). POST = sends data to an API. e.g. send_message() sends a message to the Astrobots webex room using requests.post()
-  Astrobot interacting with APIs: 
webex API = get_rooms() gets available rooms, get_latest_message() retrieves the message inputed by the user, send_message() posts a response to the room.
weather API = get_weather() gets current weather conditions which include the temperature, humidity, and wind speed.
ISS API = gets_iss_location() gets the international space stations current lat and lon and epoch timestamp from open notify.
geocoding API = get_city_coordinates() converts the city that has been inputted into a lat and a lon which is then converted into a nearby place name by reverse_geocode().
astronomy API = get_sky_info() gets data about the positions of astronomical bodies in the sky (their altitude adn azimuth) using the lat and lon from get_city_coordinates() .
- JSON response processing: the code converts the JSON response into python language such as dictionaries and lists using response.json(). I then extracted these values from the response and formated them into a readable response e.g. 'return (f"ISS location: latitude {lat}, longitude {lon}. Nearby place: {place}") .
 

#### Security Considerations: (2 marks)
- Checking status codes: the Astrobot checks if requests retun a successfull HTTP status code (200) and if not it returns an error message preventing unsuccessful responses being prrocessed. e.g. get_weather() uses 'response.status_code != 200'.
- handling unexpected responses and avoiding excessive API calls: the Astrobot checks for empty messages before continuing aswell as waiting 5 seconds between attempts using 'time.sleep(5)'.

---

###  MVC Design Pattern in AstroBot (3 Marks)

Explain how the **Model–View–Controller (MVC)** pattern applies to your solution:
Provide a short example based on your implementation

| Component   | Description and Example (Relate to your Bot) |
|------------|----------------------------------|
| **Model**  | Handles the data and API interactions. get_weather(), get_iss_location(), get_city_coordinates(), and get_sky_info() are all functions that retrieve data from different APIs and process the it via extracting and storing it in variables in dictionarys before being returned to the user. e.g. get_weather() gets the city that was entereds coordinates out of a stored dictionary returned by get_city_coordinates() and sends them to the OpenWeatherMap API to get the current weather information. |
| **View**   | Responsible for what the user sees. In my Astrobot, this is the messages sent to the Webex room using send_message(). e.g. when a user enters /weather london the code converts the JSON data using 'data = json.dump(data)' to a readable message before sending this back |
| **Controller** | handles what the user inputs into the program and decides what actions need to be performed. This is done by main() as it checks the commands used (/weather, /sky, /iss, /help, and /quit) before calling the appropriate function from the model |

---

### 📝 Reflection and Evaluation ( 8 marks )

Reflect on your AstroBot (400 words):

Overall, I believe my Astrobot is effective in meeting the Astronomy club's needs due to it providing members with a simple method to obtain astronomical information by simple typing requests into the webex chat room. The bot accepts simple commands (/weather, /iss, and /sky) in order to access things such as the weather in a provided location, the location of the international space station aswell as the location of planets (including the sun, moon and pluto) in our solar system in the sky above a certain city entered which is the main purpose of the club (stargazing events). The Astrobot is made even simpler with the addition of the /help command which tells the users how to use the bot in order to obtain requested information.

One Design decision that worked well was ensuring every function is loosely coupled so that dependencies of functions on other functions is minimised allowing for failures to be clearly identified such as certain HTTP errors or authentication errors. This will allow quick and easy fixes so that the astronomy club can effectively use the Astrobot for their required tasks. Using dictionarys to process JSON data was also an effective design choice for the code itself as the JSON data (how APIs return information) is structured heavily using dictionaries.

One of the main challenges I faced was integrating the extension API (Astronomy API) into my code. This was because I struggled to figure out how to retrieve to JSON data from the API so i could format a message to the user. To solve this i used a 'for' loop to process each row of the data one at a time by firstly extracting the name of the celestrial body from the dictionary inside of the first dictionary and then extracting the list of positions related to that celestial body. Another challenge within the Astronomy API was the error handling as the API request sometimes failed due to an incorrect ID and/or secret.

One of the main security risks was the leaking of API keys, secrets, and tokens as the Astrobot uses these to get data from the related API. In order to not expose these publicily the codes should never be shared or uploded to github and should be stored saftely elsewhere only to be used during testing.

My solution could be improved in the future by adding more astronomy information such as meteor showers, galaxies in current view, or sunrise times/sunset times. These would allow the Astronomy club to greater study and understand how astronomical bodies and different planetary features work. Input validation could also be improved in the configuratoin functions due to the bot sometimes failing if an incorrect message is sent into the hard-coded option. 

---

 **Tip:** Link your answers directly to your code and examples for higher marks.
### Notes

-'https://developer.webex.com/messaging/docs/authentication' = provided information about webex authentication
-'https://openweathermap.org/api/one-call-4?collection=one_call_api' = provided information about the openweathermap API including direct and reverse geocoding
-'http://open-notify.org/Open-Notify-API/ISS-Location-Now/' = provided information about ISS API 
-'https://docs.astronomyapi.com/' = provided information about the extension astronomy API and how to authenticate it.
-'https://www.epochconverter.com/' = provided information about how to use the epoch to human time converter
-'https://www.geeksforgeeks.org/python/how-to-convert-python-dictionary-to-json/' = helped me understand how to convert JSON data to pyhton dictionaries

---

###  Total: /40
