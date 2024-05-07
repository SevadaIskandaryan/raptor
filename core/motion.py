import cv2 as cv
import numpy as np
import time


class Motion:

    def __init__(self):

        self.init_field = np.zeros((480,640))
        self.frame_update_time = 1 # each 3 second check and change the background
        self.init_time = time.time()
        self.backSub = cv.createBackgroundSubtractorKNN(dist2Threshold=500, detectShadows=False)

        self.st_previous = []
        self.n_of_frames = 100
        self.sum_of_frames = 0
        self.sumsq_of_frames = 0

    def adaptive(self, frame):

        fgMask = self.backSub.apply(frame)
        kernel = np.array((9,9), dtype=np.uint8)
        diff_bin = cv.medianBlur(fgMask, 3)
        diff_bin = cv.morphologyEx(diff_bin, cv.MORPH_CLOSE, kernel, iterations=1)

        return diff_bin
    
    def adaptive_simple(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if self.init_field.all() == 0:
            self.init_field = gray

        abs_diff = cv.absdiff(gray, self.init_field)
        diff_bin = np.where(abs_diff > 50, 255, 0)
        diff_bin_uint8 = np.uint8(diff_bin)
        diff_bin_blur = cv.medianBlur(diff_bin_uint8, 3)
        kernel = np.array((9,9), dtype=np.uint8)
        diff_bin_final = cv.morphologyEx(diff_bin_blur, cv.MORPH_CLOSE, kernel, iterations=5)
        self.init_field = gray
        
        return diff_bin_final
    
    def adaptive_st(self, frame):
        stdev_gray = np.zeros((480,640))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = gray.astype('f4')
        if len(self.st_previous) == self.n_of_frames:
            stdev_gray = np.sqrt(self.sumsq_of_frames / self.n_of_frames - np.square(self.sum_of_frames / self.n_of_frames))
            cv.imshow('stdev_gray', stdev_gray)
            self.sum_of_frames -= self.st_previous[0]
            self.sumsq_of_frames -=np.square(self.st_previous[0])
            self.st_previous.pop(0)
        self.st_previous.append(gray)
        self.sum_of_frames = self.sum_of_frames + gray
        self.sumsq_of_frames = self.sumsq_of_frames + np.square(gray)
        if(stdev_gray.all() == 0):
            return np.uint8(gray)
        return np.uint8(stdev_gray)

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