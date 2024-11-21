"""
This code is modified from lab 08

"""


from flask import *
import mysql.connector
import json
import sys
import insert_data_multiple_tables

app = Flask(__name__)

credentials = json.load(open("credentials.json", "r"))

#gets data from mariaDB on pi and returns a json with all the data
@app.route('/getCaptureData', methods=['GET'])
def database_captures():
    capture_session = request.args.get('capture_session')

    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )
    cursor = database.cursor()
    
    cursor.execute(f"SELECT * FROM data_capture WHERE capture_id = '{capture_session}';")
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return json.dumps(data)

#gets data from mariaDB on pi and returns a json with all the data
@app.route('/getSessionsData', methods=['GET'])
def database_sessions():
    #this is a helper module I wrote that gets the new csv data on refresh.
    print(insert_data_multiple_tables.update())
    
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )
    cursor = database.cursor()
    
    cursor.execute("SELECT * FROM capture_sessions;")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    database.close()
    return json.dumps(data)




# redirect default page to frisberry page (home)
@app.route('/', methods=['GET'])
def default():
    return redirect(url_for('frisberry'))

# display home (frisberry.html)
@app.route('/frisberry', methods=['GET'])
def frisberry():
    return render_template('frisberry.html')



 