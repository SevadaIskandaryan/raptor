import cv2 as cv
import numpy as np
import time
import threading

from motion import Motion
from Arduino import moveCoordinates, close_port

def start():

    #close_port()

    #import video
    cap = cv.VideoCapture(0) # cv.VideoCapture(0) for accessing camera

    init_time = time.time()

    detect_motion = Motion()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        diff_bin = detect_motion.adaptive(frame)

        x,y,w,h = cv.boundingRect(diff_bin)
        cv.rectangle(diff_bin, (x, y), (x + w, y + h), (255,0,0), 4)

        threading.Timer(0.1, pixelCordToAngel((x+w)/2, (y+h)/2)).start()

        cv.imshow('foregroundMask',diff_bin)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def pixelCordToAngel(img_x, img_y):
    ang_x = (img_x/640)*170
    ang_y = (img_y/480)*170
    moveCoordinates(int(ang_x), int(ang_y))


if __name__ == "__main__":
    start()
# for fixing brightness - hsv