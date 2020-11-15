from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
# from crud import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/home')
def TableTime():
    """View homepage."""

    return render_template('table_time.html')


@app.route('/', methods=['GET'])
def login_page():
    """View homepage."""

    return render_template('log_in.html')


@app.route('/create_acct')
def view_create_acct():
    """View Acct Page"""

    return render_template('create_acct.html')

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
