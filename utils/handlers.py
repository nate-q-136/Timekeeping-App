import numpy as np
import cv2
import os
import math
from .db_image import (
    FaceInfoHelper
)
from typing import Tuple, List

class ImageHandler:
    """
    Handle image processing tasks
    """
    def __init__(self):
        pass

    def calculate_image_difference(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Calculate the difference between 2 images
        """
        # convert image to grayscale
        height, width = image1.shape[:2]
        image2_resized = cv2.resize(image2, (width, height))

        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2_resized, cv2.COLOR_BGR2GRAY)
        # calculate the absolute difference between the 2 images
        difference = cv2.absdiff(gray_image1, gray_image2)
        # calculate the mean of the difference
        difference_mean = np.mean(difference)
        return difference_mean
    
    def get_closest_match(self, image: np.ndarray, list_names_images: list) -> Tuple[int, str, np.ndarray]:
        """
        Get the closest match between the differences of frame image and the list of database images
        """
        min_diff = math.inf
        closest_match = ""
        for id, name, img in list_names_images:
            diff = self.calculate_image_difference(image, img)
            if diff < min_diff:
                min_diff = diff
                if min_diff < 35:
                    closest_match = (id, name, img)
                else:
                    closest_match = (-1, "Unknown", img)
        return closest_match
    
    def convert_bytes_to_numpy(self, image_bytes: bytes) -> np.ndarray:
        """
        Convert image bytes (blob from database) to numpy array
        """
        image = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    
    def check_info_image(self, image:np.ndarray)->Tuple[int, str, np.ndarray]:
        """
        Check the image with the database to get the closest match
        """
        all_records = FaceInfoHelper().get_all_records()
        all_names_images = []
        for record in all_records:
            id_info, name_info, image_info = record
            image_np = self.convert_bytes_to_numpy(image_info)
            all_names_images.append((id_info, name_info, image_np))
        closest_match = self.get_closest_match(image, all_names_images)
        return closest_match
    
        pass