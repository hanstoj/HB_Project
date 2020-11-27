from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from model import connect_to_db
from crud import get_restaurant_by_username, get_table_by_table_num, create_res, create_table, create_restaurant, get_restaurant_by_restaurant_id, get_tables_by_restaurant_id, create_guest, get_all_guests, get_guest_by_id


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def login_page():
    """View Login."""
    #
    return render_template('log_in.html')


@app.route('/login_form', methods=['POST'])
def login_form_submit():
    """Submit login form."""
    # username = request.form.get('username')
    # password = request.form.get('password')

    # restaurant = get_restaurant_by_username(username)
    # if restaurant.password == password:
    #     session['restaurant'] = restaurant.restaurant_id

    # else:
    #     flash('Logged in')

    # #
    # #     session['restaurant_id']= restaurant.restaurant
    # tables = get_tables_()

    return render_template('table_time.html', )


# @app.route('/', methods=[POST])
# def login_page():
#     """View homepage."""


#     return render_template('log_in.html')


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

    # restaurant = get_restaurant_by_restaurant_id(session['restaurant_id'])

    # restaurant = get_restaurant_by_username(username)
    # if restaurant:
    #     flash('Cannot create an account with that email. Try again.')
    #     # return redirect('/layout')
    # else:

    # render_temp late('layout.html')
    # pass in rest id as variable
    return redirect('/layout/')
    #


# <restaurant_id>
@app.route('/layout/')
def display_layout_page():
    """Display layout Creation Page"""

    restaurant_id = session['restaurant_id']

    return render_template("layout.html", restaurant_id=restaurant_id)


@ app.route('/layout_form/', methods=['POST'])
def view_layout_page():
    """View Acct Page"""
    table_num = request.form.get('table_num')
    is_booth = request.form.get('is_booth')
    num_seats = request.form.get('num_seats')
    restaurant_id = session['restaurant_id']

    # options: grab from cookie
    # add invisible form

    if is_booth == "True":
        is_booth = True
    else:
        is_booth = False

    table = get_table_by_table_num(table_num)
    if table:
        flash('Table number already exists cannot create')
    else:
        create_table(table_num=table_num,
                     is_booth=is_booth, num_seats=num_seats, restaurant_id=restaurant_id)
        flash('Table was created')
        #
        # TODO fix flash
    return render_template('layout.html')


@app.route('/TableTime')
def TableTime():
    """View homepage."""
    restaurant_id = session['restaurant_id']

    print()
    print("THE RESTAURANT_ID IS:", restaurant_id)

    tables = get_tables_by_restaurant_id(restaurant_id)
    print()
    print("THE TABLES SHOWN ARE:", tables)
    print(tables)
    print()

    return render_template('table_time.html', tables=tables)


# options: add cookie  - later in exp access
# pull out id  -
# add id as cookie
# in addition /<restid> - if layout structured this way only accepts get or post
# -flask cant read cookies


# if redirect- layout -> restaurant id take with it

# @app.route('/<user_id>/profile')
# def show_profile(user_id):

@app.route('/make_res')
def display_res_page():
    """Display Res Creation Page"""

    return render_template("make_res.html")


@ app.route('/make_res_form', methods=['POST'])
def make_reservation():
    """Resrevation form submission response"""

    guest_name = request.form.get('guest_name')
    phone_num = request.form.get('phone_num')
    party_num = request.form.get('party_num')
    res_date = request.form.get('res_date')
    res_time = request.form.get('res_time')
    res_notes = request.form.get('res_notes')
    # arrival_time = request.form.get('arrival_time')
    # end_time = request.form.get('end_time')
    booth_pref = request.form.get('booth_pref')
    is_celebrating = request.form.get('is_celebrating')

    if is_celebrating == "True":
        is_celebrating = True
    else:
        is_celebrating = False

    if booth_pref == "True":
        booth_pref = True
    else:
        booth_pref = False

    # TODO Start time conditional -html?
    # TODO End time conditional- html?
    # TODO Bookings Full??
    guest = create_guest(phone_num=phone_num, guest_name=guest_name)

    reservation = create_res(guest_id=guest.guest_id, party_num=party_num,  res_date=res_date, res_time=res_time,
                             res_notes=res_notes, booth_pref=booth_pref, is_celebrating=is_celebrating)
    restaurant_id = session['restaurant_id']
    tables = get_tables_by_restaurant_id(restaurant_id)

    return render_template('table_time.html', guest=guest,
                           reservation=reservation, tables=tables)


@app.route('/guest_info')
def display_guest_info():
    """Display guest information Page"""

    guests = get_all_guests()

    return render_template("guest_info.html", guests=guests)


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

#
if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
