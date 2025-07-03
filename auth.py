import sqlite3
import db
from hash import hash


# Authenticate User
def auth(usr, pw):
    db.create()

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    print(usr)
    res = cur.execute(" SELECT pw FROM usrs WHERE usrs.usr = ? ", (usr,)).fetchone()

    if res is not None and hash(pw) == res[0]:
        return True
    else:
        return False

