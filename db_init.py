import sqlite3

from models.user import User
from models.colonne import Colonne


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

  
db = sqlite3.connect('.data/db.sqlite')
db.row_factory = make_dicts

cur = db.cursor()
cur2 = db.cursor()


User.create_table(cur)
Colonne.create_table(cur)

users = [
    User("Ford","zda", "ford@betelgeuse.star", "12345"),
    User("Arthur","firero", "arthur@earth.planet", "12345"),
    User("ismail","Aissami", "a@a.a", "12345")
]

colonnes=[
    Colonne("colonne1","1"),
    Colonne("colonne2","2")
]

for user in users:
    user.insert(cur)

for colonne in colonnes:
  colonne.insert(cur)    

db.commit()

print("The following users has been inserted into the DB"
      " (all the passwords are 12345):")

for user in users:
    # uses the magic __repr__ method
    print("\t", user)
    
print("The following columns has been inserted into the DB")

for colonne in colonnes:
    # uses the magic __repr__ method
    print("\t", colonne)
print()
