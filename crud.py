from model import db, Guest, Dinning_table, Restaurant, Reservation, connect_to_db

# NOTE: Double check if Foreign key needs to be passed in as an argument? LIke resturant ID


def create_restaurant(username, restaurant_name,
                      password, open_time, close_time):
    #    )
    """Create and return a restaurant."""
    # TODO fix time-
    restaurant = Restaurant(username=username, restaurant_name=restaurant_name,
                            password=password, open_time=open_time, close_time=close_time)
    db.session.add(restaurant)
    db.session.commit()
    # open_time=open_time, close_time=close_time
    return restaurant


def create_table(table_num, is_booth, num_seats, is_taken=False):
    """Create Table in Restaurant"""
    table = Dinning_table(table_num=table_num, is_booth=is_booth,
                          num_seats=num_seats, is_taken=is_taken)

    db.session.add(table)
    db.session.commit()

    return table


def get_table_by_table_num(table_num):

    return Dinning_table.query.filter(Dinning_table.table_num == table_num).first()


def create_res(guest_id, party_num, res_date, res_time, res_notes, booth_pref, is_celebrating,  end_time=None, arrival_time=None):
    """Create and return a restaurant."""

    reservation = Reservation(guest_id=guest_id, party_num=party_num, res_date=res_date, res_time=res_time, res_notes=res_notes,
                              booth_pref=booth_pref, is_celebrating=is_celebrating,  end_time=end_time, arrival_time=arrival_time)
    db.session.add(reservation)
    db.session.commit()

    return reservation


def create_guest(phone_num, guest_name):

    guest = Guest(phone_num=phone_num, guest_name=guest_name)

    db.session.add(guest)
    db.session.commit()

    return guest


def get_restaurant_by_username(username):

    return Restaurant.query.filter(Restaurant.username == username).first()


def get_restaurant_by_restaurant_id(restaurant_id):

    return Restaurant.query.get(restaurant_id)


def get_tables():

    return Dinning_table.query.all()
