import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, first_name,last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    

    def insert(self, cursor):
        cursor.execute('''
          INSERT INTO users 
          ( first_name
          , last_name
          , email
          , password_hash
          )
          VALUES 
          ( ?, ?, ?, ?)
        ''', (self.first_name,self.last_name, self.email, self.password_hash)
        )
        
    def __repr__(self):
        return "[User %s.%s<%s>]"%(self.first_name,self.last_name, self.email)
        
    @classmethod
    def create_table(cls, cursor):
        cursor.execute('DROP TABLE IF EXISTS users')

        cursor.execute('''
        CREATE TABLE users      
        ( first_name TEXT NOT NULL
        , last_name TEXT NOT NULL
        , password_hash TEXT NOT NULL
        , email TEXT NOT NULL PRIMARY KEY
        )''')

class UserForLogin(flask_login.UserMixin):
    def __init__(self, row):
        self.email = row['email']
        self.password_hash = row['password_hash']
        self.first_name = row['first_name']
        self.last_name = row['last_name']
        self.rowid = row['rowid']
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.email
      
    @classmethod
    def getByEmail(cls, cursor, email):
        cursor.execute('''
            SELECT rowid, email, password_hash, first_name, last_name
            FROM users
            WHERE email = ?
        ''', (email,))

        row = cursor.fetchone()
        if row is None:
            return None
        
        return cls(row)
    
    @classmethod
    def getAll(cls, cursor):
      cursor.execute('SELECT rowid, first_name, last_name, email, password_hash FROM users')
      return [ cls(row) for row in cursor.fetchall() ]

class ConnectedUser:
    def __init__(self, rowid, first_name, last_name, socket_id):
        self.rowid = rowid
        self.first_name = first_name
        self.last_name = last_name
        self.socket_id = socket_id
        self.status = 'AVAILABLE'


  