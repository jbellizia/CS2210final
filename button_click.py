import board
import digitalio

#initialize button
button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def getPressed():
    # returns button value, transforms to true if pressed, false if not
    return not button.value


# print(getPressed())
