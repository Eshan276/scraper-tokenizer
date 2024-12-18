import json
import populartimes
import requests

YELP_API_KEY = 'ojbBaWjK9ZeHl1vX7IAFmhhHd2_eeBdKxOin35Zxg5mJpdQWjrdmd4yykA7u6oTwb315ELOXqOBR9nYB-_ookMu3ZwQxPB6hH9qg6ae_3ttLMJz5DHqAhoBtCbFVZ3Yx'
# Client ID
# 9MyUXj06KfiHohj8CigJIg


# API Key
# ojbBaWjK9ZeHl1vX7IAFmhhHd2_eeBdKxOin35Zxg5mJpdQWjrdmd4yykA7u6oTwb315ELOXqOBR9nYB - \
#     _ookMu3ZwQxPB6hH9qg6ae_3ttLMJz5DHqAhoBtCbFVZ3Yx

# def fetch_yelp_data():
#     headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
#     location = "Hicksville, NY"
#     params = {
#         'location': location,
#         'radius': 2000,  # 2 km in meters
#         'categories': 'restaurants',
#         'sort_by': 'rating',
#         'limit': 5
#     }
#     response = requests.get(
#         'https://api.yelp.com/v3/businesses/search', headers=headers, params=params
#     )
#     print(response.json())
#     return response.json()

#################################
def fetch_yelp_data():
    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    location = "Hicksville, NY"
    params = {
        'term': 'Indian restaurant',  # Search specifically for Indian restaurants
        'location': location,
        'radius': 2000,  # 2 km in meters
        'categories': 'restaurants',
        'sort_by': 'rating',
        'limit': 10
    }
    response = requests.get(
        'https://api.yelp.com/v3/businesses/search', headers=headers, params=params
    )

    if response.status_code == 200:
        print(response.json())
        with open('yelp_data.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        return response.json()
    else:
        print(
            f"Error fetching data from Yelp API: {response.status_code}, {response.text}")
        return None

# fetch_yelp_data()

OPENWEATHER_API_KEY = 'e265ff2fc821c78252b5ccf01504ebde'


def fetch_weather_data():
    location = {'lat': 40.7685, 'lon': -73.5251}  # Coordinates of Village
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    weather = response.json()
    print(weather)
    def kelvin_to_fahrenheit(kelvin):
        return (kelvin - 273.15) * 9/5 + 32
    temperature = kelvin_to_fahrenheit(weather['main']['temp'])  
    weather_condition = weather["weather"][0]["description"]
    return {"temperature": temperature, "condition": weather_condition}


GOOGLE_MAPS_API_KEY = 'AIzaSyAf33U05dBvGemX1OG8thdhjaBH-Tyfp8E'


def fetch_busy_times():
    # Fetch place details and busy times
    place_id = "ChIJG33djyO35zsRt5gOkc7GxB8"
    # place_id = "ChIJ14lCIb1hwokR8Y8dk3QRYQ4"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    # print(response.json())
    # print(populartimes.get_id(GOOGLE_MAPS_API_KEY, place_id))
    result = populartimes.get_id(GOOGLE_MAPS_API_KEY, place_id)
    finalresult={}
    current_popularity = result.get('current_popularity')
    if current_popularity:
        print(result)
        print(current_popularity)
        finalresult['busy_level'] = current_popularity
    else:
        finalresult['busy_level'] = 0

    # print(populartimes.get_id(GOOGLE_MAPS_API_KEY, place_id))
    return finalresult

# fetch_busy_times()

# fetch_weather_data()

