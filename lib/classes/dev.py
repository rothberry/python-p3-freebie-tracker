import sqlite3
from ipdb import set_trace

CONN = sqlite3.connect('./freebies.db')
CURSOR = CONN.cursor()

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
    
    @classmethod
    def new_inst_from_db(cls, row):
      return cls(name=row[1], id=row[0])
    
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

