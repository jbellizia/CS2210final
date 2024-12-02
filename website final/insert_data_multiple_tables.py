"""
This code is modified from lab 08

"""

import mysql.connector
import json
import sys
import csv
from datetime import datetime 
import os

credentials = json.load(open("credentials.json", "r"))

# this method is used to update the sql database with current data from csv file

def update():
    print("Connecting to database...")
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )
    cursor = database.cursor()
    print("Successful connection") 
 



    try:
        #check file size, if empty, return false, if populated, enter data into database
        check_file = os.stat("../../../../../media/pi/CIRCUITPY/data/this_flight.csv").st_size
    except:
        print("Pico not connected, exiting")
        return False
    print("Checking file...")
    if(check_file == 0):
        print("File had no data, none inserted")
        return False
    else:
        with open("../../../../../media/pi/CIRCUITPY/data/this_flight.csv", "r") as file:
            print("File had data")
            
            id_maker = csv.reader(file)
            next(id_maker)
            first_row = next(id_maker)
            #this makes the capture_id from first row of csv file
            capture_id = str(first_row[0]) + str(first_row[4]) + str(first_row[8])
            print("\n")
            #get the current datetime to log insertion time
            insertion_datetime = str(datetime.now())

            #get last value in capture_sessions table
            cursor.execute(f"SELECT capture_id FROM capture_sessions WHERE id = (SELECT MAX(id) FROM capture_sessions);")
            fetch = cursor.fetchall()
            if fetch:
                last_capture_id = fetch[0][0]
            else:
                last_capture_id = ""
            

            print("Last capture_id: ")
            print(last_capture_id)
            print("capture_id to be inserted: " + capture_id)
            print(last_capture_id == capture_id)
            
            print("Checking for duplicate data...")

            if (last_capture_id != capture_id):
                print("Values unique, proceeding with insertion")
                #insert new capture id
                statement = f"INSERT INTO capture_sessions (capture_id, insertion_datetime) VALUES ('{capture_id}', '{insertion_datetime}');"
                cursor.execute(statement)

                reader = csv.reader(file)
                next(reader)
                print("Inserting new captures into session...")

                #track last row to check if last insertion same as previous last insertion
                last_row = None

                for row in reader:
                    statement = f"INSERT INTO data_capture (capture_id, time_from_start, magnitude_acceleration, gyro_acceleration) VALUES ('{capture_id}',{row[0]}, {row[4]}, {row[8]});"
                    cursor.execute(statement)
                    last_row = row
                database.commit()
            else: 
                print("Values duplicate, not inserting")
                return False
            cursor.close()
            database.close()
            return True

#run update and print result
print(update())

