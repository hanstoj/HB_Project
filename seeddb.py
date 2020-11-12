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


# os.system('dropdb ratings')
# os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

for restaurant in range(5)
fake.name()
fake.password


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
