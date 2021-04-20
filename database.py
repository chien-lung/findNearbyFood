import sqlite3
import json

from google_api import *

DB_FILE_NAME = "findNearFood.db"
PLACES = "places"
RESTAURANTS = "restaurants"
DETAILS = "details"

ATTRIBUTES = {
    PLACES:{
        "place_id": 0,
        "name": 1,
        "address": 2,
        "latitude": 3,
        "longitude": 4
    },
    RESTAURANTS:{
        "place_id": 0,
        "name": 1,
        "address": 2,
        "latitude": 3,
        "longitude": 4,
        "price_level": 5,
        "rating": 6,
        "user_ratings_total": 7,
        "query_place_id": 8,
        "food_style": 9,
        "food_type": 10,
    },
    DETAILS:{
    }
}

####################
# Process Database #
####################
def create_connection():
    conn = sqlite3.connect(DB_FILE_NAME)
    return conn

def close_connection(conn):
    conn.close()

def create_table(conn, task):
    query = None
    if(task == PLACES):
        query = f'''
            CREATE TABLE IF NOT EXISTS {task} (
                "place_id"  TEXT NOT NULL UNIQUE,
                "name"  TEXT NOT NULL,
                "address"   TEXT NOT NULL,
                "latitude"  TEXT NOT NULL,
                "longitude" TEXT NOT NULL,
                PRIMARY KEY("place_id")
            );
        '''
    elif(task == RESTAURANTS):
        query = f'''
            CREATE TABLE IF NOT EXISTS {task} (
                "place_id"  TEXT NOT NULL UNIQUE,
                "name"  TEXT NOT NULL,
                "address"   TEXT NOT NULL,
                "latitude"  TEXT NOT NULL,
                "longitude" TEXT NOT NULL,
                "price_level"   TEXT,
                "rating"    TEXT NOT NULL,
                "user_ratings_total"    TEXT NOT NULL,
                "query_place_id"    TEXT NOT NULL,
                "food_style"   TEXT,
                "food_type" TEXT,
                PRIMARY KEY("place_id")
            );
        '''
    elif(task == DETAILS):
        pass
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

def insert_info(conn, task, info):
    query = None
    if(task == PLACES):
        query = f'''
            INSERT INTO {task}
            VALUES (?, ?, ?, ?, ?)
        '''
    elif(task == RESTAURANTS):
        query = f'''
            INSERT INTO {task}
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    elif(task == DETAILS):
        pass
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query, info)
    print(f"Insert new value into table \"{task}\"")
    conn.commit()

def need_update(task, new_info, old_info):
    ########
    # TODO #
    ########
    if(task == PLACES):
        pass
    elif(task == RESTAURANTS):
        food_style_idx = ATTRIBUTES[task]["food_style"]
        food_type_idx = ATTRIBUTES[task]["food_type"]
        food_style_needs_update = old_info[food_style_idx] == "null" and new_info[food_style_idx] != "null"
        food_type_needs_update = old_info[food_type_idx] == "null" and new_info[food_type_idx] != "null"
        return food_style_needs_update or food_type_needs_update
    elif(task == DETAILS):
        pass
    return False

def update_info(conn, task, new_info, old_info):
    ########
    # TODO #
    ########
    if(not need_update(task, new_info, old_info)):
        return old_info

    query = None
    if(task == PLACES):
        pass
    elif(task == RESTAURANTS):
        food_style_idx = ATTRIBUTES[task]["food_style"]
        food_type_idx = ATTRIBUTES[task]["food_type"]
        place_id_idx = ATTRIBUTES[task]["place_id"]
        condition_str = ""
        if(new_info[food_style_idx] != "null" and old_info[food_style_idx] == "null"):
            condition_str = f"food_style=\"{new_info[food_style_idx]}\""
            old_info[food_style_idx] = new_info[food_style_idx]
        elif(new_info[food_type_idx] != "null" and old_info[food_type_idx] == "null"):
            condition_str = f"food_type=\"{new_info[food_type_idx]}\""
            old_info[food_type_idx] = new_info[food_type_idx]
        query = f'''
            UPDATE {task}
            SET {condition_str}
            WHERE place_id="{old_info[place_id_idx]}"
        '''
    elif(task == DETAILS):
        pass
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    print(f"Update new value into table \"{task}\"")
    return old_info

def get_db_data(conn, task, info=None, keyword=None, food_style=None, food_type=None):
    query = None
    # Specify keyword to search
    if(keyword is not None):
        if(task == PLACES):
            query = f'''
                SELECT * FROM {task} WHERE name="{keyword}"
            '''
        elif(task == RESTAURANTS):
            condition_str = ""
            if(food_style is not None):
                condition_str += f" AND food_style=\"{food_style}\""
            if(food_type is not None):
                condition_str += f" AND food_type=\"{food_type}\""
            query = f'''
                SELECT * FROM {task} WHERE query_place_id="{keyword}"{condition_str}
            '''
        elif(task == DETAILS):
            pass
    # Search by place_id
    elif(task == PLACES):
        query = f'''
            SELECT * FROM {task} WHERE place_id="{info[0]}"
        '''
    elif(task == RESTAURANTS):
        query = f'''
            SELECT * FROM {task} WHERE place_id="{info[0]}"
        '''
    elif(task == DETAILS):
        pass
    else:
        print("Wrong Task")
    
    assert query is not None    
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    return result


if __name__ == "__main__":
    conn = create_connection()

    place_info = ["ChIJdR3LEAHKJIgR0sS5NU6Gdlc", "Detroit", "Detroit, MI, USA", "42.331427", "-83.0457538"]

    close_connection(conn)
