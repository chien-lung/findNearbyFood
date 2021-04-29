from flask import Flask, render_template, request, redirect, url_for, session

from utils import *

app = Flask(__name__)
app.secret_key = "apple"
    
@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    if request.method == 'POST':
        place = request.form['place']
        conn = create_connection()
        place_info = get_place_info(conn, place)
        session["place"] = place_info
        close_connection(conn)
        place_name = place_info[1]
        return redirect(url_for("place", place=place_name))
    else:
        return render_template('index.html')

@app.route('/<place>', methods=['GET', 'POST'])
def place(place):
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for("restaurant_type", rst_type=query))
    else:
        if "place" not in session:
            return redirect(url_for("home"))
        else:
            conn = create_connection()
            place_info = session["place"]
            restaurants_info = get_all_specified_restaurants_info(conn, place_info)
            top_k_food_styles = get_top_k_restaurant_types(conn, place_info, "food_style")
            top_k_food_types = get_top_k_restaurant_types(conn, place_info, "food_type")
            close_connection(conn)
            rst_cls = ["Type" , "Average Rating", "Average Rating Number", "Number"]
            return render_template("place.html", 
                                place=place, 
                                restaurant_class=rst_cls, 
                                food_styles=top_k_food_styles,
                                food_types=top_k_food_types)

@app.route('/restaurant_type/<rst_type>')
def restaurant_type(rst_type):
    if "place" in session:
        conn = create_connection()
        place_info = session["place"]
        if rst_type in FOOD_STYLES:
            top_k_restaurants = get_top_k_restaurants(conn, place_info, "food_style", rst_type)
        elif rst_type in FOOD_TYPES:
            top_k_restaurants = get_top_k_restaurants(conn, place_info, "food_type", rst_type)
        else:
            top_k_restaurants = get_top_k_query_restaurants(conn, place_info, rst_type)
        session["restaurants"] = top_k_restaurants
        close_connection(conn)
        restaurants = [r[:5] for r in top_k_restaurants]
    else:
        return redirect(url_for("home"))
    rst_cls = ["Name", "Rating", "Rating Number", "Price Level", "Address"]
    return render_template("restaurant_type.html", 
                        restaurant_type=rst_type,
                        restaurant_class=rst_cls, 
                        restaurants=restaurants)

@app.route('/restaurant/<rst>')
def restaurant(rst):
    restaurants = session["restaurants"]
    for rst_info in restaurants:
        if rst in rst_info:
            place_id = rst_info[-1]
            break
    conn = create_connection()
    restaurant_gmap_detail = get_gmap_restaurant_detail(conn, place_id)
    phone = restaurant_gmap_detail[2]
    restaurant_yelp_detail = get_yelp_restaurant_detail(conn, phone)
    close_connection(conn)
    addr = rst_info[4]
    open_hours = restaurant_gmap_detail[3].split(";")

    gmap_info = [rst_info[1], rst_info[2], rst_info[3]]
        
    gmap_reviews = [restaurant_gmap_detail[-9:][x: x+3] for x in range(0, len(restaurant_gmap_detail[-9:]), 3)]
    gmap_info.extend(gmap_reviews)

    yelp_info =[restaurant_yelp_detail[5], restaurant_yelp_detail[6], restaurant_yelp_detail[4]]
    yelp_reviews = [restaurant_yelp_detail[-9:][x: x+3] for x in range(0, len(restaurant_yelp_detail[-9:]), 3)]
    yelp_info.extend(yelp_reviews)

    rst_cls = ["Rating", "Rating Number", "Price Level", "Review1", "Review2", "Review3"]
    return render_template("restaurant.html", 
                           restaurant=rst,
                           phone = phone,
                           address = addr,
                           open_hours=open_hours,
                           restaurant_class=rst_cls,
                           gmap_info=gmap_info,
                           yelp_info=yelp_info, 
                           )

if __name__ == "__main__":
    app.run(debug=True)