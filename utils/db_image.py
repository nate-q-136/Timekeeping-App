import sqlite3
import cv2
import numpy as np
import os

db_name = os.getenv("DB_NAME")
conn = sqlite3.connect(db_name)


def insert_record(name:str, image:np.ndarray):
    # convert image to image bytes
    image_bytes = cv2.imencode(".jpg", image)[1].tobytes()
    cursor = conn.cursor()
    cursor.execute("insert into EmployeeInfo (name, image) values (?, ?)", (name, image_bytes))
    conn.commit()
    pass