import math
import cv2
import numpy as np


video = cv2.VideoCapture(0)
previous = []
n_of_frames = 2

sum_of_frames = 0
sumsq_of_frames = 0

while True:
   ret, frame = video.read()
   if ret:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = gray.astype('f4')
    if len(previous) == n_of_frames:
        stdev_gray = np.sqrt(sumsq_of_frames / n_of_frames - np.square(sum_of_frames / n_of_frames))
        cv2.imshow('stdev_gray', stdev_gray)
        sum_of_frames -= previous[0]
        sumsq_of_frames -=np.square(previous[0])
        previous.pop(0)
    previous.append(gray)
    sum_of_frames = sum_of_frames + gray
    sumsq_of_frames = sumsq_of_frames + np.square(gray)

    #cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()