from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
    "apiKey": "AIzaSyBRNizx0xwhqyNe3PGf_vhnLkT0tzT31rA",
    "authDomain": "meet-indv-proj.firebaseapp.com",
    "databaseURL": "https://meet-indv-proj-default-rtdb.firebaseio.com",
    "projectId": "meet-indv-proj",
    "storageBucket": "meet-indv-proj.appspot.com",
    "messagingSenderId": "972597907873",
    "appId": "1:972597907873:web:7906fe1defa5125945fbe0",
    "measurementId": "G-JJ6GFM6TNR",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods = ["POST", "GET"])
def signup():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]

        try:
            login_session["user"] = auth.create_user_with_email_and_password(email, password)
            uid = login_session["user"]["localId"]

            user = {"username": username, "email": email, "password": password}
            db.child("Users").child(uid).set(user)
            return redirect(url_for('login'))
        except:
            error = "failed to create an account, may you have one already?"
            return render_template("signup.html", error = error)
    else:
        return render_template("signup.html")


@app.route("/login", methods = ["POST", "GET"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            login_session["logged_user"] = auth.sign_in_with_email_and_password(email, password)
            uid = login_session["logged_user"]["localId"]

            user = db.child("Users").child(uid).get().val()
            login_session["logged_username"] =  username = user["username"]
            return render_template("index.html")
        except:
            error = "email or password incorrect, try again"
            return render_template("login.html", error = error)
    else:
        return render_template("login.html")


@app.route("/index")
def main():
    return render_template("index.html", quotes = db.child("Quotes").get().val())


@app.route("/add_qoute", methods = ["POST", "GET"])
def add_qoute():
    error = ""
    if request.method == "POST":
        text = request.form["qoute"]
        try:
            username = login_session["logged_username"]
            qoute = {"text": text, "author": username}
            db.child("Quotes").push(qoute)
            return render_template("index.html", quotes = db.child("Quotes").get().val())
        except:
            error = "can not upload qoute"
            return render_template("add_qoute.html", error=error)
    else:
        return render_template("add_qoute.html")


if __name__ == '__main__':
    app.run(debug=True)