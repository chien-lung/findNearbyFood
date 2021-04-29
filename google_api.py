import requests
import json

import secrets

FOOD_STYLES = ["American", "Chinese", "French", "Indian", "Italian", "Japanese", "Mexican", "Thai"]
FOOD_TYPES = ["Barbecue", "Hamburger", "Pizza", "Seafood", "Steak", "Sushi"]

################
# Requests API #
################

# Find Place Requests
def find_place_requests(place = "Ann Arbor"):
    print(f"Find Place Requests for query \"{place}\"")
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    query = {
        "input": place,
        "inputtype": "textquery",
        "key": secrets.GOOGLE_API_KEY,
        "fields": "name,place_id,formatted_address,geometry"
    }
    response = requests.get(base_url, query)
    response_json = response.json()
    return response_json

# Nearby Search Requests
def nearby_search_requests(lat="42.2808256", lng="-83.7430378", radius=1000):
    print("Nearby Search Requests")
    loc = f"{lat},{lng}"
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    query = {
        "location": loc,
        "radius": radius,
        "key": secrets.GOOGLE_API_KEY,
        "type": "restaurant"
    }
    response = requests.get(base_url, query)
    response_json = response.json()
    return response_json
    
# Text Search Requests
def text_search_requests(lat, lng, query):
    print("Text Search Requests")
    loc = f"{lat},{lng}"
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = {
        "query": query,
        "key": secrets.GOOGLE_API_KEY,
        "location": loc,
        "radius": "1000",
        "type": "restaurant"
    }
    response = requests.get(base_url, query)
    response_json = response.json()
    return response_json

# Place Details Requests
def place_details_requests(place_id = "ChIJZbsiYBOuPIgRwBPyXagDZuw"):
    print("Place Details Requests")
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    query = {
        "place_id": place_id,
        "key": secrets.GOOGLE_API_KEY,
        "fields": "name,vicinity,formatted_phone_number,opening_hours,price_level,rating,review,user_ratings_total,url",
    }
    response = requests.get(base_url, query)
    response_json = response.json()
    return response_json

##################
# Parse requests #
##################

def parse_find_place_requests(res_json):
    places_info = res_json["candidates"]
    new_infos = []
    for place_info in places_info:
        place_id = place_info["place_id"]
        name = place_info["name"]
        addr = place_info["formatted_address"]
        latitude = place_info["geometry"]["location"]["lat"]
        longitude = place_info["geometry"]["location"]["lng"]
        new_infos.append([place_id, name, addr, latitude, longitude])
    return new_infos

def parse_nearby_search_requests(res_json, query_place_id, food_style="null", food_type="null"):
    restaurants_info = res_json["results"]
    new_infos = []
    for restaurant_info in restaurants_info:
        place_id = restaurant_info["place_id"]
        name = restaurant_info["name"]
        try:
            addr = restaurant_info["vicinity"]
        except: # for parse_text_search_requests
            addr = restaurant_info["formatted_address"]
        latitude = restaurant_info["geometry"]["location"]["lat"]
        longitude = restaurant_info["geometry"]["location"]["lng"]
        try:
            price_level = restaurant_info["price_level"]
        except:
            price_level = "null"
        rating = restaurant_info["rating"]
        user_ratings_total = restaurant_info["user_ratings_total"]
        new_infos.append([place_id, name, addr, latitude, longitude, price_level, rating, user_ratings_total, query_place_id, food_style, food_type])
    return new_infos

def parse_text_search_requests(res_json, query_place_id, query, food_style, food_type):
    if not food_style:
        food_style = "null"
    else:
        food_style = query
    if not food_type:
        food_type = "null"    
    else:
        food_type = query
    return parse_nearby_search_requests(res_json, query_place_id, food_style, food_type)

def parse_place_details_requests(res_json, place_id):
    place_detail = res_json["result"]
    name = place_detail["name"]
    try:
        phone = place_detail["formatted_phone_number"]
    except:
        phone = "null"
    try:
        open_hours = place_detail["opening_hours"]["weekday_text"]
        open_hours = ";".join(open_hours)
    except:
        open_hours = "null"

    info = [place_id, name, phone, open_hours]

    reviews = place_detail["reviews"]
    for i in range(3):
        if i < len(reviews):
            author_name = reviews[i]["author_name"]
            author_rating = reviews[i]["rating"]
            author_text = reviews[i]["text"]
        else:
            author_name = "null"
            author_rating = "null"
            author_text = "null"
        info.extend([author_name, author_rating, author_text])
    return [info]

if __name__ == "__main__":
    # query_place_id = "ChIJMx9D1A2wPIgR4rXIhkb5Cds"
    # lat = "42.2808256"
    # lng = "-83.7430378"
    # query = FOOD_TYPES[-1]
    # res_json = text_search_requests(lat, lng, query)
    # new_infos = parse_text_search_requests(res_json, query_place_id, False, False)

    place_id = "ChIJ8W1G1UWuPIgR6Jetrkwtshk"
    # place_id = "ChIJTxLiLIquPIgRa4irrQUvsRw"
    res_json = place_details_requests(place_id)
    results = parse_place_details_requests(res_json, place_id)
    print(results)