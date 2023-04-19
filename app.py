from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_folder='static') # Create a new Flask object named 'app' and set the static folder to 'static'
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5) # Set the permanent session lifetime to 5 minutes using the timedelta class

@app.route("/")
def home():
  """
  This function handles the request for the home page of the website.
  It returns the rendered HTML template for the index page.
  
  Returns:
      str: Rendered HTML template for the index page.
  """
  return render_template("index.html")

@app.route("/CheckRet")
def CheckRet():
  """
  Renders the CheckRet.html template when the /CheckRet route is accessed.

  Returns:
    The rendered CheckRet.html template.
  """
  return render_template("CheckRet.html")

@app.route("/checkout_tool")
def checkout_tool_page():
  """
  Route function for the return tool page.
  
  Returns:
      rendered HTML template: checkout_tool_page.html
  """
  return render_template("checkout_tool_page.html") 

@app.route("/return_tool")
def return_tool_page():
  """
    Route function for the return tool page.

    Returns:
        HTML template: The return_tool_page.html template to be rendered.
    """
  return render_template("return_tool_page.html")

@app.route('/add_tool_page', methods=["POST", "GET"])
def add_tool_page():
  """
  Renders the add_tool_page template and allows for adding a tool to the database.

  Returns:
    If user is logged in and a POST request was made, it redirects to the user page and displays a success message
    If user is logged in and a GET request was made, it renders the add_tool_page template
    If user is not logged in, it redirects to the user page and displays a message to login
  """
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
  """
  Renders a login page where the user can enter their password.

  Returns:
    If the user is already logged in, a redirect to the user page.
    If the password is submitted and valid, a redirect to the user page.
    If the password is submitted and invalid, a redirect back to the login page with an error message.
    If no password is submitted, the login page is rendered.
  """
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
  """
  Validates password by generating a hash using the generate_password_hash() function
  and checking it against the input password using check_password_hash() function.

  Args: 
    password (str): password input by user.

  Returns:
    bool: True if the input password matches the generated hash, False otherwise.
  """
  hashed_password = generate_password_hash("1107247", method="sha256", salt_length=8)
  return check_password_hash(hashed_password, password)

@app.route("/user")
def user():
  """
  Renders the user.html template if the user is logged in, else redirects to the login page.

  Returns:
    If the user is logged in, renders the user.html template with the user's name passed in as an argument.
    If the user is not logged in, redirects to the login page.
  """
  if "user" in session:
    user = session["user"]
    return render_template("user.html", user = user)
  else:
    flash("You are not logged in!")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
  """
  Logs out the current user and redirects to the login page.

  Returns:
    A redirect response to the login page.
  """
  if "user" in session:
    user = session["user"]
    flash(f"You have been logged out", "info")
  session.pop("user", None)
  return redirect(url_for("login"))

if __name__ == "__main__":
  app.run(debug = True)