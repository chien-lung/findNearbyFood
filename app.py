from flask import Flask, render_template, request, redirect, url_for

from utils import *

app = Flask(__name__)
# app.secret_key = "apple"
place_select = None
restaurants_select = None

    
@app.route('/', methods=['GET', 'POST'])
def home():
    global place_select, restaurants_select
    place_select = None
    restaurants_select = None
    if request.method == 'POST':
        place = request.form['place']
        conn = create_connection()
        place_object = get_place_info(conn, place)
        place_select = place_object
        close_connection(conn)
        return redirect(url_for("place", place=place_object.name))
    else:
        return render_template('index.html')

@app.route('/<place>', methods=['GET', 'POST'])
def place(place):
    global place_select
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for("restaurant_type", rst_type=query))
    else:
        if place_select is None:
            return redirect(url_for("home"))
        else:
            conn = create_connection()
            restaurants_info = get_all_specified_restaurants_info(conn, place_select)
            top_k_food_styles = get_top_k_restaurant_types(conn, place_select, "food_style")
            top_k_food_types = get_top_k_restaurant_types(conn, place_select, "food_type")
            close_connection(conn)
            rst_cls = ["Type" , "Average Rating", "Average Rating Number", "Number"]
            return render_template("place.html", 
                                place=place, 
                                restaurant_class=rst_cls, 
                                food_styles=top_k_food_styles,
                                food_types=top_k_food_types)

@app.route('/restaurant_type/<rst_type>')
def restaurant_type(rst_type):
    global place_select, restaurants_select
    if place_select is None:
        return redirect(url_for("home"))      
    else:
        conn = create_connection()
        place_info = place_select
        if rst_type in FOOD_STYLES:
            top_k_restaurants = get_top_k_restaurants(conn, place_info, "food_style", rst_type)
        elif rst_type in FOOD_TYPES:
            top_k_restaurants = get_top_k_restaurants(conn, place_info, "food_type", rst_type)
        else:
            top_k_restaurants = get_top_k_query_restaurants(conn, place_info, rst_type)
        restaurants_select = top_k_restaurants
        close_connection(conn)
        rst_cls = ["Name", "Rating", "Rating Number", "Price Level", "Address"]
        return render_template("restaurant_type.html", 
                            restaurant_type=rst_type,
                            restaurant_class=rst_cls, 
                            restaurants=top_k_restaurants)

@app.route('/restaurant/<restaurant_name>')
def restaurant(restaurant_name):
    global place_select, restaurants_select
    restaurants = restaurants_select
    if place_select is None:
        return redirect(url_for("home"))
    else:
        for restaurant in restaurants:
            if restaurant_name == restaurant.name:
                place_id = restaurant.place_id
                break
        conn = create_connection()
        restaurant_gmap_detail = get_gmap_restaurant_detail(conn, place_id)
        restaurant_gmap_detail.rating = restaurant.rating
        restaurant_gmap_detail.ratings_num = restaurant.ratings_num
        restaurant_gmap_detail.price_level = restaurant.price_level
        restaurant_yelp_detail = get_yelp_restaurant_detail(conn, restaurant_gmap_detail.phone)
        close_connection(conn)

        return render_template("restaurant.html", 
                            restaurant_name=restaurant_name,
                            restaurant_gmap_detail=restaurant_gmap_detail,
                            restaurant_yelp_detail=restaurant_yelp_detail
                            )

if __name__ == "__main__":
    app.run(debug=True)