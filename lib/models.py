
# ! Class.class_method
# ! Class#instance_method

# Relationships:
#   Company has_many Freebies
#   Company has_many Devs through Freebies

#   Dev has_many Freebies
#   Dev has_many Companies through Freebies

#   Freebie belongs_to Company
#   Freebie belongs_to Dev

# Therefore there is a Many to Many Relationship
#   between the Company and Dev

import sqlite3
from ipdb import set_trace

CONN = sqlite3.connect('./freebies.db')
CURSOR = CONN.cursor()


class Company():

    def __init__(self, name, founding_year, id=None):
        # self._name = name
        # self.name = name
        self.set_name(name)
        # self._founding_year = founding_year
        self.founding_year = founding_year
        self.id = id

    # How to create the setters/getters with a propery of `name`?
    def get_name(self):
        # return f"name =>\t{self._name}"
        return self._name

    def set_name(self, new_name):
        # Check if new_name is a str AND is greater than 0 chars
        if type(new_name) == str and len(new_name) > 0:
            self._name = new_name
        else:
            print("Wasn't a str or not enough chars")
            raise Exception()

    name = property(get_name, set_name)

    @property
    def founding_year(self):
        # return f"Year is=> {self._founding_year}"
        return self._founding_year

    # method called self.founding_year=(args)
    @founding_year.setter
    def founding_year(self, new_year):
        # New_year needs to be what...
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
        sql = """ 
            DROP TABLE IF EXISTS companies
        """
        CURSOR.execute(sql)

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

    # Print_details_for_a_human_to_read(self)
    def __repr__(self):
        return f"""
            id:\t\t {self.id} 
            Name:\t {self.name}
            Year:\t {self.founding_year}
        """
    """"""
    # ? Optional Useful Methods
    def update(self):
        pass

    def delete(self):
        pass

    # ? Relationship Methods
    def freebies(self):
        # Returns all the FREEBIE Instances associated with THIS Company
        pass

    def devs(self):
        # Returns all the DEV Instances associated with THIS Company
        pass

    # ? Aggregate Methods
    def give_freebie(self, dev, item_name, value):
        pass

    @classmethod
    def oldest_company(cls):
        # Returns the COMPANY Instance of the oldest company
        # ! Should not use any python searching, it will all be done in SQL
        pass

# ! ================================


class Dev():

    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if type(new_name) == str and len(new_name) > 0:
            self._name = new_name
        else:
            raise Exception("Bad Name for dev")

    # ? ORM Table Methods
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS devs (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS devs")

    def save(self):
        sql = """
            INSERT INTO devs (name) VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        self.id = CURSOR.lastrowid
        CONN.commit()
        # Commit is needed when you INSERT/UPDATE/DELETE from the db

    @classmethod
    def create(cls, name, id=None):
        new_dev = Dev(name)
        new_dev.save()
        return new_dev
    
    def __repr__(self):
        return f"""
            id:\t\t{self.id}
            Name:\t{self.name}"""

    # ? Optional Useful Methods
    def update(self):
        pass

    def delete(self):
        pass

    # ? Relationship Methods
    def companies(self):
        pass

    def freebies(self):
        pass

    # ? Aggregate Methods
    def recieved_one(self, item_name):
        # Returns a BOOLEAN of whether or not THIS Dev has recieved
        pass

    def give_away(self, other_dev, freebie):
        # Gives this Freebie instance to other_dev
        #
        pass

# ! ================================


class Freebie():

    # initializes with a: item_name, value, both belongs_to associations, id of None on init
    def __init__(self, item_name, value, dev_id, company_id, id=None):
        self.set_item_name(item_name)
        self.set_value(value)
        self.set_dev_id(dev_id)
        self.set_company_id(company_id)
        self.id = id

    def get_dev_id(self):
        return self._dev_id

    def set_dev_id(self, dev_id):
        # What are the Validations for the dev_id
        #   Has to be an int 
        #   the dev_id has to be an ID on the Devs table
        # Find all the ids on the Devs table
        # check if this dev_id is in that list (will NOT be a range)
        all_devs = CURSOR.execute("SELECT id from devs").fetchall()
        all_ids = [row[0] for row in all_devs]
        if dev_id in all_ids:
            self._dev_id = dev_id
        else:
            raise Exception("BAD DEV ID")

    def get_company_id(self):
        return self._company_id

    def set_company_id(self, company_id):
        all_companies = CURSOR.execute("SELECT id from companies").fetchall()
        all_ids = [row[0] for row in all_companies]
        if company_id in all_ids:
            self._company_id = company_id
        else:
            raise Exception("BAD COMPANY ID")

    def get_item_name(self):
        return self._item_name
    
    def set_item_name(self, new_item_name):
        if type(new_item_name) == str and len(new_item_name) > 0:
            self._item_name = new_item_name
        else:
            raise Exception("Bad Item Name...")

    def get_value(self):
        return self._value
    
    def set_value(self, new_value):
        if type(new_value) == int and new_value >= 0:
            self._value = new_value
        else:
            raise Exception("Bad Val Bro...")
        
    # ! ALL THE FREEBIE PROPERTIES
    item_name = property(get_item_name, set_item_name)
    value = property(get_value, set_value)
    dev_id = property(get_dev_id, set_dev_id)
    company_id = property(get_company_id, set_company_id)


    # ? ORM Table Methods
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS freebies (
                id INTEGER PRIMARY KEY,
                item_name TEXT,
                value INTEGER,
                dev_id INTEGER,
                company_id INTEGER
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS freebies")

    def save(self):
        sql = """
            INSERT INTO freebies (item_name, value, dev_id, company_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.item_name, self.value, self.dev_id, self.company_id))
        self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, item_name, value, dev_id, company_id):
        new_freebie = cls(item_name, value, dev_id, company_id)
        new_freebie.save()
        return new_freebie
    
    def __repr__(self):
        return f"""
            id:\t{self.id}
            item_name:\t{self.item_name}
            value:\t{self.value}
            dev_id:\t{self.dev_id}
            company_id:\t{self.company_id}
        """

    # ? Optional Useful Methods
    def update(self):
        pass

    def delete(self):
        pass

    # ? Relationship Methods
    def company(self):
        pass

    def dev(self):
        pass

    def print_details(self):
        # Returns a String formatted like:
        #   {dev name} owns a {freebie item_name} from {company name}
        pass
