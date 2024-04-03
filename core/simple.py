import cv2 as cv
import numpy as np
import time

from motion import Motion

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
    diff_bin = detect_motion.static(frame)

    x,y,w,h = cv.boundingRect(diff_bin)
    cv.rectangle(diff_bin, (x, y), (x + w, y + h), (255,0,0), 4)


    cv.imshow('foregroundMask',diff_bin)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

# for fixing brightness - hsv