import sqlite3
import json

from google_api import *

DB_FILE_NAME = "findNearFood.db"
PLACES = "places"
RESTAURANTS = "restaurants"
DETAILS = "details"

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
                "id"    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "name"  TEXT NOT NULL,
                "place_id"  TEXT NOT NULL,
                "address"   TEXT NOT NULL,
                "latitude"  TEXT NOT NULL,
                "longitude" TEXT NOT NULL
            );
        '''
    elif(task == RESTAURANTS):
        query = f'''
            CREATE TABLE IF NOT EXISTS {task} (
                "id"    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "name"  TEXT NOT NULL,
                "place_id"  TEXT NOT NULL,
                "address"   TEXT NOT NULL,
                "latitude"  TEXT NOT NULL,
                "longitude" TEXT NOT NULL,
                "price_level"   TEXT,
                "rating"    TEXT NOT NULL,
                "user_ratings_total"    TEXT NOT NULL,
                "query_place_id"    TEXT NOT NULL,
                "food_style"   TEXT,
                "food_type" TEXT
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

def insert_new_info(conn, task, new_info):
    query = None
    if(task == PLACES):
        query = f'''
            INSERT INTO {task}
            VALUES (NULL, ?, ?, ?, ?, ?)
        '''
    elif(task == RESTAURANTS):
        query = f'''
            INSERT INTO {task}
            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    elif(task == DETAILS):
        pass
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query, new_info)
    print(f"Insert new value into table \"{task}\"")
    conn.commit()

def update_new_info(conn, task, new_info, old_info):
    query = None
    if(task == PLACES):
        pass
    elif(task == RESTAURANTS):
        condition_str = ""
        if(new_info[-2] != "null" and old_info[-2] == "null"):
            condition_str = f"food_style=\"{new_info[-2]}\""
            old_info[-2] = new_info[-2]
        elif(new_info[-1] != "null" and old_info[-1] == "null"):
            condition_str = f"food_type=\"{new_info[-1]}\""
            old_info[-1] = new_info[-1]
        query = f'''
            UPDATE {task}
            SET {condition_str}
            WHERE place_id="{old_info[1]}"
        '''
    elif(task == DETAILS):
        pass
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query)
    print(f"Update new value into table \"{task}\"")
    conn.commit()
    return old_info

def get_db_data(conn, task, info=None, keyword=None, food_style=None, food_type=None):
    query = None
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
    elif(task == PLACES):
        query = f'''
            SELECT * FROM {task} WHERE place_id="{info[1]}"
        '''
    elif(task == RESTAURANTS):
        query = f'''
            SELECT * FROM {task} WHERE place_id="{info[1]}"
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

    # place_info = ['Taoyuan City', 'ChIJP4bazg49aDQRakg6WFJP5FQ', 'Taoyuan City, Taiwan', '24.9936281', '121.3009798']
    place_info = ["Detroit", "ChIJdR3LEAHKJIgR0sS5NU6Gdlc", "Detroit, MI, USA", "42.331427", "-83.0457538"]


    close_connection(conn)
