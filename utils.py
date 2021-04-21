import requests
import sqlite3
import json

from google_api import *
from database import *

###################
# Processing info #
###################
def process_db_data(list_of_data, single_info=False):
    # [(a1, b1x, ...), (a2, b2, ...), ...] -> [[a1, b1x, ...], [a2, b2, ...], ...]
    return [list(data) for data in list_of_data]

def generate_keyword_dict(*args):
    assert len(args)%2 == 0
    keyword_dict = {}
    for i in range(len(args)//2):
        keyword_dict[args[2*i]] = args[2*i+1]
    return keyword_dict

##############################
# Get info by DB or requests #
##############################
def get_processed_db_data(conn, task, *args):
    keyword_dict = generate_keyword_dict(*args)
    infos = retrieve_db_data(conn, task, keyword_dict)
    infos = process_db_data(infos)
    return infos

def get_place_info(conn, place_name):
    task = PLACES
    # Create table of task if not exists
    create_table(conn, task)
    # Check place exits in table or not
    places_info = get_processed_db_data(conn, task, "name", place_name)
    if(len(places_info) == 0):
        # Request place info and Parse place json to info infos
        res_json = find_place_requests(place_name)
        new_infos = parse_find_place_requests(res_json)
        # Choose one place (Actually, there exists only one place)
        new_info = new_infos[0]
        places_info = get_processed_db_data(conn, task, "place_id", new_info[ATTRIBUTES[task]["place_id"]])
        if(len(places_info) == 0):
            # Insert one new row in to table
            insert_info(conn, task, new_info)
            places_info = new_infos

    # places_info = [[place_id, name, address, latitude, longitude]]
    return places_info[0]

def get_nearby_restaurants_info(conn, place_info):
    query_place_id = place_info[ATTRIBUTES[PLACES]["place_id"]]
    lat_place = place_info[ATTRIBUTES[PLACES]["latitude"]]
    lng_place = place_info[ATTRIBUTES[PLACES]["longitude"]]
    task = RESTAURANTS

    create_table(conn, task)
    restaurants_info = get_processed_db_data(conn, task, "query_place_id", query_place_id)
    if(len(restaurants_info) < 5):
        restaurants_info = []
        res_json = nearby_search_requests(lat_place, lng_place)
        new_infos = parse_nearby_search_requests(res_json, query_place_id)
        for new_info in new_infos:
            # Get info of each restaurant from DB
            restaurant_info = get_processed_db_data(conn, task, "place_id", new_info[ATTRIBUTES[task]["place_id"]])
            if(len(restaurant_info) == 0):
                insert_info(conn, task, new_info)
                restaurants_info.append(new_info)
            else:
                restaurants_info.append(restaurant_info[0])

    # restaurants_info = [[place_id, name, addr, latitude, longitude, price_level, 
    #                      rating, user_ratings_total, query_place_id, food_style, food_type], [...], ...]
    return restaurants_info

def get_nearby_specified_restaurants_info(conn, place_info, query, food_style=False, food_type=False):
    query_place_id = place_info[ATTRIBUTES[PLACES]["place_id"]]
    lat_place = place_info[ATTRIBUTES[PLACES]["latitude"]]
    lng_place = place_info[ATTRIBUTES[PLACES]["longitude"]]
    task = RESTAURANTS

    create_table(conn, task)
    if food_style:
        restaurants_info = get_processed_db_data(conn, task, "query_place_id", query_place_id, "food_style", query)
    elif food_type:
        restaurants_info = get_processed_db_data(conn, task, "query_place_id", query_place_id, "food_type", query)
    else:
        restaurants_info = []
    if(len(restaurants_info) < 5):
        restaurants_info = []
        # Request and parse json to lists of restaurants info 
        res_json = text_search_requests(lat_place, lng_place, query)
        new_infos = parse_text_search_requests(res_json, query_place_id, food_style, food_type)
        # For each info, get data from db
        for new_info in new_infos:
            restaurant_info = get_processed_db_data(conn, task, "place_id", new_info[ATTRIBUTES[task]["place_id"]])
            if(len(restaurant_info) == 0):
                insert_info(conn, task, new_info)
                restaurants_info.append(new_info)
            else:
                restaurant_info = update_info(conn, task, new_info, restaurant_info[0])
                restaurants_info.append(restaurant_info)

    # restaurants_info = [[place_id, name, addr, latitude, longitude, price_level, 
    #                      rating, user_ratings_total, query_place_id, food_style, food_type], [...], ...]
    return restaurants_info

def get_all_specified_restaurants_info(conn, place_info):
    restaurants_info = []
    for query in FOOD_STYLES:
        # print(query)
        restaurants_info_this = get_nearby_specified_restaurants_info(conn, place_info, query, food_style=True)
        restaurants_info.extend(restaurants_info_this)
    for query in FOOD_TYPES:
        # print(query)
        restaurants_info_this = get_nearby_specified_restaurants_info(conn, place_info, query, food_type=True)
        restaurants_info.extend(restaurants_info_this)
    return restaurants_info

def get_top_k_restaurant_types(conn, style_or_type="food_style", sort_key="rating", k=5):
    results = retrieve_top_k_restaurant_types(conn, style_or_type, sort_key, k)
    results = process_db_data(results)
    return results

def get_top_k_restaurants(conn, style_or_type, restaurant_type, sort_key="rating", k=10):
    results = retrieve_top_k_restaurants(conn, style_or_type, restaurant_type, sort_key, k)
    results = process_db_data(results)
    return results

def get_top_k_query_restaurants(conn, place_info, query, sort_key="rating", k=10):
    restaurants_info = get_nearby_specified_restaurants_info(conn, place_info, query)
    place_ids = [restaurant_info[ATTRIBUTES[RESTAURANTS]["place_id"]] for restaurant_info in restaurants_info]
    keyword_dict = generate_keyword_dict("place_id", place_ids)
    results = retrieve_top_k_restaurants(conn, "", "", sort_key, k, keyword_dict)
    results = process_db_data(results)
    return results