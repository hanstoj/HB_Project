import model
import os
import json
from random import random, randint
import datetime

import crud
import server
import model

from faker import Faker
fake = Faker()


os.system('dropdb cafe')
os.system('createdb cafe')

model.connect_to_db(server.app)
model.db.create_all()

for restaurant in range(5):
    username = fake.word()
    password = fake.password()
    restaurant_name = fake.name()
    # open_time = datetime(2019, 1, 1, 0, 0, 0, 0)
    # closing_time = datetime(2019, 1, 1, 0, 0, 0, 0)

    restaurant = model.Restaurant(
        username=username, password=password, restaurant_name=restaurant_name)
    model.db.session.add(restaurant)
    model.db.session.commit()

    for table in range(8):
        table_num = randint(1, 9)
        booth = fake.boolean()
        num_seats = randint(1, 6)
        table_status = fake.boolean()

    # for


#     table_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     table_num = db.Column(db.String, unique=True)
#     booth = db.Column(db.Boolean)
#     num_seats = db.Column(db.Integer)
#     table_status = db.Column(db.Boolean)
#     table_hours = db.Column(db.DateTime)
#     restaurant_id = db.Column(
#         db.Integer, db.ForeignKey('restaurants.restaurant_id'))
#     res_id = db.Column(db.Integer, db.ForeignKey('reservations.res_id'))

#     restaurant = db.relationship('Restaurant', backref='tables')
#     reservation = db.relationship('Reservation')
    # for reservation in range(10):
    #     res_size = random.randint(1, 4)
    #     res_time = datetime.today()
    #     # faker how to get reasonable times
    #     arrival_time = res_time
    #     end_time = arrival_time +
    #     booth_pref = fake.boolean()
    #     res_notes = db.Column(db.Text)
    #     celebrating = db.Column(db.Boolean)
    #     table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'))
    #     phone_num = db.Column(db.String, db.ForeignKey('guests.phone_num'))

    # for guests in range(50):
    #     name = fake.name()
    #     phone_num = fake.unique.phone()

    #     guest = model.Guest(name=name, phone_num=phone_num)
    #     model.db.session.add(guest)
    #     model.db.session.commit()

    # for reservation in range(10):
    #     res_size = random.randint(1, 4)
    #     res_time = datetime.today()
    #     # faker how to get reasonable times
    #     arrival_time = res_time
    #     end_time = arrival_time +
    #     booth_pref = fake.boolean()
    #     res_notes = db.Column(db.Text)
    #     celebrating = db.Column(db.Boolean)
    #     table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'))
    #     phone_num = db.Column(db.String, db.ForeignKey('guests.phone_num'))
