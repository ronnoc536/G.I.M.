from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector



app = Flask(__name__, static_folder='static') # Create a new Flask object named 'app' and set the static folder to 'static'
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5) # Set the permanent session lifetime to 5 minutes using the timedelta class

# bad security who cares
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="110724742069",
  database="TKE_Garage"
)

@app.errorhandler(404)
def page_not_found(e):
  """
  Render a custom 404 error page when the requested resource is not found.

  :param e: The error that occurred.
  :return: A rendered HTML template for the custom 404 error page.
  """
  return render_template('404.html'), 404


@app.route("/")
def home():
  """
  This function handles the request for the home page of the website.
  It returns the rendered HTML template for the index page.
  
  Returns:
    Rendered HTML template for the index page.
  """
  return render_template("index.html")


@app.route("/help")
def need_help():
  return render_template("help.html")


@app.route("/CheckRet")
def CheckRet():
  """
  Renders the CheckRet.html template when the /CheckRet route is accessed.

  Returns:
    The rendered CheckRet.html template.
  """
  return render_template("CheckRet.html")


@app.route("/checkout_tool", methods=["GET", "POST"])
def checkout_tool_page():
  """
  Route function for the return tool page.
  
  Returns:
      rendered HTML template: checkout_tool_page.html
  """
  cursor = mydb.cursor()
  cursor.execute("SELECT * FROM Tools WHERE last_taken <= last_returned")
  tools = cursor.fetchall()
  mydb.commit()
  if request.method == "POST":
    data = request.form
    tool_id = data["serial_num"]
    scroll_id = data["scroll_num"]
    cursor.execute(f"UPDATE Tools SET last_user = {scroll_id}, last_taken = CURRENT_DATE() WHERE id = {tool_id}")
    mydb.commit()
    flash("Tool checked out!")
    return redirect(url_for("CheckRet"))
  return render_template("checkout_tool_page.html", tools = tools) 



@app.route("/return_tool", methods=["GET", "POST"])
def return_tool_page():
    """
    Route function for the return tool page.

    Returns:
        HTML template: The return_tool_page.html template to be rendered.
    """
    if request.method == "GET":
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM Tools WHERE last_taken > last_returned")
        tools = cursor.fetchall()
        mydb.commit()
        return render_template("return_tool_page.html", tools=tools)

    if request.method == "POST":
        data = request.form
        tool_id = data["serial_num"]
        scroll_id = data["scroll_num"]
        cursor = mydb.cursor()
        cursor.execute(f"UPDATE Tools SET last_user = {scroll_id}, last_returned = CURRENT_DATE() WHERE id = {tool_id}")
        mydb.commit()
        flash("Tool returned!")
        return redirect(url_for("CheckRet"))


@app.route("/remove_tool_page", methods=["GET", "POST"])
def remove_tool():
  if "user" in session:
    # Retrieve all tools from the database
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Tools")
    tools = cursor.fetchall()
    if request.method == "POST":
      data = request.form
      tool_id = data["serial_num"]
      cursor.execute(f"DELETE FROM Tools WHERE id = {tool_id}")
      mydb.commit()
      flash("Tool removed successfully!")
      return redirect(url_for("user"))
    return render_template("remove_tool_page.html", tools=tools)
  else:
    return redirect(url_for("user"))


@app.route("/edit_tool_page", methods=["GET", "POST"])
def edit_tool():
  if "user" in session:
    # Retrieve all tools from the database
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Tools")
    tools = cursor.fetchall()
    if request.method == "POST":
      tool_id = request.form["serial_num"]
      # Fetch the specific tool from the database using its ID
      cursor.execute("SELECT * FROM Tools WHERE id= %s", (tool_id,))
      tool = cursor.fetchall()
      return redirect(url_for("edit_tool_2", tool=tool))
    return render_template("edit_tool_page.html", tools=tools)
  else: 
    return redirect(url_for("user"))


@app.route("/2_edit_tool_page", methods=["GET"])
def edit_tool_get():
  print("Loaded page")
  tool_string = request.args.get("tool")
  if tool_string and "user" in session:
      tool_list = list(str(tool_string[1:-1]).split(", "))
      tool_list[0] = int(tool_list[0])
      del tool_list[2]
      del tool_list[3]
      return render_template("2_edit_tool_page.html", tool=tool_list)
  else:
    return redirect(url_for("edit_tool"))


  
@app.route("/2_edit_tool_page", methods=["POST"])
def edit_tool_2():
    #if form on this page was submited
    print("edit tool submitted")
    try:
      data = request.form
      cursor = mydb.cursor()
      sql = f"UPDATE Tools SET name = \"{data['tool_name']}\", location = \"{data['tool_location']}\", quality = \"{data['tool_cond']}\" WHERE ID = {data['tool_id']}"
      cursor.execute(sql)
      mydb.commit()
      flash("Tool edited successfully!")
      return redirect(url_for("user"))
    except:
      return redirect(url_for("edit_tool"))


@app.route("/view_tools_page")
def view_tools():
  if "user" in session:
    # Retrieve all tools from the database
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Tools")
    tools = cursor.fetchall()
    return render_template("view_tools_page.html", tools=tools)
  else: 
    return redirect(url_for("user")) #send to user func where they will be told they are not logged in

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
      data = request.form #gathers the data from the form into a container to be indexed.
      cursor = mydb.cursor()
      sql = f"INSERT INTO Tools (name, last_user, location, last_returned, quality, last_taken) \
                VALUES (\"{data['tool_name']}\", NULL, \"{data['tool_location']}\", CURRENT_DATE(), \"{data['tool_cond']}\", \"1936-11-12\")"
      cursor.execute(sql) # executes the sql
      mydb.commit() # sends the request i guess?
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
  hashed_password = generate_password_hash("1107", method="sha256", salt_length=8)
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
  cursor = mydb.cursor() # just a test
  cursor.execute("SELECT * FROM Tools WHERE id = 69") # just a test
  print(cursor.fetchall()) # just a test
  app.run(debug = True)
