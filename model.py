from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Restaurant(db.Model):
    """A Restaurant."""

    __tablename__ = 'restaurants'

    restaurant_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    restaurant_name = db.Column(db.String)
    open_time = db.Column(db.Time)  # Store in a datetime.datetime object
    close_time = db.Column(db.Time)

    # NOTE: To convert time obj to a string in backend  time_str = str(time_obj)

    def __repr__(self):
        return f'<Restaurant restaurant_id={self.restaurant_id} password={self.password} restaurant_name={self.restaurant_name}>'
# resttest = Restaurant(username="user", password="password", restaurant_name="restaurant_name"


class Dinning_table(db.Model):
    """A Table in the restaurant."""

    __tablename__ = 'tables'

    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_num = db.Column(db.String)
    is_booth = db.Column(db.Boolean, default=True)
    num_seats = db.Column(db.Integer)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.restaurant_id'))

    # reservation_id = db.Column(
    #     db.Integer, db.ForeignKey('reservations.res_id'))

    restaurants = db.relationship("Restaurant", backref="tables")
    reservation = db.relationship("Reservation")

    # restaurant = db.relationship('Restaurant')
    # reservation = db.relationship('Reservation')

    def __repr__(self):
        return f'<Dinning_table table_id={self.table_id} table_num={self.table_num} booth={self.is_booth} num_seats={self.num_seats} restaurant_id={self.restaurant_id}>'


class Reservation(db.Model):
    """A reservation."""

    __tablename__ = 'reservations'

    res_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'))
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    party_num = db.Column(db.Integer)
    res_date = db.Column(db.DateTime)
    res_time = db.Column(db.DateTime)
    expected_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    booth_pref = db.Column(db.Boolean)
    res_notes = db.Column(db.Text)
    is_celebrating = db.Column(db.Boolean)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'))

    # phone_num = db.Column(db.String, db.ForeignKey('guests.phone_num'))
    restaurant = db.relationship('Restaurant', backref="reservations")
    guest = db.relationship('Guest')
    table = db.relationship('Dinning_table')
    # guest_stats = db.relationship('Guest_stat')

    def __repr__(self):
        return f'<Reservation res_id={self.res_id} restaurant_id= {self.restaurant_id} table_id = {self.table_id} party_num={self.party_num} expected_time = {self.expected_time} res_time={self.res_time} arrival_time={self.arrival_time} end_time={self.end_time}booth_pref={self.booth_pref} res_notes={self.res_notes}  celebrating={self.is_celebrating} >'


class Guest(db.Model):
    """A reservation."""

    __tablename__ = 'guests'

    guest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    guest_name = db.Column(db.String)
    phone_num = db.Column(db.String, unique=True)
    avg_time_spent = db.Column(db.Integer)
    num_visits = db.Column(db.Integer)

    reservation = db.relationship('Reservation')
    # guest_stats = db.relationship('Guest_stat')

    def __repr__(self):
        return f'<Guest guest_id={self.guest_id} phone_num={self.phone_num}> avg_time_spent{self.avg_time_spent} num_visits={self.num_visits}'
# resttest = Restaurant(username="user", password="password", restaurant_name="restaurant_name")


# class Guest_stat(db.Model):
#     """A Guest's stats."""

#     __tablename__ = 'guest_stats'

#     guest_stats_id = db.Column(
#         db.Integer, autoincrement=True, primary_key=True)
#     guest_notes = db.Column(db.String, unique=True)
#     num_visits = db.Column(db.Integer)
#     avg_time_spent = db.Column(db.DateTime)
#     guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'))

#     guest = db.relationship('Guest')

    # def __repr__(self):
    #     return f'<Guest_stats guest_stats_id={self.guest_stats_id} guest_notes={self.guest_notes}num_visits={self.num_visits} avg_time_spent={self.avg_time_spent}res_time={self.} phone_num={self.phone_num}>'


def connect_to_db(flask_app, db_uri='postgresql:///cafe', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
