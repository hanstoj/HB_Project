from model import db, Guest, Table, Restaurant, connect_to_db


def create_restaurant(username, restaurant_name, password, open_time, close_time):
    """Create and return a restaurant."""

    restaurant = Restaurant(username=username, restaurant_name=restaurant_name,
                            password=password, open_time=open_time, close_time=close_time)

    db.session.add(restaurant)
    db.session.commit()

    return restaurant


def create_table(table_num, is_booth, num_seats, is_taken=False):
    """Create Table in Restaurant"""
    table = Table(table_num=table_num, is_booth=is_booth,
                  num_seats=num_seats, is_taken=is_taken)

    db.session.add(table)
    db.session.commit()

    return table


def get_table_by_table_num(table_num):

    return Table.query.filter(Table.table_num == table_num).first()


def create_res(res_size, res_time, arrival_time, end_time, booth_pref, res_notes, celebrating, phone_num):
    """Create and return a restaurant."""

    reservation = Restaurant(res_size=res_size, res_time=res_time, arrival_time=arrival_time,
                             end_time=end_time, booth_pref=booth_pref, celebrating=celebrating, phone_num=phone_num)

    db.session.add(reservation)
    db.session.commit()

    return reservation


def get_restaurant_by_username(username):

    return Restaurant.query.filter(Restaurant.username == username).first()
# def get_guest_stats(guest_id):

#     pass
