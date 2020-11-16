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


@app.route('/create_acct')
def view_acct_page():
    """View homepage."""

    return render_template('create_acct.html')


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

    return render_template('layout.html')
# @app.route('/make_res')
# def view_make_res():
#     """View Res Page"""

#     return render_template('make_res.html')


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
