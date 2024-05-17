import cv2 as cv
import numpy as np
import time


class Motion:

    def __init__(self):

        self.init_field = np.zeros((480,640))
        self.frame2 = np.zeros((480,640))
        self.frame_update_time = 1 # each 3 second check and change the background
        self.init_time = time.time()
        self.backSub = cv.createBackgroundSubtractorKNN(history=10, dist2Threshold=500, detectShadows=True)

        self.st_previous = []
        self.n_of_frames = 100
        self.sum_of_frames = 0
        self.sumsq_of_frames = 0

        # Parameters for Shi-Tomasi corner detection
        self.feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

        # Parameters for Lucas-Kanade optical flow
        self.lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

        self.p0 = None



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
    
    def adaptive_simple_hsv(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        if self.init_field.all() == 0:
            self.init_field = v

        abs_diff_h = cv.absdiff(v, self.init_field)
        self.init_field = v

        diff_bin = np.where(abs_diff_h > 30, 255, 0)
        diff_bin_uint8 = np.uint8(diff_bin)
        diff_bin_blur = cv.medianBlur(diff_bin_uint8, 3)
        kernel = np.array((9,9), dtype=np.uint8)
        diff_bin_final = cv.morphologyEx(diff_bin_blur, cv.MORPH_CLOSE, kernel, iterations=5)

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

    def detect_with_features(self, frame):

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if self.init_field.all() == 0:
            self.init_field = gray.copy()
            self.p0 = cv.goodFeaturesToTrack(self.init_field, mask=None, **self.feature_params)

        # Calculate optical flow
        p1, st, err = cv.calcOpticalFlowPyrLK(self.init_field, gray, self.p0, None, **self.lk_params)

        # Select good points
        good_new = p1[st == 1]
        good_old = self.p0[st == 1]
        
        for new in good_new:
            a, b = map(int, new.ravel())
            cv.circle(gray, (a, b), 5, (0, 0, 255), -1)

        # Update the previous frame and previous points
        self.init_field = gray.copy()
        self.p0 = good_new.reshape(-1, 1, 2)

        return gray, (good_old, good_new)