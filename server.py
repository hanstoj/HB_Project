from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from model import connect_to_db
from crud import get_restaurant_by_username, get_table_by_table_num, create_res, create_table, create_restaurant, get_restaurant_by_restaurant_id, get_tables


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/home')
def TableTime():
    """View homepage."""
    tables = get_tables()

    return render_template('table_time.html', tables=tables)


@app.route('/')
def login_page():
    """View homepage."""

    return render_template('log_in.html')


@app.route('/create_acct')
def display_acct_page():
    """Display Acct Creation Page"""

    return render_template("create_acct.html")


@app.route('/create_acct', methods=['POST'])
def create_acct():
    """Create Acct"""

    username = request.form.get('username')
    password = request.form.get('password')
    restaurant_name = request.form.get('restaurant_name')
    open_time = request.form.get('open_time')
    close_time = request.form.get('close_time')

    restaurant = get_restaurant_by_username(username)
    if restaurant:
        flash('Cannot create an account with that email. Try again.')
        # return redirect('/layout')
    else:
        create_restaurant(username, restaurant_name,
                          password, open_time, close_time)
        #

        return render_template('layout.html')
        # redirect('/layout')

# @app.route('/<user_id>/profile')
# def show_profile(user_id):


@app.route('/layout/<restaurant_id>')
def display_layout_page(restaurant_id):
    """Display layout Creation Page"""
    restaurant_id = get_restaurant_by_restaurant_id(restaurant_id)

    return render_template("layout.html", restaurant_id=restaurant_id)


@ app.route('/layout', methods=['POST'])
def view_layout_page():
    """View Acct Page"""
    table_num = request.form.get('table_num')
    is_booth = request.form.get('is_booth')
    num_seats = request.form.get('num_seats')

    if is_booth == "True":
        is_booth = True
    else:
        is_booth = False

    table = get_table_by_table_num(table_num)
    if table:
        flash('Table number already exists cannot create')
    else:
        create_table(table_num=table_num,
                     is_booth=is_booth, num_seats=num_seats)
        flash('Table was created')
        #
        # TODO create visual table
    return render_template('layout.html')


@app.route('/make_res')
def display_res_page():
    """Display Res Creation Page"""

    return render_template("make_res.html")


@ app.route('/make_res', methods=['POST'])
def make_reservation():
    """Resrevation form submission response"""

    res_size = request.form.get('res_size')
    res_time = request.form.get('res_time')
    res_notes = request.form.get('res_notes')
    arrival_time = request.form.get('arrival_time')
    end_time = request.form.get('end_time')
    booth_pref = request.form.get('booth_pref')
    celebrating = request.form.get('celebrating')
    phone_num = request.form.get('phone_num')

    # TODO Start time conditional -html?

    # TODO End time conditional- html?
    # TODO Bookings Full??
    reservation = create_res(res_size=res_size, res_time=res_time, res_notes=res_notes, arrival_time=arrival_time,
                             end_time=end_time, booth_pref=booth_pref, celebrating=celebrating, phone_num=phone_num)

    redirect('/make_res', reservation=reservation)


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
