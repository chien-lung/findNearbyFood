class Place():
    def __init__(self, info) -> None:
        # info: [place_id, name, address, latitude, longitude]
        self.place_id = info[0]
        self.name = info[1]
        self.address = info[2]
        self.latitude = info[3]
        self.longitude = info[4]

class Restaurant():
    def __init__(self, info) -> None:
        # info: [place_id, name, addr, latitude, longitude, price_level, rating, 
        #        user_ratings_total, query_place_id, food_style, food_type]
        self.place_id = info[0]
        self.name = info[1]
        self.address = info[2]
        self.latitude = info[3]
        self.longitude = info[4]
        self.price_level = info[5]
        self.rating = info[6]
        self.ratings_num = info[7]
        self.query_place_id = info[8]
        self.food_style = info[9]
        self.food_type = info[10]

class RestaurantType():
    def __init__(self, info) -> None:
        # info: [type, average_rating, average_rating_number, number]
        self.type = info[0]
        self.avg_rating = info[1]
        self.avg_ratings_num = info[2]
        self.number = info[3]

class GmapDetail():
    def __init__(self, info) -> None:
        # info: [place_id, name, phone, open_hours, 
        #        reviewer1, reviewer1_rating, reviewer1_text,
        #        reviewer2, reviewer2_rating, reviewer2_text, 
        #        reviewer3, reviewer3_rating, reviewer3_text]
        self.place_id = info[0]
        self.name = info[1]
        self.phone = info[2]
        self.open_hours = info[3]
        self.price_level = None
        self.rating = None
        self.ratings_num = None
        review1 = info[4:7]
        review2 = info[7:10]
        review3 = info[10:]
        self.reviews = [review1, review2, review3]

class YelpDetail():
    def __init__(self, info) -> None:
        self.id = info[0]
        self.name = info[1]
        self.phone = info[2]
        self.url = info[3]
        self.price_level = info[4]
        self.rating = info[5]
        self.ratings_num = info[6]
        review1 = info[7:10]
        review2 = info[10:13]
        review3 = info[13:]
        self.reviews = [review1, review2, review3]

def get_place_object(info):
    return Place(info)

def get_restaurant_object(info):
    return Restaurant(info)

def get_restaurant_type_object(info):
    return RestaurantType(info)

def get_gmap_detail_object(info):
    return GmapDetail(info)

def get_yelp_detail_object(info):
    return YelpDetail(info)