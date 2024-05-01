""" Seed file to create/delete and add test data to our Wabbit DB """

import os, model, server, json
from pdb import set_trace

server.app.app_context().push()

os.system("dropdb wabbit")              ## drop table and all data
os.system("createdb wabbit")            ## recreate table

model.connect_to_db(server.app)         ## connect to Wabbit DB
model.db.create_all()                   ## create all tables

with open ('data/test_data.json') as file:
    test_data = json.loads(file.read())


print("🚨 Database has been seeded 🚨")