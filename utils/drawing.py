import cv2

class ImageDrawing:
    def __init__(self):
        pass

    @staticmethod
    def draw_rectangle(image, x1, y1, x2, y2):
        x1, y1, x2, y2 = map(round, [x1, y1, x2, y2])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image