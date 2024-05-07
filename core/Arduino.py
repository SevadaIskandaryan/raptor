import serial
import time

# Open the serial port
ser = serial.Serial('COM3', 9600)  # Change '/dev/ttyUSB0' to the appropriate serial port
#time.sleep(2)  # Wait for the Arduino to initialize


def moveCoordinates(x, y):
    # Send coordinates
    coordinates = "{}:{}".format(x, y)
    #print(coordinates)
    ser.write(coordinates.encode())
    # Close the serial port

def close_port():
    ser.close()
