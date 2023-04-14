# from classes.company import Company
# from classes.dev import Dev
import sqlite3
from ipdb import set_trace

CONN = sqlite3.connect('./freebies.db')
CURSOR = CONN.cursor()

class Freebie():

    def __init__(self, item_name, value, dev_id, company_id, id=None):
        self.set_item_name(item_name)
        self.set_value(value)
        self.set_dev_id(dev_id)
        self.set_company_id(company_id)
        self.id = id

    def get_dev_id(self):
        return self._dev_id

    def set_dev_id(self, dev_id):
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
        CONN.commit()

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
    
    @classmethod
    def new_inst_from_db(cls, row):
        #   Freeboe.__init__
        free_inst = cls(item_name=row[1], value=row[2], dev_id=row[3], company_id=row[4])
        free_inst.id = row[4]
    #   return cls(item_name=row[1], value=row[2], dev_id=row[3], company_id=row[4], id=row[0])
    
    @classmethod
    def map_db_to_instances(cls):
        all_free = CURSOR.execute("SELECT * FROM freebies").fetchall()
        return [ cls.new_inst_from_db(row) for row in all_free]

    def __repr__(self):
        return f"""
            id:\t{self.id}
            item_name:\t{self.item_name}
            value:\t{self.value}
            dev_id:\t{self.dev_id}
            company_id:\t{self.company_id}"""

    # ? Optional Useful Methods
    def update(self):
        pass

    def delete(self):
        pass

    # ? Relationship Methods
    def company(self):
        sql = """
            SELECT * FROM companies
            WHERE id = ?
        """
        company = CURSOR.execute(sql, (self.company_id,)).fetchone()
        from classes.company import Company
        # * ACCEPTABLE
        # return company
        return Company.new_inst_from_db(company)

    def dev(self):
        sql = """
            SELECT * FROM devs
            WHERE id = ?
        """
        dev = CURSOR.execute(sql, (self.dev_id,)).fetchone()
        from classes.dev import Dev
        # * ACCEPTABLE
        # return dev
        return Dev.new_inst_from_db(dev)

    def print_details(self):
        # Returns a String formatted like:
        #   {dev name} owns a {freebie item_name} from {company name}
        print(f"{self.dev().name} owns a {self.item_name} from {self.company().name}")
