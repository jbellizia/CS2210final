import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lsm6ds import Rate, AccelRange, GyroRange
import busio
import storage
import math
from adafruit_datetime import datetime
import circuitpython_csv as csv
import button_click

# initialize sensor
sclpin = board.GP5
sdapin = board.GP4
i2c = busio.I2C(sclpin, sdapin)
sensor = LSM6DSOX(i2c)
sensor.accelerometer_range = AccelRange.RANGE_2G

# initialize calibration components
x_additive = 0
y_additive = 0
z_additive = 0
x_multiplicative = 0
y_multiplicative = 0
z_multiplicative = 0

# get most recent calibration constants from file
with open("../data/calibration_constants.csv",  "r") as constants_file:
    csvreader = csv.reader(constants_file)
    for row in csvreader:
        if row[1] == 'x':
            x_additive = float(row[2])
            x_multiplicative = float(row[3])
        if row[1] == 'y':
            y_additive = float(row[2])
            y_multiplicative = float(row[3])
        if row[1] == 'z':
            z_additive = float(row[2])
            z_multiplicative = float(row[3])

# initialize running variables to false, start not running
isRunning = False
lastPressed = False

# open data file
with open('/data/this_flight.csv', 'w') as outFile:
    outFile.write('Time, X Acceleration, Y Acceleration, Z acceleration, Magnitude Acceleration, X Gyro, Y Gyro, Z Gyro, Magnitude Gyro\n') # header
    
    print("Running program")
    #loop while there is power
    while True:
        # get true / false button value for running or not
        pressed = button_click.getPressed()
        
        # toggle running if the button is actually pressed and the
        # last press didn't have the same value (basically won't switch super fast
        # if you hold it down
        if pressed and not lastPressed:
            isRunning = not isRunning
            if isRunning:
                print("Writing data")
            else:
                print("Stopped writing data")
        # debounce
        lastPressed = pressed
        
        # if true, run program: if false, keep moving, checking every 0.5 seconds
        if(isRunning):
            pt_acceleration = sensor.acceleration
            pt_gyro = sensor.gyro
            x_acceleration = (pt_acceleration[0] + x_additive) * x_multiplicative
            y_acceleration = (pt_acceleration[1] + y_additive) * y_multiplicative
            z_acceleration = (pt_acceleration[2] + z_additive) * z_multiplicative
            mag_acceleration = math.sqrt((x_acceleration ** 2) + (y_acceleration ** 2) + (z_acceleration ** 2))
            x_gyro = pt_gyro[0]
            y_gyro = pt_gyro[1]
            z_gyro = pt_gyro[2] 
            mag_gyro = math.sqrt((x_gyro ** 2) + (y_gyro ** 2) + (z_gyro ** 2))
            c = datetime.now()
            outFile.write(str(c) + ", " + str(x_acceleration) + ", " + str(y_acceleration) + ", " + str(z_acceleration) + ", " + str(mag_acceleration)
                          + ", " + str(x_gyro)+ ", " + str(y_gyro)+ ", " + str(z_gyro)+ ", " + str(mag_gyro) + "\n") # insert datum
            outFile.flush()
#             print(str(c) + ", " + str(x_acceleration) + ", " + str(y_acceleration) + ", " + str(z_acceleration) + ", " + str(mag_acceleration)
#                   + ", " + str(x_gyro)+ ", " + str(y_gyro)+ ", " + str(z_gyro)+ ", " + str(mag_gyro))
        time.sleep(0.25)
            
        
        
    


