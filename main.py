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
    # restaurants_info = get_nearby_specified_restaurants_info(conn, place_info, food_style=FOOD_STYLES[0])
    # restaurants_info = get_nearby_specified_restaurants_info(conn, place_info, food_type=FOOD_TYPES[-1])
    # Get ALL Nearby Specidied Restaurants Info
    restaurants_info = get_all_specified_restaurants_info(conn, place_info)

    close_connection(conn)



if __name__ == "__main__":
    place = "Ann Arbor"
    main(place)