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
        # Check if currentid save file exists, creates it if not (and sets first current_id as 0)
        if not exists('currentid.txt'):
            open('currentid.txt', 'x')
            with open('currentid.txt', 'w') as id_file:
                id_file.write('0')
        
        self.con = sql.connect('db.sqlite')
        self.cur = self.con.cursor()
        self.current_date = date.today().strftime('%d/%m/%y') # Maybe deprecated
        self.current_expense_id = 0

        # Check if expense table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='expenses'"):
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE expenses
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    establishment_id INTEGER REFERENCES establishments(id),
                                    account_id INTEGER REFERENCES accounts(id),
                                    expense REAL,
                                    year INTEGER,
                                    month INTEGER,
                                    day INTEGER)''')
        # Check if accounts table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='accounts'"):
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE accounts
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    account VARCHAR(10),
                                    user_id INTEGER REFERENCES users(id),
                                    balance MONEY)''')
        # Check if users table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'"):
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE users
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user VARCHAR(10),
                                    email VARCHAR(20))''')
        # Check if establishments table exists, creates it if not
        for table in self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='establishments'"):
            if table[0] == 0:
                self.cur.execute('''CREATE TABLE establishments
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    establishment VARCHAR(15))''')

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
    
    def create_expense(self, establishment, account, expense, year, month, day):
        if establishment.isnumeric():
            return ValueError('Establishment name cannot be numeric')
        elif len(establishment) > 10:
            return ValueError('Entered establishment name is too long')
        elif not bool(self.cur.execute("SELECT COUNT(*) FROM accounts WHERE account=:account", {'account': account}).fetchone()[0]):
            return NameError('Entered account does not exist in the database')
        elif (len(str(year)) < 4 or year < 2021) or (month > 12 or month < 1) or (day > 31 or day < 0):
            return ValueError('Entered date is invalid')
        else:
            file = open('currentid.txt')
            current_id = int(file.readline())
            current_id += 1
            self.cur.execute('''INSERT INTO expenses
                                VALUES (?,
                                ?,
                                ?,
                                ?,
                                ?,
                                ?,
                                ?)''', (current_id, establishment, account, expense, year, month, day))
            file = open('currentid.txt', 'w')
            file.write(str(current_id))
            return ('Succesfully created expense and wrote to currentid')