import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lsm6ds import Rate, AccelRange, GyroRange
import busio
import storage
import math 
from adafruit_datetime import datetime


# initialize sensor
sclpin = board.GP5
sdapin = board.GP4
i2c = busio.I2C(sclpin, sdapin)
sensor = LSM6DSOX(i2c)

#constants
REPS = 10000
G_FORCE = 9.81
INTERVAL = 0.001

#function for getting additive element when axis datapt should be 0
#used before calibrate_g_axis to get linear additive element
#axis parameter should be number 0 = x, 1 = y, or 2 = z
def calibrate_0_axis(axis):
    print("Calculating additive scalar...") 
    counter = 0
    sum_axis = 0
    while counter < REPS:
        pt_acceleration = sensor.acceleration
        axis_acceleration = pt_acceleration[axis]
        sum_axis += axis_acceleration
        counter += 1
        time.sleep(INTERVAL)
        #progress bar
        tenth_progress = REPS / 10
        if counter % tenth_progress == 0:
            percentage = (counter / REPS)* 100
            string = ""
            for i in range(percentage / 5): #print two hashtags for each 10 percent, ie total 20
                string += "#"
            print(string + "  " + str(percentage) + "%")
    average_zero_difference = sum_axis / REPS 
    return average_zero_difference

#function for getting the linear (multiplicative) element when axis
#axis is the axis facing up to calibrate, additive is the component to be added to datapt before multiplying
#datapt should be g = 9.81
def calibrate_g_axis(axis, additive):
    print("Calculating multiplicative scalar...")
    counter = 0
    sum_axis = 0
    while counter < REPS:
        pt_acceleration = sensor.acceleration
        axis_acceleration = pt_acceleration[axis]
        sum_axis += axis_acceleration + additive
        counter += 1
        #progress bar
        tenth_progress = REPS / 10
        if counter % tenth_progress == 0:
            percentage = (counter / REPS)* 100
            string = ""
            for i in range(percentage / 5): #print two hashtags for each 10 percent, ie total 20
                string += "#"
            print(string + "  " + str(percentage) + "%")
        time.sleep(INTERVAL)
    average_g_difference = sum_axis / REPS
    return G_FORCE / average_g_difference
    
need_header = True

 
calibration_file = open("../data/calibration_constants.csv", "a")

axis = (int(input("Enter which axis to calibrate (x = 0, y = 1, z = 2): ")))
input("position accelerometer with desired axis not facing up. Press enter to continue: ")
print("settling...")
time.sleep(2)
axis_additive = (-1) * calibrate_0_axis(axis)
print(f"Additive component for specified axis is: {axis_additive}")
input("position accelerometer with desired axis facing up. Press enter to continue: ")
print("settling...")
time.sleep(2)
axis_multiplicative = calibrate_g_axis(axis, axis_additive)
print(f"Multiplicative component for specified axis is: {axis_multiplicative}")
axis_letter = ""
if axis == 0:
    axis_letter = "x"
elif axis == 1:
    axis_letter = "y"
elif axis == 2:
    axis_letter = "z"
    
c = datetime.now()
calibration_file.write(str(c) + "," + str(axis_letter) + "," + str(axis_additive) + "," + str(axis_multiplicative) + "\n")
print(str(c) + "," + str(axis_letter) + "," + str(axis_additive) + "," + str(axis_multiplicative) + "\n")
calibration_file.close()

