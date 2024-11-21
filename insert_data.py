"""
This code is modified from lab 08

"""

import mysql.connector
import json
import sys
import csv


credentials = json.load(open("credentials.json", "r"))

# this method is used to update the sql database with current data from csv file


# TODO - would be interesting to make a more complex linked SQL structure with sessions list and data capture table that points to it


def update():
    try:
        database = mysql.connector.connect(
            host=credentials["host"],
            user=credentials["user"],
            passwd=credentials["password"],
            database=credentials["database"]
        )
        cursor = database.cursor()
        with open("data/this_flight.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                insert_values = {row[0], row[4], row[8]}
                statement = f"INSERT INTO frisberry_data (time_from_start, magnitude_acceleration, gyro_acceleration) VALUES ({row[0]}, {row[4]}, {row[8]});"
                print(statement)
                cursor.execute(statement)
        database.commit()
        cursor.close()
        database.close()
        
        return True
    except:
        return False

#run update and print result
print(update())
