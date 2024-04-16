import numpy as np
import cv2
import os
import math

class ImageHandler:
    def __init__(self):
        pass

    def calculate_image_difference(self, image1: np.ndarray, image2: np.ndarray) -> float:
        # convert image to grayscale
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # calculate the absolute difference between the 2 images
        difference = cv2.absdiff(gray_image1, gray_image2)
        # calculate the mean of the difference
        difference_mean = np.mean(difference)
        return difference_mean
    
    def get_closest_match(self, image: np.ndarray, images: list) -> str:
        min_diff = math.inf
        closest_match = ""
        for name, img in images:
            diff = self.calculate_image_difference(image, img)
            if diff < min_diff:
                min_diff = diff
                closest_match = name
        return closest_match