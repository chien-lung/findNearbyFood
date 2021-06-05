import sqlite3
import json

DB_FILE_NAME = "findNearFood.db"
PLACES = "places"
RESTAURANTS = "restaurants"
GMAP_DETAILS = "gmap_details"
YELP_DETAILS = "yelp_details"

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
    GMAP_DETAILS:{
        "place_id": 0,
        "name": 1,
        "phone": 2,
        "open_hours": 3,
        "reviewer1": 4,
        "reviewer1_rating": 5,
        "reviewer1_text": 6,
        "reviewer2": 7,
        "reviewer2_rating": 8,
        "reviewer2_text": 9,
        "reviewer3": 10,
        "reviewer3_rating": 11,
        "reviewer3_text": 12,
        "reviewer4": 13,
        "reviewer4_rating": 14,
        "reviewer4_text": 15,
        "reviewer5": 16,
        "reviewer5_rating": 17,
        "reviewer5_text": 18,
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
    elif(task == GMAP_DETAILS):
        query = f'''
            CREATE TABLE IF NOT EXISTS {task} (
                "place_id"  TEXT NOT NULL UNIQUE,
                "name"  TEXT NOT NULL,
                "phone" TEXT NOT NULL,
                "open_hours" TEXT,
                "reviewer1" TEXT,
                "reviewer1_rating" TEXT,
                "reviewer1_text" TEXT,
                "reviewer2" TEXT,
                "reviewer2_rating" TEXT,
                "reviewer2_text" TEXT,
                "reviewer3" TEXT,
                "reviewer3_rating" TEXT,
                "reviewer3_text" TEXT,
                PRIMARY KEY("place_id")
            );
        '''
    elif(task == YELP_DETAILS):
        query = f'''
            CREATE TABLE IF NOT EXISTS {task} (
                "id"  TEXT NOT NULL UNIQUE,
                "name"  TEXT NOT NULL,
                "phone" TEXT NOT NULL,
                "url" TEXT, 
                "price_level" TEXT,
                "rating" TEXT, 
                "user_ratings_total" TEXT,
                "reviewer1" TEXT,
                "reviewer1_rating" TEXT,
                "reviewer1_text" TEXT,
                "reviewer2" TEXT,
                "reviewer2_rating" TEXT,
                "reviewer2_text" TEXT,
                "reviewer3" TEXT,
                "reviewer3_rating" TEXT,
                "reviewer3_text" TEXT,
                PRIMARY KEY("id")
            );
        '''
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

def insert_info(conn, task, info):
    query = None
    if(task == PLACES):
        values = ",".join("?"*5)
    elif(task == RESTAURANTS):
        values = ",".join("?"*11)
    elif(task == GMAP_DETAILS):
        values = ",".join("?"*13)
    elif(task == YELP_DETAILS):
        values = ",".join("?"*16)
    else:
        print("Wrong Task")

    query = f'''
            INSERT INTO {task}
            VALUES ({values})
        '''
    cur = conn.cursor()
    cur.execute(query, info)
    print(f"Insert new value into table \"{task}\"")
    conn.commit()

def need_update(task, new_info, old_info):
    if(task == PLACES):
        pass
    elif(task == RESTAURANTS):
        food_style_idx = ATTRIBUTES[task]["food_style"]
        food_type_idx = ATTRIBUTES[task]["food_type"]
        food_style_needs_update = old_info[food_style_idx] == "null" and new_info[food_style_idx] != "null"
        food_type_needs_update = old_info[food_type_idx] == "null" and new_info[food_type_idx] != "null"
        return food_style_needs_update or food_type_needs_update
    elif(task == GMAP_DETAILS):
        pass
    return False

def update_info(conn, task, new_info, old_info):
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
    elif(task == GMAP_DETAILS):
        pass
    else:
        print("Wrong Task")

    assert query is not None    
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    print(f"Update new value into table \"{task}\"")
    return old_info

def generate_condition_str(keyword_dict):
    keys = list(keyword_dict.keys())
    values = [keyword_dict[key] for key in keys]
    
    condition_strs = []
    for i in range(len(keys)):
        if type(values[i]) is list:
            c_str = f"{keys[i]} in "
            c_str += "(\"" + "\",\"".join(values[i]) + "\")"
        else:
            c_str = f"{keys[i]}=\"{values[i]}\""
        condition_strs.append(c_str)
    condition_str = ' AND '.join(condition_strs)
    return condition_str

def retrieve_db_data(conn, task, keyword_dict):
    condition_str = generate_condition_str(keyword_dict)
    query = f'''
        SELECT * FROM {task}
        WHERE {condition_str}
    '''   
    cur = conn.cursor()
    results = cur.execute(query).fetchall()
    return results

def retrieve_top_k_restaurant_types(conn, query_place_id, style_or_type, sort_key, k):
    query = f'''
        SELECT {style_or_type}, ROUND(AVG(rating),2), ROUND(AVG(user_ratings_total),2), COUNT({style_or_type}) FROM restaurants
        WHERE {style_or_type}<>"null" AND user_ratings_total<>"0" AND query_place_id="{query_place_id}"
        GROUP BY {style_or_type}
        ORDER BY AVG({sort_key}) DESC
        LIMIT {k};
    '''
    cur = conn.cursor()
    results = cur.execute(query).fetchall()  
    return results

def retrieve_top_k_restaurants(conn, query_place_id, style_or_type, restaurant_type, sort_key, k, keyword_dict=None):
    if keyword_dict is None:
        condition_str = f'''
            {style_or_type}="{restaurant_type}" 
            AND query_place_id="{query_place_id}"
            COLLATE NOCASE
        '''
    else:
        condition_str = generate_condition_str(keyword_dict)
    
    query = f'''
        SELECT * FROM restaurants
        WHERE {condition_str}
        ORDER BY {sort_key}
        DESC
        LIMIT {k};
    '''
    cur = conn.cursor()
    results = cur.execute(query).fetchall()  
    return results

if __name__ == "__main__":
    conn = create_connection()

    # place_info = ["ChIJdR3LEAHKJIgR0sS5NU6Gdlc", "Detroit", "Detroit, MI, USA", "42.331427", "-83.0457538"]
    close_connection(conn)
