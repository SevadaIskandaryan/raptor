import cv2 as cv
import numpy as np
import time

#import video
cap = cv.VideoCapture(0) # cv.VideoCapture(0) for accessing camera


init_field = np.zeros((480,640))
prev_frame = np.zeros((480,640))
prev_frame_mask = np.zeros((480,640))
frame_update_time = 5 # each 3 second check and change the background
init_time = time.time()

def get_mask(frame1, frame2, kernel=np.array((9,9), dtype=np.uint8)):
    """ Obtains image mask
        Inputs: 
            frame1 - Grayscale frame at time t
            frame2 - Grayscale frame at time t + 1
            kernel - (NxN) array for Morphological Operations
        Outputs: 
            mask - Thresholded mask for moving pixels
        """

    frame_diff = cv.subtract(frame1, frame2)
    #frame_diff = frame1 - frame2
    frame_diff = np.where(frame_diff > 10, 255, 0)
    frame_diff = np.uint8(frame_diff)
    # blur the frame difference
    #frame_diff = cv.medianBlur(frame_diff, 3)
    
    # mask = cv.adaptiveThreshold(frame_diff, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv.THRESH_BINARY_INV, 11, 3)

    mask = frame_diff #cv.medianBlur(frame_diff, 3)

    # morphological operations
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=1)

    return mask


#if using camera uncomment this
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break


    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # if prev_frame.all() == 0:
    #     prev_frame = gray
    #     init_field = gray

    kernel = np.array((9,9), dtype=np.uint8)
    # mask = get_mask(gray, prev_frame, kernel)
    # prev_frame = gray

    # mask = mask.astype(np.float32)/255
    # init_field = np.where(mask == 1, gray, init_field)#init_field*(1-mask) + mask*prev_frame
    if init_field.all() == 0:
        init_field = gray

    # if time.time()-init_time > frame_update_time:
    #     init_field = gray
    #     init_time = time.time()

    #init_field = init_field.astype(np.uint8)
    # diff1 = cv.subtract(init_field, gray)
    # diff_bin1 = np.where(diff1 > 50, 255, 0)
    # diff_bin1 = np.uint8(diff_bin1)
    # diff_bin1 = cv.medianBlur(diff_bin1, 3)
    # diff_bin1 = cv.morphologyEx(diff_bin1, cv.MORPH_CLOSE, kernel, iterations=5)
    # cv.imshow('frame', diff_bin1)

    diff2 = cv.absdiff(gray, init_field)
    diff_bin2 = np.where(diff2 > 50, 255, 0)
    diff_bin2 = np.uint8(diff_bin2)
    diff_bin2 = cv.medianBlur(diff_bin2, 3)
    diff_bin2 = cv.morphologyEx(diff_bin2, cv.MORPH_CLOSE, kernel, iterations=5)
    x,y,w,h = cv.boundingRect(diff_bin2)
    cv.rectangle(diff_bin2, (x, y), (x + w, y + h), (255,0,0), 4)
    cv.imshow('frame1', diff_bin2)
    init_field = gray
    #diff_bin1 = diff_bin1.astype(np.float32)/255
    # diff_bin2_float = diff_bin2.astype(np.float32)/255
    # init_field = np.where(diff_bin2_float == 1, gray, init_field)

    # diff1 = cv.subtract(init_field, gray)
    # diff_bin1 = np.where(diff1 > 50, 255, 0)
    # diff_bin1 = np.uint8(diff_bin1)
    # diff_bin1 = cv.medianBlur(diff_bin1, 3)
    # diff_bin1 = cv.morphologyEx(diff_bin1, cv.MORPH_CLOSE, kernel, iterations=5)
    # cv.imshow('frame2', init_field)

    if cv.waitKey(1) == ord('q'):
        break


# compute motion mask

cap.release()
cv.destroyAllWindows()