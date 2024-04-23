import sqlite3
import cv2
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
conn = sqlite3.connect(db_name)

class FaceInfoHelper:
    """
    FaceInfoHelper class to handle database operations
    """
    def insert_record(self, name:str, image:np.ndarray):
        # convert image to image bytes
        image_bytes = cv2.imencode(".jpg", image)[1].tobytes()
        cursor = conn.cursor()
        cursor.execute("insert into EmployeeInfo (name, image) values (?, ?)", (name, image_bytes))
        conn.commit()
        pass

    def get_all_records(self):
        cursor = conn.cursor()
        cursor.execute("select * from EmployeeInfo")
        return cursor.fetchall()

    def get_record_by_image(self, image:np.ndarray):
        image_bytes = cv2.imencode(".jpg", image)[1].tobytes()
        cursor = conn.cursor()
        cursor.execute("select * from EmployeeInfo where image=?", (image_bytes,))
        return cursor.fetchone()
    
class TimeKeepingHelper:
    """
    TimeKeepingHelper class to handle database operations
    """
    def insert_record(self, id:int, checkin:str, checkout:str):
        cursor = conn.cursor()
        cursor.execute("insert into Timekeeping (employee_id, checkin, checkout) values (?, ?, ?)", (id, checkin, checkout))
        conn.commit()
        pass

    def update_checkout_record(self, id:int, checkin:str, checkout:str):
        # select the latest checkin time
        cursor = conn.cursor()
        cursor.execute("select * from Timekeeping where employee_id=?", (id,))
        records = cursor.fetchall()
        latest_checkin = records[-1][2]
        cursor.execute("update Timekeeping set checkout=? where employee_id=? and checkin=?", (checkout, id, latest_checkin))
        conn.commit()
        pass

    def get_lastest_checkin_record_by_id(self, id:int):
        cursor = conn.cursor()
        cursor.execute("select * from Timekeeping where employee_id=?", (id,))
        records = cursor.fetchall()
        latest_checkout = records[-1][3]
        # get id, name, checkin, checkout
        cursor.execute("""
                       select EmployeeInfo.id, EmployeeInfo.name, Timekeeping.checkin, Timekeeping.checkout 
                       from EmployeeInfo 
                       inner join Timekeeping on EmployeeInfo.id=Timekeeping.employee_id 
                       where EmployeeInfo.id=? and Timekeeping.checkout=?
                       """, (id, latest_checkout))
        return cursor.fetchone()

# result = get_all_records()
# print(result)