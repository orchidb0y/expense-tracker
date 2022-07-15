import sqlite3 as sql
from datetime import date
from os.path import exists

# This class will handle input and output to the expense database

class db_manager:
    def __init__(self):
        # Checks if the database exists, creates it if not
        if not exists('db.sqlite'):
            open('db.sqlite', 'x')
        
        self.con = sql.connect('db.sqlite')
        self.cur = self.con.cursor()
        self.current_date = date.today().strftime('%d/%m/%y')

        # Checks if expense table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='expenses'", {'date': self.current_date}):
            print(table) # debug print
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE expenses
                                    (id INTEGER PRIMARY KEY,
                                    establishment TEXT,
                                    category TEXT,
                                    year INTEGER,
                                    month INTEGER,
                                    day INTEGER)''')

expense_database = db_manager()