#!/usr/bin/env python3
from models import Company, Dev, Freebie
from ipdb import set_trace

# # ASSUMPTION, DB RESETS TO id=1 autoincrement
# Script goes here!
print("Seeding DB 🌱...")

# ? Start By Dropping all the tables
print("Dropping Tables...")
Company.drop_table()
Dev.drop_table()
Freebie.drop_table()

# ? Then recreate the tables
print("Creating Tables...")
Company.create_table()
Dev.create_table()
Freebie.create_table()

# ORDER DOES MATTER
# ? Create some Test Companies
print("Creating Companies...")
c1 = Company.create("billworld", 1090)
c2 = Company.create("wallyyworld", 1809)

# ? Create some Test Devs
print("Creating Devs...")
d1 = Dev.create("Colc")
d2 = Dev.create("Oli")

# Because the Freebies are the child of Dev/Company, we will need the ids from the Company/Devs to create
# ? Create some Test Freebies
print("Creating Freebies...")
# We don't want to hardcode our relationships because....
#   
# # Freebie.create("", 10, 1, 2)
# set_trace()
Freebie.create("A cool pen", 10, d1.id, c1.id )
Freebie.create("Not a cool pen", 1, d1.id, c2.id )
Freebie.create("Headphones", 999, d2.id, c1.id )

print("DONE!")
