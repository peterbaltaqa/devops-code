from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import auth
from db import table, update, usrs, chk_usr , add_usr


app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# Index Page
@app.route("/")
def index(): 
    if 'usr' in session:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))

# Home Page
@app.route("/home", methods=["GET", "POST"])
def home():
    if "usr" in session:
        if request.method == 'GET':
            return render_template("home.html", table = table(), usr = session.get('usr'), usrs = usrs())
        
        elif request.form.get("edit") is not None:
            return render_template("home.html", table = table(), mode = "edit", usr = session.get('usr'), usrs = usrs())
        
        elif request.form.get("save") is not None:
            error = update(request)
            return render_template("home.html", table = table(), mode = "save", usr = session.get('usr'), usrs = usrs(), error = error)
        
        elif request.form.get("add") is not None:
            return render_template("home.html", table = table(), mode = "add", usr = session.get('usr'), usrs = usrs())
        
        elif request.form.get("exit") is not None:
            return render_template("home.html", table = table(), usr = session.get('usr'), usrs = usrs())

        elif request.form.get("delete") is not None:
            return render_template("home.html", table = table(), mode = "delete", usr = session.get('usr'), usrs = usrs())

    else:
        return redirect(url_for('login'))


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.pop('usr', None)

    if request.method == 'GET':
        return render_template("login.html")
    
    elif request.form.get("login") is not None:
        usr = request.form["usr"]
        pw = request.form["pw"]

        if not auth(usr, pw):
            return render_template("login.html", fail = "auth")
        else:
            session['usr'] = usr
            return redirect(url_for('home'))

    elif request.form.get("register") is not None:
        return render_template("login.html", register = True)

    elif request.form.get("back") is not None:
        return render_template("login.html")

    elif request.form.get("confirm") is not None:
        usr = request.form["usr"]
        pw = request.form["pw"]
        confirm = request.form["pw2"]

        if (pw != confirm):
            return render_template("login.html", fail = "confirm")
        
        elif (not chk_usr(usr)):
            return render_template("login.html", fail = "taken")
        
        else:
            add_usr(usr, pw)
            return render_template("login.html", registered = True)


    