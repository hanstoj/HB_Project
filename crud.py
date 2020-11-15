from model import db, Guest, Table, Restaurant, connect_to_db


def create_restaurant(username, restaurant_name, password, open_time, close_time):
    """Create and return a restaurant."""

    restaurant = Restaurant(username=username, restaurant_name=restaurant_name,
                            password=password, open_time=open_time, close_time=close_time)

    db.session.add(restaurant)
    db.session.commit()

    return restaurant


# def get_guest_stats(guest_id):

#     pass
