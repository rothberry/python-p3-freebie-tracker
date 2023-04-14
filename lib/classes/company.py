import sqlite3
from ipdb import set_trace
from classes.freebie import Freebie
# from dev import Dev

CONN = sqlite3.connect('./freebies.db')
CURSOR = CONN.cursor()

class Company():

    def __init__(self, name, founding_year, id=None):
        self.name = name
        self.founding_year = founding_year
        self.id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if type(new_name) == str and len(new_name) > 0:
            self._name = new_name
        else:
            print("Wasn't a str or not enough chars")
            raise Exception()
    @property
    def founding_year(self):
        return self._founding_year

    @founding_year.setter
    def founding_year(self, new_year):
        if type(new_year) == int and new_year > 0:
            self._founding_year = new_year
        else:
            raise Exception("Incorrect Year")

    # ? ORM Table Methods
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY,
                name TEXT,
                founding_year INTEGER
            )
        """
        CURSOR.execute(sql)
        
    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS companies")

    def save(self):
        sql = """
            INSERT INTO companies (name,  founding_year)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.founding_year))
        CONN.commit()
        self.id = CURSOR.lastrowid
        print(f'Created with id: {self.id}')

    @classmethod
    def create(cls, name, founding_year, id=None):
        new_company = cls(name, founding_year, id)
        new_company.save()
        return new_company
    
    @classmethod
    def new_inst_from_db(cls, row):
      return cls(name=row[1], founding_year=row[2], id=row[0])
      
    @classmethod
    def map_db_to_instances(cls):
        all_comp = CURSOR.execute("SELECT * FROM companies").fetchall()
        return [ cls.new_inst_from_db(row) for row in all_comp]

    
    # Print_details_for_a_human_to_read(self)
    def __repr__(self):
        return f"""
            id:\t\t {self.id} 
            Name:\t {self.name}
            Year:\t {self.founding_year}"""

    # ? Optional Useful Methods
    def update(self):
        pass

    def delete(self):
        pass

    # ? Relationship Methods
    def freebies(self):
        # Returns all the FREEBIE Instances associated with THIS Company
        sql = """
            SELECT * FROM freebies
            WHERE company_id = ?
        """
        freebie_rows = CURSOR.execute(sql, (self.id,)).fetchall()
        # * ACCEPTABLE RETURN OF THE LIST OF FREEBIE TUPLES
        # return freebie_rows
        # OR
        return  [ Freebie.new_inst_from_db(row) for row in freebie_rows ]

    def devs(self):
        # Returns all the DEV Instances associated with THIS Company
        pass

    # ? Aggregate Methods
    def give_freebie(self, dev_inst, item_name, value):
        # dev_inst is an INSTANCE of Dev, not the tuple
        return Freebie.create(item_name, value, dev_inst.id, self.id)

    @classmethod
    def oldest_company(cls):
        # Returns the COMPANY Instance of the oldest company
        # ! Should not use any python searching, it will all be done in SQL
        sql = """
            SELECT * FROM companies 
            ORDER by founding_year LIMIT 1
        """
        old = CURSOR.execute(sql).fetchone()
        return cls.new_inst_from_db(old)
        # return Company.new_inst_from_db(old)
