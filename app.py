from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home():
  return render_template("index.html")

@app.route("/CheckRet")
def CheckRet():
  return render_template("CheckRet.html")
    
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/login", methods=["POST", "GET"])
def login():
  if request.method == "POST":
    password = request.form["password"]
    if validate_password(password):
      session.permanent = True
      user = request.form["password"]
      session["user"] = user
      flash("House Manager Login Successful!")
      return redirect(url_for("user"))
    else:
      if "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("user"))
      flash("Invalid password!")
      return redirect(url_for("login"))
  else:
    return render_template("login.html")

def validate_password(password):
  # Perform password validation here
  hashed_password = generate_password_hash("1107", method="sha256", salt_length=8)
  return check_password_hash(hashed_password, password)



@app.route("/user")
def user():
  if "user" in session:
    user = session["user"]
    return render_template("user.html", user = user)
  else:
    flash("You are not logged in!")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
  if "user" in session:
    user = session["user"]
    flash(f"You have been logged out, {user}", "info")
  session.pop("user", None)
  return redirect(url_for("login"))


if __name__ == "__main__":
  app.run(debug = True)