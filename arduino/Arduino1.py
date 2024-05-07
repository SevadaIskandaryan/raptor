import serial
import time

# Open the serial port
# ser = serial.Serial('COM3', 9600)  # Change '/dev/ttyUSB0' to the appropriate serial port
# time.sleep(2)  # Wait for the Arduino to initialize


def moveCoordinates(x, y):
    ser = serial.Serial('COM3', 9600)  # Change '/dev/ttyUSB0' to the appropriate serial port
    time.sleep(2)  # Wait for the Arduino to initialize
    # Send coordinates
    coordinates = "{}:{}".format(x, y)
    ser.write(coordinates.encode())
    ser.close()
    #Close the serial port
    #ser.close()

for i in range(0, 90):
    moveCoordinates(i, i)
    time.sleep(1)