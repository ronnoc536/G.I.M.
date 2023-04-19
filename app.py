from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/CheckRet")
def CheckRet():
  return render_template("CheckRet.html")

@app.route('/add_tool_page', methods=["POST", "GET"])
def add_tool_page():
  if "user" in session:
    if request.method == "POST":#if they clicked submit on add tools for example
                                # also where i think that the adding tool to db would go but idk
      flash("Tool added successfully!") #lets user know that it got added
      return redirect(url_for("user")) # takes them back to where the options are
    return render_template("add_tool_page.html") # dont remember
  else: 
    return redirect(url_for("user")) #send to user func where they will be told they are not logged in
    
@app.route("/login", methods=["POST", "GET"])
def login():
  if "user" in session: #before anything, check if in login session
    flash("Already Logged In!") # let them know they are still logged in 
    return redirect(url_for("user")) # take them to the user page
  if request.method == "POST": #if password is submitted
    password = request.form["password"] #assign var to the form data
    if validate_password(password): #validate the password
      session.permanent = True  #This and the next 2 lines is to do with the session
      user = request.form["password"]
      session["user"] = user
      flash("House Manager Login Successful!") #let them know they got logged in
      return redirect(url_for("user")) #send them to the user page
    else:
      flash("Invalid password!")
      return redirect(url_for("login"))
  else:
    return render_template("login.html")

def validate_password(password):
  # Perform password validation here
  hashed_password = generate_password_hash("1107247", method="sha256", salt_length=8)
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
    flash(f"You have been logged out", "info")
  session.pop("user", None)
  return redirect(url_for("login"))

if __name__ == "__main__":
  app.run(debug = True)