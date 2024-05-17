import cv2 as cv
import numpy as np
import time
import math


class Target:
    
    def __init__(self):
        self.x, self.y, self.w, self.h = 0, 0, 0, 0
        self.speed = 0
        self.location = [0,0]
        self.previous_location = [0,0]
    
    def get_location(self, frame):
        self.x, self.y, self.w, self.h = cv.boundingRect(frame)
        return self.x, self.y, self.w, self.h
    
    def draw_rectanganle(self, frame):
        cv.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255,0,0), 4)
        return frame

    def find_center(self, strategy):

        if strategy == "CENTER":
            self.previous_location = self.location
            self.location = [(self.x+self.w)/2, (self.y+self.h)/2]
        else:
            self.previous_location = self.location
            self.location = [(self.x+self.w)/4, (self.y+self.h)/4]
        # TODO
        # add different strategies like location in top, bottom, left etc.
        return self.location

    # Get speed if needed
    def get_speed(self, FPS):
        dt = 1/FPS
        displacement_x = self.previous_location[0] - self.location[0]
        displacement_y = self.previous_location[1] - self.location[1]
        displacement = math.sqrt(displacement_x**2 + displacement_y**2)
        # Calculate velocity
        speed = displacement / dt
        return speed
    
    def get_velocity_with_features(self, new_points, old_points, FPS):
        dt = 1/FPS
        displacement = new_points - old_points
        # Calculate velocity
        velocities = displacement / dt
        velocity = velocities[0]
        speed = np.linalg.norm(velocity)
        direction = np.arctan2(velocity[1], velocity[0]) * 180 / np.pi
        return velocity, speed, direction
    