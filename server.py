from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/home')
def TableTime():
    """View homepage."""

    return render_template('table_time.html')


@app.route('/')
def login_page():
    """View homepage."""
    # username = request.form.get('username')
    # password = request.form.get('password')
    # restaurant_name = request.form.get('restaurant_name')
    # open_time = request.form.get('open_time')
    # close_time = request.form.get('close_time')

    # user = crud.get_user_by_email(username)
    # if user:
    #     flash('Cannot create an account with that username. Try again.')
    # else:
    #     crud.create_user(username, password, restaurant_name,
    #                      open_time, close_time)
    #     flash('Account created!')

    # return redirect('/')

    return render_template('log_in.html')


@app.route('/create_acct', methods=['POST'])
def create_acct():
    """Create Acct"""
    username = request.form.get('username')
    password = request.form.get('password')
    restaurant_name = request.form.get('restaurant_name')
    open_time = request.form.get('open_time')
    close_time = request.form.get('close_time')

    restaurant = crud.get_restaurant_by_username(username)
    if restaurant:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_restaurant(username, password, restaurant_name,
                               open_time, close_time)
        flash('Account created! Please log in.')
    return render_template('/layout')


@app.route('/layout', methods=['POST'])
def view_layout_page():
    """View Acct Page"""
    table_num = request.form.get('table_num')
    is_booth = request.form.get('is_booth')
    num_seats = request.form.get('num_seats')

    table = crud.get_table_by_table_num(table_num)
    if table:
        flash('Table number already exists cannot create')
    else:
        crud.create_table(table_num=table_num,
                          is_booth=is_booth, num_seats=num_seats)

    return table


@app.route('/make_res', methods=['POST'])
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

    # TODO Start time conditional
    # TODO End time conditional
    # TODO Bookings Full?
    reservation = crud.create_res(res_size=res_size, res_time=res_time, res_notes=res_notes, arrival_time=arrival_time,
                                  end_time=end_time, booth_pref=booth_pref, celebrating=celebrating, phone_num=phone_num)

    redirect('/make_res', reservation=reservation)


# @app.route('/create_acct')
# def create_acct():
#     """create acct"""


# @app.route('/<guest_id>')
# def show_user(guest_id):
#     """Show details on a particular guest."""

#     guest = crud.get_guest_by_id(guest_id)

#     return render_template('user_details.html', guest=guest)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
