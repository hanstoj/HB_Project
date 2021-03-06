from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from model import connect_to_db, Guest
from crud import get_restaurant_by_username, get_table_by_table_num, create_res, create_table, create_restaurant, get_restaurant_by_restaurant_id, get_tables_by_restaurant_id, create_guest,  get_guest_by_id, date_match, expected_time_calc, get_guest_by_phone_num, get_pending_reservations_by_restaurant, get_current_reservations_by_restaurant, get_past_reservations_by_restaurant, table_match, get_reservations_by_restaurant, open_time_slot, get_unseated_by_restaurant, assign_table, update_guest_seating_time, update_reservation_arrival_time, update_finished_time, get_guest
from dateutil import parser
from arrow import arrow
from datetime import datetime, timedelta

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# --------------------------------------------------------------------------------------
#    Account Creation
# --------------------------------------------------------------------------------------


@app.route('/')
def login_page():
    """View Login."""
    #
    return render_template('log_in.html')


@app.route('/login_form', methods=['POST'])
def login_form_submit():


"""Submit login form."""
username = request.form.get('username')
password = request.form.get('password')
restaurant = get_restaurant_by_username(username)

   if restaurant.password == password:
        session['restaurant'] = restaurant.restaurant_id

    else:
        flash('Logged in')

    session['restaurant_id'] = restaurant.restaurant
    tables = get_tables_()

    return render_template('table_time.html')


@app.route('/create_acct')
def display_acct_page():
    """Display Acct Creation Page"""

    return render_template("create_acct.html")


@app.route('/create_acct_form', methods=['POST'])
def create_acct():
    """Create Acct"""

    username = request.form.get('username')
    password = request.form.get('password')
    restaurant_name = request.form.get('restaurant_name')
    open_time = request.form.get('open_time')
    close_time = request.form.get('close_time')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('passwords do not match.')
        return render_template('create_acct.html')

    create_restaurant(username, restaurant_name,
                      password, open_time, close_time)

    this_restaurant = get_restaurant_by_username(username)

    session['restaurant_id'] = this_restaurant.restaurant_id

    return redirect('/layout/')
    #


# --------------------------------------------------------------------------------------
    #    Table Layout
# --------------------------------------------------------------------------------------


@app.route('/layout/')
def display_layout_page():
    """Display layout Creation Page"""

    return render_template("layout.html")


@ app.route('/layout_form/', methods=['POST'])
def view_layout_page():
    """View Acct Page"""
    table_num = request.form.get('table_num')
    is_booth = request.form.get('is_booth')
    num_seats = request.form.get('num_seats')
    restaurant_id = session['restaurant_id']

    if is_booth == "True":
        is_booth = True
    else:
        is_booth = False

    create_table(table_num=table_num,
                 is_booth=is_booth, num_seats=num_seats, restaurant_id=restaurant_id)
    flash('Table was created')

    return render_template('layout.html')


# --------------------------------------------------------------------------------------
    #    Main Page
# --------------------------------------------------------------------------------------


@app.route('/TableTime')
def TableTime():
    """View homepage."""
    restaurant_id = session['restaurant_id']

    tables = get_tables_by_restaurant_id(restaurant_id)

    unseated_upcoming = get_unseated_by_restaurant(restaurant_id)

    current_res = get_current_reservations_by_restaurant(restaurant_id)
    guests = get_guest()

    return render_template('table_time.html', tables=tables, unseated_upcoming=unseated_upcoming, current_res=current_res, guests=guests)


@app.route('/seated', methods=['POST'])
def update_seating_page():
    guest_id = request.form.get('seated')
    print("THIS IS THE Guest BEING TAKEN IN")
    print(guest_id)
    print("THIS IS THE G BEING TAKEN IN")
    print(guest_id)
    print("THIS IS THE G BEING TAKEN IN")

    res_id = request.form.get('seated_r')

    print("THIS IS THE RES BEING TAKEN IN")
    print(res_id)
    print("THIS IS THE RES BEING TAKEN IN")
    print(res_id)
    print("THIS IS THE RES BEING TAKEN IN")
    print(res_id)
    seated_time = datetime.now()

    update_guest_seating_time(guest_id, seated_time)

    update_reservation_arrival_time(res_id, seated_time)

    restaurant_id = session['restaurant_id']

    tables = get_tables_by_restaurant_id(restaurant_id)

    unseated_upcoming = get_unseated_by_restaurant(restaurant_id)
    current_res = get_current_reservations_by_restaurant(restaurant_id)
    guests = get_guest()
    return render_template('table_time.html', tables=tables, unseated_upcoming=unseated_upcoming, guests=guests, current_res=current_res)


@app.route('/finished', methods=['POST'])
def collect_finished_data():
    guest_id = request.form.get('finished_g')
    res_id = request.form.get('finished_r')

    finished_time = datetime.now()
    print(guest_id)
    print(res_id)
    print(finished_time)

    update_finished_time(res_id, guest_id, finished_time)
    print("GUEST ID FOLLOWED BY SEATED ID")
    print("GUEST ID FOLLOWED BY SEATED ID")
    print("GUEST ID FOLLOWED BY SEATED ID")

    restaurant_id = session['restaurant_id']

    tables = get_tables_by_restaurant_id(restaurant_id)

    unseated_upcoming = get_unseated_by_restaurant(restaurant_id)

    current_res = get_current_reservations_by_restaurant(restaurant_id)
    print(current_res)
    print("this is the problem")
    guests = get_guest()
    return render_template('table_time.html', tables=tables, unseated_upcoming=unseated_upcoming, current_res=current_res, guests=guests)


# --------------------------------------------------------------------------------------
    #    Reservation
# --------------------------------------------------------------------------------------


@app.route('/make_res')
def display_res_page():
    """Display Res Creation Page"""
    restaurant_id = session['restaurant_id']
    restaurant = get_restaurant_by_restaurant_id(restaurant_id)
    return render_template("make_res.html", restaurant=restaurant)


@ app.route('/make_res_form', methods=['POST'])
def make_reservation():
    """Resrevation form submission response"""

    guest_name = request.form.get('guest_name')
    phone_num = request.form.get('phone_num')
    party_num = request.form.get('party_num')
    res_date = request.form.get('res_date')
    res_time = request.form.get('res_time')
    res_notes = request.form.get('res_notes')

    booth_pref = request.form.get('booth_pref')
    is_celebrating = request.form.get('is_celebrating')

    restaurant_id = session['restaurant_id']

    res_date = parser.parse(res_date)
    res_time = parser.parse(res_time)
    # changing to datetime

    if is_celebrating == "True":
        is_celebrating = True
    else:
        is_celebrating = False

    if booth_pref == "True":
        booth_pref = True
    else:
        booth_pref = False

    tables = get_tables_by_restaurant_id(restaurant_id)
    # gets tables in the restaurant

    qualified_tables = table_match(party_num, booth_pref, tables)
    if qualified_tables == []:
        flash('Unfortunately this restaurant can not accomidate tables of that size')
        return redirect('/make_res')
    # checks which tables match requirements- retuns list of table objects
    # TODO reenter booth logic after testing

    res_check = get_pending_reservations_by_restaurant(restaurant_id)
    print('')
    print('')
    print('')
    print(f"reservations waiting {res_check}")

    g = get_guest_by_phone_num(phone_num)
    print(g)
    print(g)

    if g != None:
        guest = g

    else:
        guest = create_guest(phone_num=phone_num, guest_name=guest_name)

    expected = expected_time_calc(
        party_num, is_celebrating, guest.avg_time_spent)

    # calculates expected minutes a guest may stay

    expected_time = res_time + timedelta(minutes=expected)
    # converts to relevant format
    print(expected_time)
    print("expected_time")
    print("expected_time")
    print("expected_time")
    print("expected_time")
    print("expected_time")
    print("expected_time")
    print("expected_time")

    qualified_time_table = open_time_slot(
        restaurant_id, qualified_tables, res_time, expected_time)
    print(qualified_time_table)
    qual = len(qualified_time_table)
    print(qual)
    if qual == 0:
        while qual == 0:

            res_time = res_time + timedelta(minutes=10)
            expected_time = expected_time + timedelta(minutes=10)
            print("NEW RES TIME!")
            print("NEW RES TIME!")
            print("NEW RES TIME!")
            print(res_time)
            print(type(res_time))

            qualified_time_table = open_time_slot(
                restaurant_id, qualified_tables, res_time, expected_time)

            qual = len(qualified_time_table)

        print(qualified_time_table)
        print("ALL THE WAY BACK HERE")
        print("ALL THE WAY BACK HERE")
        print("ALL THE WAY BACK HERE")
        print("ALL THE WAY BACK HERE")
        print("ALL THE WAY BACK HERE")

        alert_m = res_time.time()
        print(alert_m)
        flash(
            f'There are no tables avaliable at this time, The next expected avaliablity for this table is {alert_m}')
        return redirect('/make_res')
    elif qual == 1:
        print("ARE WE GETTING HERE")
        table_id = qualified_time_table[0]
    else:
        table_id = assign_table(qualified_time_table,
                                res_time, expected_time)
    print(table_id)

    # checks booked times for reservations not yet seated that fit the table requirements

    # retrieves for display

    # if open_time_slot == None:
    #     return print("THERE ARE NO OPEN TIMES THAT MATCH THIS REQUEST \n\n\n\n")
    # # reservations = get_reservation_by_table_and_time(tables)
    # else:
    reservation = create_res(guest_id=guest.guest_id, restaurant_id=restaurant_id, party_num=party_num,  res_date=res_date, res_time=res_time, expected_time=expected_time,
                             res_notes=res_notes, booth_pref=booth_pref, is_celebrating=is_celebrating, table_id=table_id)
    # creates reservation
    unseated_upcoming = get_unseated_by_restaurant(restaurant_id)
    current_res = get_current_reservations_by_restaurant(restaurant_id)
    print(current_res)
    print(reservation)
    guests = get_guest()
    return render_template('table_time.html', guest=guest,
                           reservation=reservation, guests=guests, tables=tables, unseated_upcoming=unseated_upcoming, current_res=current_res)


@app.route('/guest_info')
def display_guest_info():
    """Display guest information Page"""

    guests = get_guest()

    # sort by restaurant
    return render_template("guest_info.html", guests=guests)


#
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
