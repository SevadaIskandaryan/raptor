import cv2 as cv
import numpy as np
import time

#import video
cap = cv.VideoCapture(0) # cv.VideoCapture(0) for accessing camera


init_field = np.zeros((480,640))
prev_frame = np.zeros((480,640))
prev_frame_mask = np.zeros((480,640))
frame_update_time = 1 # each 3 second check and change the background
init_time = time.time()

#if using camera uncomment this
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    if init_field.all() == 0:
        init_field = gray
    
    # if prev_frame.all() != 0:#time.time() - init_time > frame_update_time:
    #     init_field = prev_frame_mask*init_field + (1-prev_frame_mask)*prev_frame

    #diff = prev_frame - gray
    diff = init_field - gray #cv.subtract(gray, init_field) #init_field - gray
    prev_frame = gray
    diff_bin = np.where((diff > 20) & (diff < 200), 255, 0)
    #diff_bin = np.where(diff > 50, 255, 0)
    prev_frame_mask = diff_bin.astype("float32")/255
    #diff_bin = cv.merge((diff_bin, diff_bin, diff_bin))
    diff_bin = np.uint8(diff_bin)
    # Display the resulting frame
    cv.imshow('frame', diff_bin)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()