from model import db, Guest, Dinning_table, Restaurant, Reservation, connect_to_db
from dateutil import parser
# NOTE: Double check if Foreign key needs to be passed in as an argument? LIke resturant ID


def create_restaurant(username, restaurant_name,
                      password, open_time, close_time):
    #    )
    """Create and return a restaurant."""
    # TODO fix time
    print(f'open_time {open_time}')
    print("")
    print("")
    print(f'type close before parse{type(close_time)}')
    open_time = parser.parse(open_time)
    close_time = parser.parse(close_time)
    print(f'check parsing method {close_time}')
    print(f'type{type(close_time)}')
    print("")
    print(f'close_time {close_time}')
    restaurant = Restaurant(username=username, restaurant_name=restaurant_name,
                            password=password, open_time=open_time, close_time=close_time)
    db.session.add(restaurant)
    db.session.commit()
    # open_time=open_time, close_time=close_time
    return restaurant


def create_table(table_num, is_booth, num_seats, restaurant_id, is_taken=False):
    """Create Table in Restaurant"""
    table = Dinning_table(table_num=table_num, is_booth=is_booth,
                          num_seats=num_seats, restaurant_id=restaurant_id, is_taken=is_taken)

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


def get_all_guests():

    return Guest.query.all()


def get_guest_by_id(guest_id):

    return Guest.query.get(guest_id)


def get_restaurant_by_username(username):

    return Restaurant.query.filter(Restaurant.username == username).first()


def get_restaurant_by_restaurant_id(restaurant_id):

    return Restaurant.query.get(restaurant_id)


def reservation_by_id(reservation_id):

    return Restaurant.query.get(reservation_id)


def get_tables_by_restaurant_id(restaurant_id):

    # NOTE: changed it from .all() to .first()
    return Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).options(db.joinedload("tables")).first()


# def reservation_assignment(reservation_id):
#     if table_seats < reservation.party_num:
#         seats = True

#     if is_taken = False:
#         not_taken = True
    #   if res_date == datetime.today()


# >>> datetime.now()
# datetime.datetime(2020, 11, 24, 23, 54, 52, 15333)
# >>> datetime.today()
# datetime.datetime(2020, 11, 24, 23, 54, 58, 89993)

# 'res_date': '2020-11-25',

# >>> date.today()
# datetime.date(2020, 11, 25)


# assign reservation
# min in reservation start - min res end = avg res

# expected table stay = 45

# if party_num in range 6+:
#     expected table stay +15

# if celebrating
#     expected table stay +20:


# total = end - arrival
# dinning_speed =  total - expected


# assigning table
# if num_seats - res_size > 0:

# if is_taken = False

# if arrival_time +delta? expected_min is < new arrival time?
