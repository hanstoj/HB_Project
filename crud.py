from model import db, Guest, Dinning_table, Restaurant, Reservation, connect_to_db
from dateutil import parser
from dateutil.parser import parse
from arrow import arrow
from datetime import datetime, time, timedelta

# NOTE: Double check if Foreign key needs to be passed in as an argument? LIke resturant ID

# --------------------------------------------------------------------------------------
#    Restaurant
# --------------------------------------------------------------------------------------


def create_restaurant(username, restaurant_name,
                      password, open_time, close_time):
    #    )
    """Create and return a restaurant."""
    # TODO fix time
    print(f'open_time {open_time}')
    print("")
    print("")
    print(f'type close before parse{type(close_time)}')

    open_time = parse(open_time).time()
    close_time = parse(close_time).time()
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


def get_restaurant_by_username(username):

    return Restaurant.query.filter(Restaurant.username == username).first()


def get_restaurant_by_restaurant_id(restaurant_id):

    return Restaurant.query.get(restaurant_id)


# --------------------------------------------------------------------------------------
    #    Table
# --------------------------------------------------------------------------------------

def create_table(table_num, is_booth, num_seats, restaurant_id):
    """Create Table in Restaurant"""
    table = Dinning_table(table_num=table_num, is_booth=is_booth,
                          num_seats=num_seats, restaurant_id=restaurant_id)

    db.session.add(table)
    db.session.commit()

    return table


def get_table_by_table_num(table_num):

    return Dinning_table.query.filter(Dinning_table.table_num == table_num).first()


def get_tables_by_restaurant_id(restaurant_id):

    # NOTE: changed it from .all() to .first()
    return Restaurant.query.filter(Restaurant.restaurant_id == restaurant_id).options(db.joinedload("tables")).first()


# --------------------------------------------------------------------------------------
    #    Guest
# --------------------------------------------------------------------------------------


def create_guest(phone_num, guest_name, avg_time_spent=45, num_visits=0):
    print("")
    print("")
    print(f"avg time spent {avg_time_spent} ")
    print(f"avg time spent {type(avg_time_spent)} ")
    guest = Guest(phone_num=phone_num, guest_name=guest_name,
                  avg_time_spent=avg_time_spent, num_visits=num_visits)

    db.session.add(guest)
    db.session.commit()

    return guest


def update_guest_seating_time(guest_id, seated_time):
    g = Guest.query.get(guest_id)
    print(g)

    g.num_visits += 1
    print(g.num_visits)
    db.session.add(g)
    db.session.commit()
    print(g)


def get_guest_by_id(guest_id):

    return Guest.query.get(guest_id)


def get_guest_by_phone_num(phone_num):

    return Guest.query.get(phone_num)


def get_guest():

    return Guest.query.get().all()


# --------------------------------------------------------------------------------------
    #    Reservation Making
# --------------------------------------------------------------------------------------

def create_res(guest_id, restaurant_id, party_num, res_date, res_time, expected_time, res_notes, booth_pref, is_celebrating, table_id, end_time=None, arrival_time=None):
    """Create and return a restaurant."""

    reservation = Reservation(guest_id=guest_id, restaurant_id=restaurant_id, party_num=party_num, res_date=res_date, res_time=res_time, expected_time=expected_time, res_notes=res_notes,
                              booth_pref=booth_pref, is_celebrating=is_celebrating, table_id=table_id, end_time=end_time, arrival_time=arrival_time)
    db.session.add(reservation)
    db.session.commit()

    return reservation


def update_reservation_arrival_time(res_id, seated_time):
    print(res_id)
    print("the res id is above")
    r = Reservation.query.get(res_id)
    print(seated_time)
    print(r)
    print(seated_time)
    print(r)
    print(seated_time)
    print(r)
    print(seated_time)
    print(r)
    print(seated_time)
    print(r)
    print("this is the reservation withthe res id")
    print(r.arrival_time)
    print(r.arrival_time)
    print(r.arrival_time)
    print(r.arrival_time)
    print(r.arrival_time)
    print(r.arrival_time)
    print(r.arrival_time)
    print(r.arrival_time)

    r.arrival_time = seated_time

    print(r.arrival_time)

    db.session.add(r)
    db.session.commit()


def reservation_by_id(reservation_id):

    return Restaurant.query.get(reservation_id)


def date_match(res_date):

    if (datetime.today() - res_date).days == 0:
        return print("date match")


def expected_time_calc(party_num, is_celebrating, avg_time_spent):

    print(f"{party_num}, {is_celebrating}, {avg_time_spent}")

    expected = avg_time_spent

    if int(party_num) > 5:
        expected = expected + 20
        print(f"over 6 expected update: {expected}")
    if is_celebrating:
        expected = expected + 20
        print(f"is celebraing update: {expected}")
    print("")
    print("")
    print("")
    print(expected)
    print("expected time is above")
    return expected


def update_finished_time(res_id, guest_id, finished_time):
    g = get_guest_by_id(guest_id)
    r = Reservation.query.get(res_id)
    print(r.arrival_time)
    print("arrival time")
    print(finished_time)
    print("finished")

    print(r.end_time)
    print("end time beforre")
    r.end_time = finished_time
    print("end time after assignment")
    print(r.end_time)

    print(r)
    print("DOUBLE CHECK BEFORE YOU LOSE THE EXAMPLE")
    # FINDING A CHECK

    db.session.add(r)
    db.session.commit()
    print("IT HAS BEEN COMMITED")

    finished_time = (finished_time - r.arrival_time).total_seconds() / 60.0
    intfinish = int(finished_time)
    print
    print(type(intfinish))

    print(g.avg_time_spent)
    print("THIS IS THE OLD ONE")
    added = g.avg_time_spent + intfinish
    divide = g.num_visits + 1
    g.avg_time_spent = added / divide

    print(g.avg_time_spent)
    print("THIS IS THE NEW ONE")
    print(g)
    print("DOUBLE CHECK BEFORE YOU LOOSE EXAMPLE")
    db.session.add(g)
    db.session.commit()

    # r.res =

    print("arrival and seated")
    print("arrival and seated")
    print("arrival and seated")
    print("arrival and seated")
    print("arrival and seated")
    print("arrival and seated")


def get_reservations_by_restaurant(restaurant_id):

    return db.session.query(Reservation).filter_by(restaurant_id=restaurant_id)


def get_pending_reservations_by_restaurant(restaurant_id):

    return Reservation.query.filter(Reservation.arrival_time == None, Reservation.restaurant_id == restaurant_id).all()


def get_current_reservations_by_restaurant(restaurant_id):

    return Reservation.query.filter(Reservation.arrival_time != None, Reservation.end_time == None, Reservation.restaurant_id == restaurant_id).all()


def get_past_reservations_by_restaurant(restaurant_id):

    return Reservation.query.filter(Reservation.arrival_time != None, Reservation.end_time != None, Reservation.restaurant_id == restaurant_id).all()


def table_match(party_num, tables):
    # booth_pref,
    table_matches = []
    for table in tables.tables:
        print(f"checking {table.table_id}")
        if int(party_num) <= table.num_seats:
            # empty = table.num_seats - int(party_num)
            print(f"table {table.table_id} is a match ")
            table_matches.append(table.table_id)

        else:
            print(
                f"table {table.table_id} is NOT a match  it has {party_num} and {table.num_seats}")

    print("")
    print("")
    print("")
    print(table_matches)
    print("the above tables match the requirements")
    return table_matches  # Return list of table ids that it matches with

# NOTE: Goal:  get table id for each reservation and times of assigned reservations with that table


def open_time_slot(restaurant_id, qualified_tables, res_time, expected_time):

    print("IF YOU MADE IT HERE")
    unseated = Reservation.query.filter(
        Reservation.arrival_time == None,  Reservation.restaurant_id == restaurant_id).all()
    banned_table = []
    for t in unseated:

        if t.table_id in qualified_tables:

            if t.res_time <= res_time and res_time <= t.expected_time:
                print(f"new reservation times: {res_time} - {expected_time}")
                print(
                    f"previously made res times: {t.res_time} - {t.expected_time}")
                print(
                    f" case 1")
                print(f"{t.table_id} maps as :")
                print(
                    f"-----------")
                print(
                    f"     ------------")
                print("THIS IS BEING REMOVED CONFIRM IS THIS CORRECT")
                # qualified_tables.pop(t.table_id)
                banned_table.append(t.table_id)
                print(banned_table)

            if res_time <= t.res_time and t.res_time <= expected_time:
                print(f"new reservation times: {res_time} - {expected_time}")
                print(
                    f"previously made res times: {t.res_time} - {t.expected_time}")
                print(f"{t.table_id} maps as :")
                print(
                    "case 2")

                print(
                    f"          ----------------")
                print(
                    f" ----------------")
                print("THIS IS BEING REMOVED CONFIRM IS THIS CORRECT")
                # qualified_tables.pop(t.table_id)
                banned_table.append(t.table_id)
                print(banned_table)

            if t.res_time <= res_time and expected_time <= t.expected_time:
                print(f"new reservation times: {res_time} - {expected_time}")
                print(
                    f"previously made res times: {t.res_time} - {t.expected_time}")
                print(f"{t.table_id} maps as :")

                print(
                    f"case 3")
                print(
                    f"---------------------------")
                print(
                    f"      ------      ")
                print("THIS IS BEING REMOVED CONFIRM IS THIS CORRECT")
                # qualified_tables.pop(t.table_id)
                banned_table.append(t.table_id)
                print(banned_table)

            if res_time <= t.res_time and t.expected_time <= expected_time:
                print(f"new reservation times: {res_time} - {expected_time}")
                print(
                    f"previously made res times: {t.res_time} - {t.expected_time}")
                print(f"{t.table_id} maps as :")
                print(
                    f"case 4")

                print(
                    f"   -----    ")
                print(
                    f"-----------------")
                print("THIS IS BEING REMOVED CONFIRM IS THIS CORRECT")
                # qualified_tables.pop(t.table_id)
                banned_table.append(t.table_id)
                print(banned_table)

    print("final")
    print(banned_table)
    print("this is the final list of banned tables")
    print("")
    print("")
    print("")
    print("these are still qualified")
    qt_set = set(qualified_tables)
    print("qt_set")
    print("set of qualified")
    print(qt_set)
    print("set of banned tables")
    banned = set(banned_table)
    print(banned)

    f = qt_set - banned
    print("set qt minus banned")
    free_tables = list(f)
    print("does this look right??????")
    print("free tables")
    print(free_tables)
    print('')
    print('')
    print('')
    print('')
    return free_tables


def assign_table(qualified_time_table, res_time, expected_time):

    qt = set(qualified_time_table)
    unseated = Reservation.query.filter(
        Reservation.arrival_time == None, Reservation.table_id.in_(qt))

    print(unseated)
    print("at the fuction assign table")
    print("at the fuction assign table")
    print("at the fuction assign table")
    print(qt)
    print("at the fuction assign table")
    print("at the fuction assign table")
    print("at the fuction assign table")
    table_selected = 0
    smallest_diff = timedelta(2020, 4, 12, 0, 0, 0)
    for t in unseated:
        print("")
        print("this is an instance of i")
        print(t)

        if t.res_time <= res_time and res_time >= t.expected_time:
            res_diff = expected_time - t.res_time
            print(f"smallest_diff {smallest_diff}")
            if res_diff < smallest_diff:
                smallest_diff = res_diff
                table_selected = t.table_id
                print(smallest_diff)
        else:
            res_diff = expected_time - t.res_time
            print(f"smallest_diff {smallest_diff}")
            if res_diff < smallest_diff:
                smallest_diff = res_diff
                table_selected = t.table_id
                print(smallest_diff)
    print(smallest_diff, table_selected)
    if smallest_diff == timedelta(2020, 4, 12, 0, 0, 0):
        return qualified_time_table[0]
    else:
        return table_selected


def get_unseated_by_restaurant(restaurant_id):

    two_hour_before = datetime.now() - timedelta(hours=2)
    hour_after = datetime.now() + timedelta(hours=1)
    print(two_hour_before)
    print(' two hours before ')

    print('until an hour after')
    print(hour_after)
    print(type(hour_after))

    unseated_upcoming = Reservation.query.filter(Reservation.arrival_time == None, Reservation.restaurant_id == restaurant_id,
                                                 Reservation.res_time < hour_after, Reservation.res_time > two_hour_before).order_by(Reservation.res_time.desc()).all()

    print(
        f"here is the first option original____________________________________________________\n\n\n\n {unseated_upcoming}")

    return unseated_upcoming
