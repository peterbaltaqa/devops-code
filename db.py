import sqlite3
from usr import Usr
from os.path import isfile
from datetime import datetime

name = "data.db"

def isdate(date):
    try:
        datetime.fromisoformat(date)
    except:
        return False
    
    return True

def create():

    # Return early if database is already set up
    if isfile(name):
        return
    
    accounts = [Usr("admin", "admin", True).data,
                Usr("John Smith", "123456").data,
                Usr("Jane Doe", "qwerty").data,
                Usr("Mary", "111111").data,
                Usr("Sam Jones", "dragon").data,
                Usr("Jeremy Fox", "123123").data,
                Usr("Terry Jobs", "baseball").data,
                Usr("Muhammad Li", "abc123").data,
                Usr("JM", "football").data,
                Usr("Jerry Allen", "monkey").data,
                Usr("Sarah McGill", "letmein").data,]

    # Create database files
    con = sqlite3.connect(name)
    cur = con.cursor()

    # Create table for accounts and load them
    cur.execute("CREATE TABLE usrs (usr PRIMARY KEY, pw NOT NULL, isadmin NOT NULL)")
    cur.executemany("INSERT INTO usrs VALUES (?, ?, ?)", accounts)
    con.commit()

    # Create table to store tickets
    cur.execute("CREATE TABLE tickets (ticketno INT PRIMARY KEY, usr, subject, status, priority, dt, FOREIGN KEY (usr) REFERENCES usrs(usr))")
    con.commit()

    # Add placeholder data 
    tickets = [ (1,  "John Smith",   "Computer not working",       "Pending",   "Low",  "2024-09-15 12:22:00"),
                (2,  "Jane Doe",     "cannot send any e-mails",    "Assigned",  "Low",  "2024-09-16 14:00:00"),
                (3,  "Mary",         "PC encrypted by ransomware", "Assigned",  "High", "2024-09-13 16:55:00"),
                (4,  "Sam Jones",    "Lost my keyboard",           "Resolved",  "Low",  "2012-12-21 12:00:00"),
                (5,  "Jeremy Fox",   "Computer Slowness",          "Resolved",  "Low",  "2024-09-09 09:09:00"),
                (6,  "Terry Jobs",   "Require new laptop",         "Pending",   "Low",  "2024-09-15 13:30:00"),
                (7,  "Muhammad Li",  "Servers are down",           "Pending",   "High", "2024-10-01 13:37:00"),
                (8,  "JM",         "New Starter Onboarding",     "Assigned",  "Low",  "2024-09-10 21:00:00"),
                (9,  "Jerry Allen",  "monitor is cracked!",        "Resolved",  "Low",  "2024-09-13 17:38:00"),
                (10, "Sarah McGill", "Blue-screen when booting",   "Resolved",  "High", "2024-07-19 04:10:00")]
    
    cur.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)", tickets)
    con.commit()

    con.close()

def table():

    if not isfile(name):
        create()

    con = sqlite3.connect(name)
    cur = con.cursor()   

    res = cur.execute("SELECT * FROM tickets").fetchall()
    con.close()

    return res

def usrs():

    con = sqlite3.connect(name)
    cur = con.cursor()   

    res = cur.execute("SELECT usr FROM usrs").fetchall()

    con.close()

    return res

def update(request):
    con = sqlite3.connect(name)
    cur = con.cursor()   

    request = request.form.to_dict()
    request.pop("save")

    columns = ["ticketno", "usr", "subject", "status", "priority", "dt"]

    if request.get("new 0") is not None:
        ticketno = request.get("new 0") 

    # Get current ticket numbers
    seentickets = [];

    for i in request:
        field = i.split()
        if field[1] != 'del' and columns[int(field[1])] == "ticketno":
            seentickets.append(request[i])

    # Validation
    for i in request:
        field = i.split()

        if (field[1] == "del"):
            cur.execute("DELETE FROM tickets WHERE ticketno = ?", (field[0],))
            con.commit()
            continue

        # Ticket number must be integer
        print(field[1])
        if not request[i].isnumeric() and columns[int(field[1])] == "ticketno":
            con.close()
            return "Integer"
        
        # Must be valid date format
        if not isdate(request[i]) and columns[int(field[1])] == "dt":
            con.close()
            return "Datetime"
        
        # Convert to standard format if date is updated
        if columns[int(field[1])] == "dt":
            request[i] = datetime.fromisoformat(request[i])

        # Status must be from selection
        if columns[int(field[1])] == "status" and not (request[i] ==  "Pending" or request[i] == "Assigned" or request[i] == "Resolved"):
            con.close()
            return "Status"
        
         # Priority must be from selection
        if columns[int(field[1])] == "priority" and not (request[i] ==  "High" or request[i] == "Low"):
            con.close()
            return "Priority"       


        res = cur.execute("SELECT * FROM tickets WHERE ticketno = ?", (request[i],)).fetchall()


        if (columns[int(field[1])] == "ticketno" and field[0] == "new"):

            # Ticket number must be unique
            if len(res) > 0: 
                con.close()
                return "Unique"
            
            cur.execute("INSERT INTO tickets (ticketno) VALUES (?)", (ticketno,))

        else:
            if len(seentickets) != len(set(seentickets)):
                con.close()
                return "Unique"

            if request.get("new 0") is None:
                cur.execute("UPDATE tickets SET ? = ? WHERE ticketno = ?", columns[int(field[1])], request[i], field[0])
            else:
                cur.execute("UPDATE tickets SET ? = ? WHERE ticketno = ?", columns[int(field[1])], request[i], ticketno)

    con.commit()
    con.close()

def chk_usr(usr):
    con = sqlite3.connect(name)
    cur = con.cursor()

    res = cur.execute(f"SELECT usr FROM usrs WHERE usr = ?", (usr,)).fetchall()

    con.close()
    return not res

def add_usr(usr, pw):
    con = sqlite3.connect(name)
    cur = con.cursor()
    
    NewUser = Usr(usr, pw)

    cur.execute(f"INSERT INTO usrs VALUES (?, ?, ?)", NewUser.usrname, NewUser.pw, False)

    con.commit()
    con.close()
