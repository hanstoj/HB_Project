from model import db, Guest, Dinning_table, Restaurant, Reservation, connect_to_db
from dateutil import parser
from dateutil.parser import parse
from arrow import arrow
from datetime import datetime, time, timedelta

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


def create_table(table_num, is_booth, num_seats, restaurant_id):
    """Create Table in Restaurant"""
    table = Dinning_table(table_num=table_num, is_booth=is_booth,
                          num_seats=num_seats, restaurant_id=restaurant_id)

    db.session.add(table)
    db.session.commit()

    return table


def get_table_by_table_num(table_num):

    return Dinning_table.query.filter(Dinning_table.table_num == table_num).first()


def create_res(guest_id, restaurant_id, party_num, res_date, res_time, expected_time, res_notes, booth_pref, is_celebrating, table_id, end_time=None, arrival_time=None):
    """Create and return a restaurant."""

    reservation = Reservation(guest_id=guest_id, restaurant_id=restaurant_id, party_num=party_num, res_date=res_date, res_time=res_time, expected_time=expected_time, res_notes=res_notes,
                              booth_pref=booth_pref, is_celebrating=is_celebrating, table_id=table_id, end_time=end_time, arrival_time=arrival_time)
    db.session.add(reservation)
    db.session.commit()

    return reservation


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


# def get_guest_by_phone_num(phone_num):

#     return Guest.query.


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


def date_match(res_date):

    if (datetime.today() - res_date).days == 0:
        return print("date match")


def get_guest_by_phone_num(phone_num):

    return Guest.query.get(phone_num)


def expected_time_calc(party_num, is_celebrating, avg_time_spent):

    print(f"{party_num}, {is_celebrating}, {avg_time_spent}")

    expected = avg_time_spent

    if int(party_num) > 5:
        expected = expected + 20
        print(f"over 6 expected update: {expected}")
    if is_celebrating:
        expected = expected + 20
        print(f"is celebraing update: {expected}")

    return expected


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
        if int(party_num) <= table.num_seats:
            seats = True
        else:
            seats = False
            print("no booths currently avalible, continue without booth?")
        if seats == True:
            table_matches.append(table.table_id)
    return table_matches  # Return list of table ids that it matches with

# NOTE: Goal:  get table id for each reservation and times of assigned reservations with that table


def open_time_slot(restaurant_id, qualified_tables, res_time, expected_time):

    print("IF YOU MADE IT HERE")
    unseated = Reservation.query.filter(
        Reservation.arrival_time == None, Reservation.restaurant_id == restaurant_id)

    print(qualified_tables)
    print("qualified")
    print("qualified")
    print("qualified")

    print("starting the loop")
    for t in unseated:
        print(t.res_time)
        print(t.table_id)
        unseatable_tables = []
        print(unseatable_tables)

        for t.table_id in qualified_tables:
            if t.res_time <= res_time and t.expected_time <= expected_time:
                print(
                    f"first res {t.res_time} is less than new res {res_time} ")
                print(
                    f" first exp time {t.expected_time} is before new expected {expected_time}")
                print(f"{t.table_id} maps as :")
                print(
                    f"-----------")
                print(
                    f"     ------------")
                qualified_tables.remove(t.table_id)
                print(qualified_tables)

            if res_time <= t.res_time and expected_time <= t.expected_time:
                print(f"{t.table_id} maps as :")
                print(
                    f"first NEW {res_time} is before the OLD res {t.res_time} ")
                print(
                    f" first NEW exp time {expected_time} is before new expected {t.expected_time}")
                print(
                    f"          ----------------")
                print(
                    f" ----------------")
                qualified_tables.remove(t.table_id)
                print(qualified_tables)

            if t.res_time <= res_time and expected_time <= t.expected_time:
                print(f"{t.table_id} maps as :")
                print(
                    f"first OLD {t.res_time} is before the NEW res {res_time} ")
                print(
                    f" first NEW exp time {expected_time} is before new expected {t.expected_time}")
                print(
                    f"---------------------------")
                print(
                    f"      ------      ")
                qualified_tables.remove(t.table_id)
                print(qualified_tables)

            if res_time <= t.res_time and t.expected_time <= expected_time:
                print(f"{t.table_id} maps as :")
                print(
                    f"first NEW {res_time} is before the OLD res {t.res_time} ")
                print(
                    f" first OLD exp time {expected_time} is before NEW expected {t.expected_time}")
                print(
                    f"   -----    ")
                print(
                    f"-----------------")
                qualified_tables.remove(t.table_id)
                print(qualified_tables)
            print("these are still qualified")

            return qualified_tables


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
    return table_selected

    #     if i.table_id in qt:
    #         print(i.table_id)
    #         print(qt)

    # for t in unseated:
    #     print(t)

    #     smallest_diff = timedelta(2020, 4, 12, 0, 0, 0)
    #     for t in qualified_time_table:
    #         if t.res_time <= res_time and res_time >= t.expected_time:
    #             res_diff = expected_time - t.res_time
    #             print(f"smallest_diff {smallest_diff}")
    #             if res_diff < smallest_diff:
    #                 smallest_diff = res_diff
    #                 table_selected = t.table_id
    #                 print(smallest_diff)

    #         if res_time <= t.res_time and expected_time >= res_time:
    #             res_diff = expected_time - t.res_time
    #             print(f"smallest_diff {smallest_diff}")
    #             if res_diff < smallest_diff:
    #                 smallest_diff = res_diff
    #                 table_selected = t.table_id
    #                 print(smallest_diff)

    #     print(smallest_diff)
    #     print(table_selected)
    #     return table_selected


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


# .order_by(
#         Reservation.res_time.desc()).limit(10).all()
    return unseated_upcoming


#     for table_id, dept_name, phone in table_reservations:      # [(n, d, p), (n, d, p)]
#         print(name, dept_name, phone)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # else conditions for testing

    # if res_time >= t.res_time and res_time <= t.expected_time:
    #         print(
    #             f"res time of {res_time} is after previously booked res_time {t.res_time}")
    #         print(
    #             f"res time of {res_time} is before previously booked estimated_time end time {t.expected_time}")
    #         seatable = False
    #         print(seatable)
    #     if res_time <= t.res_time and expected_time >= t.expected_time:
    #         print(
    #             f"res time of {res_time} is before previously booked res_time  {t.res_time}")
    #         print(
    #             f" and expected time of {expected_time} is after the reservation time {res_time}")

    #         seatable = False
    #         print(seatable)

    # if res_time >= t.res_time and res_time >= t.expected_time:
    #     print(
    #         f"res time of {res_time} is after the previously assigned {t.res_time}")
    #     print(
    #         f" res time of {res_time} is after expected end of expected time{t.expected_time}")

    #     print("Yeah huh")
    # elif res_time <= t.res_time:
    #     print(
    #         f"This res time of {res_time} is before previously booked {t.res_time}")
    #     print("Yeah huh")
    # else:
    #     print("Nu uh")

    # test2 = Dinning_table.query.filter_by(restaurant_id = restaurant_id, table_num = )

    # test_table_id = DiningTable.query.filter_by(resturant_id==desired_resturant, table_num==desired_table).first()

    # res_list = Reservation.query.filter_by(Reservation.arrival_time == None, table_id == test_table_id).all()

    # res_check = Reservation.query.filter(
    # Reservation.table_id == Dinning_table.table_id)

    # .join(DinningTable)

    # NOTE: From SQL ALchemy 2 Lecture Notes
    # emps = db.session.query(Emplyee, Department).join(Department).all()

    # you can do this
# if product.favorite[0].user_id == user_id:


# if you make a relationship like this

# favorite = db.relationship("Favorite")
# product = product.query.filter(aldkfjlakdjf)
# product.favorite

    # products = db.session.query(Product).select_from(Product).join(Favorite, Favorite.product_id == Product.product_id).filter(Favorite.user_id == user_id).all()

    # print(f"THIS IS RES_CHECK {res_check}")  # Identify the tables

    # table_match(party_num, booth_pref, tables):

    # find table id = 1 assocatied with each resrvation id = 1
    # check start_times reservations associated with that table
    # check finish_times reservations associated with that table
    # print()
#     # [<Reservation res_id=1 table_id = None party_num=4 expected_time = 2020-12-03 14:35:00 res_time=2020-12-03 13:50:00 arriv
#     print("THIS IS TEST VARIABLE:", test)
# # al_time=None end_time=Nonebooth_pref=False res_notes=  celebrating=False >

#     for i in test:
#         print("WHAT IS THIS:", i.res_id)

#     # for i in test.table:
#     #     print("IS THIS THE TABLE ID?", i.table_id)

#     # check = db.session.query(Reservation.table_id,
#     #                          Dinning_table.reservation_id,
#     #                          Reservation.res_time, Reservation.expected_time).join(Reservation).all()
#     # q.group_by('state').all()
#     # q.group_by('state').having(db.func.count(Employee.employee_id) > 2).all()
#     print("If the Above executes..")
#     # for table_id, reservation_id, res_time, expected_time in check:

#     #     return print(table_id, reservation_id, res_time, expected_time)

#     # tables = Dinning_table.query.options(db.joinedload('reservation')).all()
#     # print(tables)

#     #     for table in tables:    # [<Emp>, <Emp>]
#     #         if emp.dept is not None:
#     #             print(emp.name, emp.dept.dept_code, emp.dept.phone)
#     #         else:
#     #             print(emp.name, "-", "-")
#     #     for table in qualified_tables:
#     #         print(table)
#     #         print(table.res_time)
#     #         print(table.expected_time)

#     # if table.res_time > expected_time:
#     #     print("")
#     #     print(f"table.res {table.res}")
#     #     print ("is greater than")
#     #     print(f"table.res {expected_time}")
#     # if table.expected_time > res_time:
#     #     print("")
#     #     print
#     #

#     # pass
# # def check_logic():

# #     time_expected = 45
# #     start_time = datetime.now()

# #     finish_time = start_time + timedelta(minutes=time_expected)
# #     print(f"start time {start_time}")
# #     print(f"finish time {finish_time}")

# #     for table where match


# # def get_

# # def seating_order():

# slack_time = ( res_time - seated_time - e' )
# if table open from arrivaltime to expected end seat table
#
# for table where requirements met

# if table is open from time to time
# reserve table

# while True:

#     if task_queue.is_empty():
#         next_task = None
#     else:
#         next_task = task_queue.peek()

#     print("Next task:", next_task)

#     command = input("A)dd task, D)o first task, or Q)uit? ")

#     if command == "A":
#         task = input("Task: ")
#         task_queue.enqueue(task)

#     elif command == "D":
#         print("Completed:", task_queue.dequeue())

#     elif command == "Q":
#         break

#     else:
#         print("*** Invalid command; try again ***")

# def table_match():

# if table_seats >= party_num:
#     print("seats match")

# if booth_pref == is_booth:
#     print("booth match")

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
