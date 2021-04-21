import requests
import sqlite3
import json

# from google_api import *
# from database import *
from utils import *

def main(place):
    # Connect to DB
    conn = create_connection()
    # Get Place Info
    place_info = get_place_info(conn, place)
    # Get Nearby Restaurants Info
    # restaurants_info = get_nearby_restaurants_info(conn, place_info)
    # Get Nearby Specidied Restaurants Info
    # restaurants_info = get_nearby_specified_restaurants_info(conn, place_info, FOOD_STYLES[2], food_style=True)
    # Get ALL Nearby Specidied Restaurants Info
    restaurants_info = get_all_specified_restaurants_info(conn, place_info)

    # Retrieve top-5 restaurant types, sorted by rating (average)
    top_k_restaurant_types = get_top_k_restaurant_types(conn, "food_style")

    # Choose one restaurant type (SQL)
    chosen_restaurant_type = top_k_restaurant_types[1][0]
    top_k_restaurants = get_top_k_restaurants(conn, "food_style", chosen_restaurant_type)
    # Search other restaurant type (SQL)
    entered_restaurant_type = "italian"
    top_k_restaurants = get_top_k_restaurants(conn, "food_style", entered_restaurant_type)
    # Search food directly (Request)
    query = "pizza"
    top_k_restaurants = get_top_k_query_restaurants(conn, place_info, query)
    
    
    close_connection(conn)



if __name__ == "__main__":
    place = "Ann Arbor"
    main(place)