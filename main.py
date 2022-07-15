from multiprocessing.sharedctypes import Value
import sqlite3 as sql
from datetime import date
from os.path import exists


def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


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
                                    establishment VARCHAR(20),
                                    account VARCHAR(10),
                                    year INTEGER,
                                    month INTEGER,
                                    day INTEGER)''')
        # Check if accounts table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='accounts'"):
            print(table) # debug print
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE accounts
                                    (account VARCHAR(10) PRIMARY KEY,
                                    user VARCHAR(10),
                                    balance MONEY)''')
        # Check if users table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'"):
            print(table) # debug print
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE users
                                    (user VARCHAR(10) PRIMARY KEY,
                                    email VARCHAR(20))''')

    def create_user(self, user, email):
        if user.isnumeric() or email.isnumeric():
            return ValueError('User name/Email cannot be numeric')
        elif ('@' not in email):
            return ValueError('Entered invalid email')
        elif len(user) > 10 or len(email) > 20:
            return ValueError('User/email entered is too long (max of 10 char for user and 30 char for email')
        elif bool(self.cur.execute("SELECT COUNT(*) FROM users WHERE user=:user", {'user': user}).fetchone()[0]):
            return NameError('User already exists in database')
        self.cur.execute('''INSERT INTO users
                            VALUES (?,
                            ?)''', (user, email))
        return 'Successfully created user'
    
    def create_account(self, account_name, user, initial_balance):
        # Check if user exists
        if not bool(self.cur.execute("SELECT COUNT(*) FROM users WHERE user=:user", {'user': user}).fetchone()[0]):
            return NameError('Entered user does not exist in the database')
        elif account_name.isnumeric():
            return ValueError('Account name cannot be numeric')
        elif len(account_name) > 10:
            return ValueError('Entered account name is too long')
        elif not isfloat(initial_balance):
            return ValueError('Entered initial balance is not valid (only accepts integers or floats)')
        elif bool(self.cur.execute("SELECT COUNT(*) FROM accounts WHERE account=:account", {'account': account_name}).fetchone()[0]):
            return NameError('Account already exists in database')
        else:
            self.cur.execute('''INSERT INTO accounts
                                VALUES (?,
                                ?,
                                ?)''', (account_name, user, initial_balance))
            return 'Successfully created account'


# Testing ground (while I don't get a handle on pytest)
manager = db_manager()
print(manager.create_user('David', 'myemail@email.com'))
print(manager.create_account('Bank', 'David', 50))

for row in manager.cur.execute('SELECT * FROM users'):
    print(row)

for row in manager.cur.execute('SELECT * FROM accounts'):
    print(row)