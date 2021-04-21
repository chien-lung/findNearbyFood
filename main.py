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
    restaurants_info = get_nearby_restaurants_info(conn, place_info)
    # Get Nearby Specidied Restaurants Info
    # restaurants_info = get_nearby_specified_restaurants_info(conn, place_info, food_style=FOOD_STYLES[2])
    # Get ALL Nearby Specidied Restaurants Info
    restaurants_info = get_all_specified_restaurants_info(conn, place_info)

    # Retrieve top-5 restaurant types, sorted by rating (average)
    top_k_restaurant_type = get_top_k_restaurant_type(conn, "food_style")
    # for r in top_k_restaurant_type:
    #     print(r)

    # Choose one restaurant type (SQL)
    chosen_restaurant_type = top_k_restaurant_type[0][0]

    # Search other restaurant type (SQL)
    entered_restaurant_type = "italian"

    # Search food directly (Request)

    
    close_connection(conn)



if __name__ == "__main__":
    place = "Ann Arbor"
    main(place)