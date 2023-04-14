#!/usr/bin/env python3

# from sqlalchemy import create_engine

# from models import Company, Dev, Freebie, CONN, CURSOR
from classes.company import Company, CONN, CURSOR
from classes.dev import Dev
from classes.freebie import Freebie
from ipdb import set_trace

if __name__ == '__main__':
    # engine = create_engine('sqlite:///freebies.db')
    all_comp = CURSOR.execute("SELECT * FROM companies").fetchall()
    all_devs = CURSOR.execute("SELECT * FROM devs").fetchall()
    all_free = CURSOR.execute("SELECT * FROM freebies").fetchall()
    
    all_comp_as_insts = Company.map_db_to_instances()
    # ! Python destructuring
    billworld, wallyworld = all_comp_as_insts
    # billworld = all_comp_as_insts[0]

    billworld.freebies()

    all_devs_as_insts = Dev.map_db_to_instances()
    cole, oli = all_devs_as_insts
    
    cole.freebies()

    all_freebies_as_insts = Freebie.map_db_to_instances()
    one = all_freebies_as_insts[0]

    # ! CHAIN REACTION INSTANCES
    # dev_inst = one.dev()
    # list_o_freebies = dev_inst.freebies()
    # comp = list_o_freebies[0].company()

    # TEST AGGREGATE METHODS

    one.print_details()

    # Company.oldest_company()
    billworld.give_freebie(cole, "Mug Warmer", 99)

    set_trace()
