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
    top_k_restaurant_types = get_top_k_restaurant_types(conn, place_info, "food_style")
    for restaurant_type in top_k_restaurant_types:
        print(restaurant_type)

    # Choose one restaurant type (SQL)
    chosen_restaurant_type = restaurant_type[0]
    top_k_restaurants = get_top_k_restaurants(conn, "food_style", chosen_restaurant_type)
    # Search other restaurant type (SQL)
    entered_restaurant_type = "italian"
    top_k_restaurants = get_top_k_restaurants(conn, "food_style", entered_restaurant_type)
    # Search food directly (Request)
    # query = "pub"
    # top_k_restaurants = get_top_k_query_restaurants(conn, place_info, query)
    
    # Choose an interesting restaurant from results
    for i, chosen_restaurant in enumerate(top_k_restaurants):
        place_id = chosen_restaurant[0]
        restaurant_gmap_detail = get_gmap_restaurant_detail(conn, place_id)
        phone = restaurant_gmap_detail[2]
        restaurant_yelp_detail = get_yelp_restaurant_detail(conn, phone)
        print(i)
        print(restaurant_gmap_detail)
        print(restaurant_yelp_detail)



    close_connection(conn)



if __name__ == "__main__":
    place = "New York"
    main(place)