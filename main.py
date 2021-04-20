import requests
import sqlite3
import json

from google_api import *
from database import *

def get_place_info(conn, place):
    task = PLACES
    # Create table of task if not exists
    create_table(conn, task)
    # Check place exits in table or not
    place_info = get_db_data(conn, task, keyword=place)
    if(len(place_info) == 0):
        # Request place info
        res_json = find_place_requests(place)
        # Parse place json to info rows
        new_infos = parse_find_place_requests(res_json)
        # Choose one place (Actually, there exists only one place)
        new_info = new_infos[0]
        # Check info row exits or not
        place_info = get_db_data(conn, task, new_info)
        if(len(place_info) == 0):
            # Insert one new row in to table
            insert_info(conn, task, new_info)
            place_info = new_info
        else:
            # [(id, a, b,...)] -> [a, b, ...]
            place_info = list(place_info[0])
    else:
        # [(id, a, b,...)] -> [a, b, ...]
        place_info = list(place_info[0])

    # place_info = [name, place_id, address, latitude, longitude]
    return place_info

def get_nearby_restaurants_info(conn, place_info):
    query_place_id = place_info[0]
    lat_place, lng_place = place_info[3], place_info[4]
    task = RESTAURANTS

    create_table(conn, task)
    restaurants_info = get_db_data(conn, task, keyword=query_place_id)
    if(len(restaurants_info) < 5):
        restaurants_info = []
        res_json = nearby_search_requests(lat_place, lng_place)
        new_infos = parse_nearby_search_requests(res_json, query_place_id)
        for new_info in new_infos:
            # Get info of each restaurant from DB
            restaurant_info = get_db_data(conn, task, new_info)
            if(len(restaurant_info) == 0):
                insert_info(conn, task, new_info)
                restaurants_info.append(new_info)
            else:
                restaurants_info.append(list(restaurant_info[0]))
    else:
        restaurants_info = [list(restaurant_info) for restaurant_info in restaurants_info]

    # restaurants_info = [[name, place_id, addr, latitude, longitude, price_level, 
    #                      rating, user_ratings_total, query_place_id, food_style, food_type], ...]
    return restaurants_info

def get_nearby_specified_restaurants_info(conn, place_info, food_style=None, food_type=None):
    assert (food_type is not None) ^ (food_style is not None)
    query_place_id = place_info[0]
    lat_place, lng_place = place_info[3], place_info[4]
    task = RESTAURANTS

    create_table(conn, task)
    restaurants_info = get_db_data(conn, task, keyword=query_place_id, food_style=food_style, food_type=food_type)
    print(len(restaurants_info))
    if(len(restaurants_info) < 10):
        restaurants_info = []
        # Request and parse json to lists of restaurants info 
        if(food_type is not None):
            res_json = text_search_requests(lat_place, lng_place, food_type)
            new_infos = parse_text_search_requests(res_json, query_place_id, food_type=food_type)
        else:
            res_json = text_search_requests(lat_place, lng_place, food_style)
            new_infos = parse_text_search_requests(res_json, query_place_id, food_style=food_style)
        # For each info, get data from db
        for new_info in new_infos:
            restaurant_info = get_db_data(conn, task, new_info)
            if(len(restaurant_info) == 0):
                insert_info(conn, task, new_info)
                restaurants_info.append(new_info)
            else:
                restaurant_info = list(restaurant_info[0])
                # UPDATE if food_style is null or food_type is null
                if((restaurant_info[-2] == "null" and new_info[-2] != "null") or (restaurant_info[-1] == "null" and new_info[-1] != "null")):
                    restaurant_info = update_info(conn, task, new_info, restaurant_info)
                restaurants_info.append(restaurant_info)
    else:
        restaurants_info = [list(restaurant_info) for restaurant_info in restaurants_info]

    # restaurants_info = [[name, place_id, addr, latitude, longitude, price_level, 
    #                      rating, user_ratings_total, query_place_id, food_style, food_type], ...]
    return restaurants_info

def get_all_specified_restaurants_info(conn, place_info):
    restaurants_info = []
    for food_style in FOOD_STYLES:
        print(food_style)
        restaurants_info_this = get_nearby_specified_restaurants_info(conn, place_info, food_style=food_style)
        restaurants_info.extend(restaurants_info_this)
    for food_type in FOOD_TYPES:
        print(food_type)
        restaurants_info_this = get_nearby_specified_restaurants_info(conn, place_info, food_type=food_type)
        restaurants_info.extend(restaurants_info_this)
    return restaurants_info

def main(place):
    # Connect to DB
    conn = create_connection()
    # Get Place Info
    place_info = get_place_info(conn, place)
    # Get Nearby Restaurants Info
    # restaurants_info = get_nearby_restaurants_info(conn, place_info)
    # Get Nearby Specidied Restaurants Info
    # restaurants_info = get_nearby_specified_restaurants_info(conn, place_info, food_style=FOOD_STYLES[0])
    # Get ALL Nearby Specidied Restaurants Info
    restaurants_info = get_all_specified_restaurants_info(conn, place_info)
    # for restaurant_info in restaurants_info:
    #     print(restaurant_info)


    close_connection(conn)



if __name__ == "__main__":
    place = "Ann Arbor"
    main(place)