import sqlite3 as sql
from datetime import date
from os.path import exists


# This class will handle input and output to and from the expense database
class db_manager:


    def __init__(self):
        # Check if the database exists, creates it if not
        if not exists('db.sqlite'):
            open('db.sqlite', 'x')
        
        self.con = sql.connect('db.sqlite')
        self.cur = self.con.cursor()
        self.current_date = date.today().strftime('%d/%m/%y') # Maybe deprecated
        self.current_expense_id = 0

        # Check if expense table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='expenses'"):
            print(table) # debug print
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE expenses
                                    (id INTEGER PRIMARY KEY,
                                    establishment VARCHAR(50),
                                    account VARCHAR(20),
                                    year INTEGER,
                                    month INTEGER,
                                    day INTEGER)''')
        
        # Check if accounts table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='accounts'"):
            print(table) # debug print
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE accounts
                                    (account VARCHAR(20) PRIMARY KEY,
                                    user VARCHAR(20),
                                    balance MONEY)''')
        
        # Check if users table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'"):
            print(table) # debug print
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE users
                                    (user VARCHAR(20) PRIMARY KEY,
                                    email VARCHAR(30))''')

    def create_user(self, user, email):
        self.cur.execute('''INSERT INTO users
                            VALUES (?,
                            ?)''', (user, email))
        return 'Successfully created user'
    
    def create_account(self, account_name, user, initial_balance):
        # Check if user exists
        if not bool(self.cur.execute("SELECT COUNT(*) FROM users WHERE user=:user", {'user': user}).fetchone()[0]):
            return NameError('This user does not exist in the database.')
        # In the future, add checks to see if the arguments account_name, user and initial balance are appropriate
        else:
            self.cur.execute('''INSERT INTO accounts
                                VALUES (?,
                                ?,
                                ?)''', (account_name, user, initial_balance))
            return 'Successfully created account'


# Testing ground (while I don't get a handle on pytest)
manager = db_manager()
manager.create_user('David', 'myemail@email.com')
print(manager.create_account('Mybank', 'David', 50))

for row in manager.cur.execute('SELECT * FROM users'):
    print(row)

for row in manager.cur.execute('SELECT * FROM accounts'):
    print(row)