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
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)

    def __repr__(self):
        return f'<Restaurant restaurant_id={self.restaurant_id} email={self.email} password={self.password} restaurant_name={self.restaurant_name}>'
# resttest = Restaurant(username="user", password="password", restaurant_name="restaurant_name"


class Table(db.Model):
    """A Table in the restaurant."""

    __tablename__ = 'tables'

    table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_num = db.Column(db.String, unique=True)
    booth = db.Column(db.Boolean)
    num_seats = db.Column(db.Integer)
    table_status = db.Column(db.Boolean)
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    res_id = db.Column(db.Integer, db.ForeignKey('reservations.res_id'))

    restaurant = db.relationship('Restaurant', backref='tables')
    reservation = db.relationship('Reservation')

    def __repr__(self):
        return f'<Table table_id={self.table_id} table_num={self.table_num} booth={self.booth} restaurant_name={self.num_seats}table_status={self.table_status} table_hours={self.table_hours} restaurant_id={self.restaurant_id}>'


class Reservation(db.Model):
    """A reservation."""

    __tablename__ = 'reservations'

    res_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    res_size = db.Column(db.Integer)
    res_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    booth_pref = db.Column(db.Boolean)
    res_notes = db.Column(db.Text)
    celebrating = db.Column(db.Boolean)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'))
    phone_num = db.Column(db.String, db.ForeignKey('guests.phone_num'))

    guest = db.relationship('Guest')
    table = db.relationship('Table')
    guest_stats = db.relationship('Guest_stat')

    def __repr__(self):
        return f'<Reservation res_id={self.res_id} res_size={self.res_size} phone_num={self.phone_num} res_size={self.res_size}res_time={self.res_time} arrival_time={self.arrival_time} end_time={self.end_time}booth_pref={self.booth_pref} res_notes={self.res_notes}table_id={self.table_id} celebrating={self.celebrating} >'


class Guest(db.Model):
    """A reservation."""

    __tablename__ = 'guests'

    guest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    phone_num = db.Column(db.String, unique=True)

    reservation = db.relationship('Reservation')
    guest_stats = db.relationship('Guest_stat')

    def __repr__(self):
        return f'<Reservation res_id={self.res_id} res_size={self.res_size} phone_num={self.phone_num}>'
# resttest = Restaurant(username="user", password="password", restaurant_name="restaurant_name")


class Guest_stat(db.Model):
    """A Guest's stats."""

    __tablename__ = 'guest_stats'

    guest_stats_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    guest_notes = db.Column(db.String, unique=True)
    num_visits = db.Column(db.Integer, autoincrement=True)
    avg_time_spent = db.Column(db.DateTime)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'))
    res_id = db.Column(db.Integer, db.ForeignKey('reservations.res_id'))

    guest = db.relationship('Guest')
    reservation = db.relationship('Reservation')

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
