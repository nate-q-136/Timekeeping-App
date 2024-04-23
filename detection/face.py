import cv2     
from skimage import data
import numpy as np
import os

# get the full path of current file
current_path = os.path.dirname(os.path.abspath(__file__))
print("current_path: ", current_path)
yunet_filename = "face_detection_yunet_2023mar.onnx"
yunet_fullpath = os.path.join(current_path, yunet_filename)


# dnn face detection with Yunet
yunet = cv2.FaceDetectorYN.create(
    model=yunet_fullpath,
    config='',
    input_size=(320, 320),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000,
    backend_id=cv2.dnn.DNN_BACKEND_DEFAULT,
    target_id=cv2.dnn.DNN_TARGET_CPU
)

class FaceDetector:
    """
    Detect face in image with Yunet model
    """
    def __init__(self, image_path, store):
        self.image_path = image_path
        self.store = store
    
    @staticmethod
    def detect_v3(image):
        yunet.setInputSize((image.shape[1], image.shape[0]))
        _, faces = yunet.detect(image)
        coors_faces = []
        for face in faces:
            bbox = face[0:4].astype(np.int32)
            coors_faces.append(bbox)
        return coors_faces
    
    
  