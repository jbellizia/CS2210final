import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import busio
import storage
import math
from adafruit_datetime import datetime
import circuitpython_csv as csv
import button_click
import digitalio
import supervisor

def main():
    usb_connected = supervisor.runtime.usb_connected
    if usb_connected:
        # make note of USB connection status in usb connection file
        with open("usb-connection.txt", "w") as usbFile:
            usbFile.write("USB connection at runtime")
    elif not usb_connected:
        # make note of USB connection status in usb connection file
        with open("usb-connection.txt", "w") as usbFile:
            usbFile.write("NO USB connection at runtime")
            
        # initialize sensor
        sclpin = board.GP5
        sdapin = board.GP4
        i2c = busio.I2C(sclpin, sdapin)
        sensor = LSM6DSOX(i2c)            
        
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


        # Turn LED off
        led = digitalio.DigitalInOut(board.LED)
        led.direction = digitalio.Direction.OUTPUT
        LED_on = False
        led.value = LED_on

        # open data file
        with open('/data/this_flight.csv', 'w') as outFile:
            outFile.write('Time from start (s), X Acceleration (m/s^2), Y Acceleration (m/s^2), Z acceleration (m/s^2), Magnitude Acceleration (m/s^2), X Gyro (dps), Y Gyro (dps), Z Gyro (dps), Magnitude Gyro (dps)\n') # header
            
            print("Running program")
            
            # for making sure orig time is only taken on first iteration of running
            #the write script
            orig_time = -1

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
                   
                    # set the original time of the run (start of program)
                    if (orig_time == -1):
                        orig_time = time.monotonic()            
                    
                    # toggle LED
                    LED_on = not LED_on
                    led.value = LED_on

                    # get point values
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
                    
                    # get current time in seconds, subtract original to get actual current time
                    timeval = time.monotonic()
                    time_now = int((timeval - orig_time) * 1000) / 1000
                    
                    #write to data file and flush each iteration
                    outFile.write(str(time_now) + ", " + str(x_acceleration) + ", " + str(y_acceleration) + ", " + str(z_acceleration) + ", " + str(mag_acceleration)
                                  + ", " + str(x_gyro)+ ", " + str(y_gyro)+ ", " + str(z_gyro)+ ", " + str(mag_gyro) + "\n") # insert datum
                    outFile.flush()
        #             print(str(time_now) + ", " + str(x_acceleration) + ", " + str(y_acceleration) + ", " + str(z_acceleration) + ", " + str(mag_acceleration)
        #                   + ", " + str(x_gyro)+ ", " + str(y_gyro)+ ", " + str(z_gyro)+ ", " + str(mag_gyro))
                time.sleep(0.1)
                
if __name__ == "__main__":
    main()
else:
    main()
        
    



