import model
import os
import json
from random import random
from datetime import datetime

import crud
from model import connect_do_db, db, Restaurant,
import server


from faker import faker
fake = Faker()


os.system('dropdb cafe')
os.system('createdb cafe')

model.connect_to_db(server.app)
model.db.create_all()

for restaurant in range(5):
    username = fake.username()
    password = fake.password()
    restaurant_name = fake.name(length=10)

    restaurant = model.Restaurant(
        username=username, password=password, restaurant_name=restaurant_name)
    model.db.session.add(restaurant_name)
    model.db.session.commit()

    for guests in range(50):
        name = fake.name()
        phone_num = fake.unique.phone()

        guest = model.Guest(name=name, phone_num=phone_num)

        # for reservation in range(200):

        # import os
        # import json
        # from random import choice, randint
        # from datetime import datetime

        # import crud
        # import model
        # import server

        # os.system('dropdb ratings')
        # os.system('createdb ratings')

        # model.connect_to_db(server.app)
        # model.db.create_all()
