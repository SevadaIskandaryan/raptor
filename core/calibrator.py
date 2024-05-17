import cv2 as cv
import numpy as np
import time

class Calibrator:

    def __init__(self):
        self.height, self.width = 0, 0
        self.center_x, self.center_y = 0, 0
        self.radius = 30
        self.color = (0, 255, 0)
        self.thickness = 2
        self.isCalibrated = False
        self.calibrated_dot_frame_count = 0 # keep count of frames where laser dot exists
        self.calibrated_dot_verify_count = 100 # if exists in 100 frames change status isCalibrated to True

        # Define the range for bright red color in HSV
        self.lower_red1 = np.array([0, 100, 100])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([160, 100, 100])
        self.upper_red2 = np.array([180, 255, 255])

    def draw_calibrator(self, frame):

        if self.height == 0 or self.width == 0:
            self.height, self.width = frame.shape[:2]
            self.center_x, self.center_y =  self.width // 2, self.height // 2
        
        # Draw the horizontal line
        cv.line(frame, (0, self.center_y), (self.width, self.center_y), self.color, self.thickness)
        
        # Draw the vertical line
        cv.line(frame, (self.center_x, 0), (self.center_x, self.height), self.color, self.thickness)
        
        # Draw the circle at the center
        cv.circle(frame, (self.center_x, self.center_y), self.radius, self.color, self.thickness)

        return frame
    
    def verify_calibration(self, frame):
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

         # Create masks for the two red ranges
        mask1 = cv.inRange(hsv_frame, self.lower_red1, self.upper_red1)
        mask2 = cv.inRange(hsv_frame, self.lower_red2, self.upper_red2)
        
        # Combine the masks
        red_mask = cv.bitwise_or(mask1, mask2)

        circle_mask = np.zeros_like(red_mask)
        cv.circle(circle_mask, (self.center_x, self.center_y), self.radius, 255, -1)

        red_mask = cv.bitwise_and(red_mask, red_mask, mask=circle_mask)

        # Find contours in the mask
        contours, _ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            self.calibrated_dot_frame_count += 1
            if self.calibrated_dot_frame_count >= self.calibrated_dot_verify_count:
                self.calibrated_dot_frame_count = 0
                self.isCalibrated = True
        else:
            # To make sure it is present in all consecutive frames 
            # reset value to 0
            self.calibrated_dot_frame_count = 0



    
    def start_calibrator(self):
        cap = cv.VideoCapture(0) # cv.VideoCapture(0) for accessing camera

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come here
            calibrator_frame = self.draw_calibrator(frame)
            self.verify_calibration(frame)

            cv.imshow('foregroundMask',calibrator_frame)
            if cv.waitKey(1) == ord('q') or self.isCalibrated:
                break

        cap.release()
        cv.destroyAllWindows()
        