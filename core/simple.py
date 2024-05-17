import cv2 as cv
import numpy as np
import time
import threading

from motion import Motion
from target import Target
# from ArduinoFirmata import move_servo_x, move_servo_y

def start(strategy):

    #import video
    cap = cv.VideoCapture(0) # cv.VideoCapture(0) for accessing camera

    init_time = time.time()

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
        target.find_center("CENTER")

        # For DETECT_WITH_FEATURES strategy use this to get velocity, speed, direction 
        # target.get_velocity_with_features(location[0], location[1], FPS)

        # For other strategy use 
        # target.get_speed(FPS)

        cv.imshow('Results',img)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def pixelCordToAngel(img_x, img_y):
    ang_x = (img_x/640)*170
    ang_y = (img_y/480)*170
    move_servo_x(ang_x)
    move_servo_y(ang_y)


if __name__ == "__main__":
    start("ADAPTIVE_WITH_FEATURES")