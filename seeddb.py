import model
import os
import json
from random import random
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

    restaurant = model.Restaurant(
        username=username, password=password, restaurant_name=restaurant_name)
    model.db.session.add(restaurant)
    model.db.session.commit()

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
