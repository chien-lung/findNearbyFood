from yelpapi import YelpAPI

import secrets

def yelp_restaurant_search(phone):
    # restaurant search by phone
    # "(987) 654-3210" -> "+19876543210"
    phone = "+1" + ''.join(c for c in phone if c.isdigit())
    client = YelpAPI(secrets.YELP_API_KEY)
    print("yelp phone and id request")
    res_json = client.phone_search_query(phone=phone)
    assert res_json["total"] != 0
    info = []
    restaurant = res_json["businesses"][0]
    id = restaurant["id"]
    name = restaurant["name"]
    url = restaurant["url"]
    user_ratings_total = restaurant["review_count"]
    rating = restaurant["rating"]
    price_level = len(restaurant["price"])
    phone = restaurant["display_phone"]
    info.extend([id, name, phone, url, price_level, rating, user_ratings_total])
    # reviews search by id
    res_json = client.reviews_query(id=id)
    reviews = res_json["reviews"]
    for i in range(3):
        if i < len(reviews):
            author_name = reviews[i]["user"]["name"]
            author_rating = reviews[i]["rating"]
            author_text = reviews[i]["text"]
        else:
            author_name = "null"
            author_rating = "null"
            author_text = "null"
        info.extend([author_name, author_rating, author_text])
    return [info]
