import cv2 as cv
import numpy as np
import time


class Motion:

    def __init__(self):

        self.init_field = np.zeros((480,640))
        self.frame_update_time = 1 # each 3 second check and change the background
        self.init_time = time.time()
        self.backSub = cv.createBackgroundSubtractorKNN(dist2Threshold=500, detectShadows=False)

    def adaptive(self, frame):

        fgMask = self.backSub.apply(frame)
        kernel = np.array((9,9), dtype=np.uint8)
        diff_bin = cv.medianBlur(fgMask, 3)
        diff_bin = cv.morphologyEx(diff_bin, cv.MORPH_CLOSE, kernel, iterations=1)

        return diff_bin

    def static(self, frame):

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if self.init_field.all() == 0:
            self.init_field = gray

        abs_diff = cv.absdiff(gray, self.init_field)
        diff_bin = np.where(abs_diff > 50, 255, 0)
        diff_bin_uint8 = np.uint8(diff_bin)
        diff_bin_blur = cv.medianBlur(diff_bin_uint8, 3)
        kernel = np.array((9,9), dtype=np.uint8)
        diff_bin_final = cv.morphologyEx(diff_bin_blur, cv.MORPH_CLOSE, kernel, iterations=5)
        
        return diff_bin_final

    def semi_static():

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if self.init_field.all() == 0:
            self.init_field = gray

        abs_diff = cv.absdiff(gray, self.init_field)
        self.init_field = gray
        diff_bin = np.where(abs_diff > 50, 255, 0)
        diff_bin_uint8 = np.uint8(diff_bin)
        diff_bin_blur = cv.medianBlur(diff_bin_uint8, 3)
        kernel = np.array((9,9), dtype=np.uint8)
        diff_bin_final = cv.morphologyEx(diff_bin_blur, cv.MORPH_CLOSE, kernel, iterations=5)
        
        return diff_bin_final