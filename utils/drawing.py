import cv2
import numpy as np
from typing import Tuple, List
class ImageDrawing:
    def __init__(self):
        pass

    @staticmethod
    def draw_rectangle(image, id:int, name:str, x1:int, y1:int, x2:int, y2:int)->np.ndarray:
        x1, y1, x2, y2 = map(round, [x1, y1, x2, y2])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{id}:{name}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        return image