from flask import Flask, render_template, request, redirect, flash, session

#import the connector function
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "full_friends secret key"
#connect and store the connection in "mysql"; note that we pass the database name to the function
mysql = MySQLConnector(app, 'fullfriends')

#a sample query to test the db connection
#print mysql.query_db("SELECT * FROM friends")

@app.route('/', methods=['GET','POST'])
def index():
    call = "SELECT CONCAT(first_name, +' ',+ last_name) AS 'name', age, DATE_FORMAT(created_at, '%M %D' ) AS 'since', YEAR(created_at) AS 'year' FROM friends"
    myFriends = mysql.query_db(call)
    return render_template('index.html', myFriends=myFriends)


@app.route("/addfriend", methods=["POST"])
def addfriend():
    fname = request.form['firstname']
    lname = request.form['lastname']
    age = request.form['age']
    query = "INSERT INTO friends (first_name, last_name, age, created_at, updated_at) VALUES (:firstname, :lastname, :age, NOW(), NOW() )"
    data = {
        "firstname" : fname,
        "lastname" : lname,
        "age" : age
    }
    mysql.query_db(query, data)
    flash("Successfully Added")
    return redirect('/')

app.run(debug=True)