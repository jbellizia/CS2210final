import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lsm6ds import Rate, AccelRange, GyroRange
import busio
import storage
import math
from adafruit_datetime import datetime
import circuitpython_csv as csv
import switch

# initialize sensor
def main():
    sclpin = board.GP5
    sdapin = board.GP4
    i2c = busio.I2C(sclpin, sdapin)
    sensor = LSM6DSOX(i2c)

    sensor.accelerometer_range = AccelRange.RANGE_2G

    # open data file
    with open('/data/this_flight.csv', 'w') as outFile:
        outFile.write('Time, X Acceleration, Y Acceleration, Z acceleration, Magnitude Acceleration, X Gyro, Y Gyro, Z Gyro, Magnitude Gyro\n') # header

        #initialize calibration components
        x_additive = 0
        y_additive = 0
        z_additive = 0
        x_multiplicative = 0
        y_multiplicative = 0
        z_multiplicative = 0

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

        while switch.getSwitchValue():
            #get accel and gyro at pt
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
            print(str(c) + ", " + str(x_acceleration) + ", " + str(y_acceleration) + ", " + str(z_acceleration) + ", " + str(mag_acceleration)
                          + ", " + str(x_gyro)+ ", " + str(y_gyro)+ ", " + str(z_gyro)+ ", " + str(mag_gyro))
            time.sleep(0.5)
            
if __name__ == '__main__':
    main()
