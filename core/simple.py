import cv2 as cv
import numpy as np
import threading

import pyfirmata2
import time

from motion import Motion
from target import Target

coordinates = [320.0, 480.0]
enable_arduino = True
fov = [60, 40]

def move_servo(servo_x, servo_y):
    while enable_arduino:
        img_x, img_y = coordinates
        print(img_x, img_y)
        ang_x = ((640-img_x)/640)*120
        ang_y = ((480-img_y)/480)*180
        print(ang_x, ang_y)
        servo_x.write(ang_x)
        time.sleep(0.1)
        servo_y.write(ang_y)
        time.sleep(0.1)

def start(strategy):

    # enable arduino
    if False:
        PORT = pyfirmata2.Arduino.AUTODETECT

        if PORT is None:
            PORT = "COM3"
        print(PORT)
        # Creates a new board
        board = pyfirmata2.Arduino(PORT)
        print("Setting up the connection to the board ...")
        print(board)
        SERVO_PIN_X = 10
        SERVO_PIN_Y = 9
        # Setup the digital pin as servo
        servo_x = board.get_pin('d:{}:s'.format(SERVO_PIN_X))
        servo_y = board.get_pin('d:{}:s'.format(SERVO_PIN_Y))

        t1 = threading.Thread(target=move_servo, daemon=True, args=(servo_x, servo_y))
        t1.start()


    #import video
    cap = cv.VideoCapture(0) # cv.VideoCapture(0) for accessing camera

    detect_motion = Motion()
    target = Target()


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        FPS = cap.get(cv.CAP_PROP_FPS)
        
        match strategy:
            case "STATIC":
                img = detect_motion.static(frame)
            case "ADAPTIVE":
                img = detect_motion.adaptive(frame)
            case "ADAPTIVE_SIMPLE":
                img = detect_motion.adaptive_simple(frame)
            case "ADAPTIVE_SIMPLE_HSV":
                img = detect_motion.adaptive_simple_hsv(frame)
            case "ADAPTIVE_STD":
                img = detect_motion.adaptive_st(frame)
            case "DETECT_WITH_FEATURES":
                img, location = detect_motion.detect_with_features(frame)
            case "ADAPTIVE_WITH_FEATURES":
                img1 = detect_motion.adaptive(frame)
                img2, _ = detect_motion.detect_with_features(frame)

                kernel = np.ones((5, 5), np.uint8) 
                img1 = cv.dilate(img1, kernel, iterations=3)
                img1 = cv.morphologyEx(img1, cv.MORPH_CLOSE, kernel, iterations=5)

                img = img1 & img2
            case default:
                img = detect_motion.adaptive_simple(frame)
        
        target.get_location(img)
        img = target.draw_rectanganle(img)
        global coordinates
        tmp_cord = target.find_center("CENTER")
        if tmp_cord[0] != 0.0 and tmp_cord[1] != 0.0:
            coordinates = target.find_center("CENTER")
        
        # For DETECT_WITH_FEATURES strategy use this to get velocity, speed, direction 
        # target.get_velocity_with_features(location[0], location[1], FPS)

        # For other strategy use 
        # target.get_speed(FPS)

        cv.imshow('Results',img)
        if cv.waitKey(1) == ord('q'):
            #cv.imwrite(strategy+".jpg", img)
            global enable_arduino
            enable_arduino = False
            break

    #board.exit()
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    start("STATIC")