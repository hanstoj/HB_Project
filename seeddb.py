import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server
# from faker import faker
# os.system('dropdb ratings')
# os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()


fake_data = Faker()
