import cv2 as cv
import numpy as np
import time


class Target:
    
    def __init__(self):
        self.x, self.y, self.w, self.h = 0
        self.speed = 0
        self.location = [0,0]
        self.previous_location = [0,0]
    
    def get_location(self, frame):
        self.x, self.y, self.w, self.h = cv.boundingRect(frame)
        return self.x, self.y, self.w, self.h
    
    def draw_rectanganle(self, frame):
        cv.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255,0,0), 4)

    def find_center(self, strategy):

        if strategy == "CENTER":
            self.previous_location = self.location
            self.location = [(self.x+self.w)/2, (self.y+self.h)/2]

        return self.location

    def get_velocity(self):
        speed_x = self.previous_location - self.location