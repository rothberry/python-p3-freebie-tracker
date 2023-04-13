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
    
    all_comp_as_insts = [ Company.new_inst_from_db(row) for row in all_comp]
    all_devs_as_insts = [ Dev.new_inst_from_db(row) for row in all_devs]
    all_free_as_insts = [ Freebie.new_inst_from_db(row) for row in all_free]

    
    set_trace()
