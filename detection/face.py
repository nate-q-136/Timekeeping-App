import cv2     
from skimage import data
from skimage.feature import Cascade
import numpy as np

# cascade face detection
trained_file = data.lbp_frontal_face_cascade_filename()
haar_cascade = cv2.CascadeClassifier("/Volumes/Untitled 2 1/2-PPBL-Cham-Cong/timekeeping_realtime/detection/haarcascade_frontalface_default.xml") 

face_detector = Cascade(trained_file)

# dnn face detection
yunet = cv2.FaceDetectorYN.create(
    model="/Volumes/Untitled 2 1/2-PPBL-Cham-Cong/timekeeping_realtime/detection/face_detection_yunet_2023mar.onnx",
    config='',
    input_size=(320, 320),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000,
    backend_id=cv2.dnn.DNN_BACKEND_DEFAULT,
    target_id=cv2.dnn.DNN_TARGET_CPU
)

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
    
    @staticmethod
    def detect_v3(image):
        yunet.setInputSize((image.shape[1], image.shape[0]))
        _, faces = yunet.detect(image)
        coors_faces = []
        for face in faces:
            bbox = face[0:4].astype(np.int32)
            coors_faces.append(bbox)
        return coors_faces
    
    
  