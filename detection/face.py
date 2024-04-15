from deepface import DeepFace
import cv2
from skimage import data
from skimage.feature import Cascade

trained_file = data.lbp_frontal_face_cascade_filename()
haar_cascade = cv2.CascadeClassifier("/Volumes/Untitled 2/2-PPBL-Cham-Cong/timekeeping_realtime/detection/haarcascade_frontalface_default.xml") 

face_detector = Cascade(trained_file)

class FaceDetector:
    def __init__(self, image_path, store):
        self.image_path = image_path
        self.store = store

    @staticmethod
    def detect_v2(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = haar_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=9)
        # faces = face_detector.detect_multi_scale(image=image, scale_factor=1.2, step_ratio=1, min_size=(50, 50), max_size=(200, 200))
        return faces
    
    def detect(self):
        metrics = ["cosine", "euclidean", "euclidean_l2"]
        backends = [
        'opencv', 
        'ssd', 
        'dlib', 
        'mtcnn', 
        'fastmtcnn',
        'retinaface', 
        'mediapipe',
        'yolov8',
        'yunet',
        'centerface',
        ]
        dfs = DeepFace.find(img_path=self.image_path, db_path=self.store, distance_metric=metrics[0])
        
        data_faces = []
        for df in dfs:
            target_x = df["target_x"].values[0]
            target_y = df["target_y"].values[0]
            target_w = df["target_w"].values[0]
            target_h = df["target_h"].values[0]

            target_x2 = target_x + target_w
            target_y2 = target_y + target_h
            # source_x = df["source_x"].values[0]
            # source_y = df["source_y"].values[0]
            # source_w = df["source_w"].values[0]
            # source_h = df["source_h"].values[0]
            # threshold = df["threshold"].values[0]
            # distance = df["distance"].values[0]

            data_info = {
                "target_x": target_x,
                "target_y": target_y,
                "target_x2": target_x2,
                "target_y2": target_y2,
                "target_w": target_w,
                "target_h": target_h,
                # "source_x": source_x,
                # "source_y": source_y,
                # "source_w": source_w,
                # "source_h": source_h,
                # "threshold": threshold,
                # "distance": distance,
            }
            data_faces.append(data_info)
        return data_faces
        pass