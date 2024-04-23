import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


"""
Create DB Sqlite3 with a table EmployeeInfo and a table Timekeeping
"""

db_name = os.getenv("DB_NAME")
conn = sqlite3.connect(db_name)

def create_table_face_info():
    cursor = conn.cursor()
    cursor.execute("""Create table if not exists EmployeeInfo (
        id integer primary key autoincrement,
        name text,
        image blob
    )""")

def create_table_timekeeping():
    cursor = conn.cursor()
    cursor.execute("""Create table if not exists Timekeeping (
        id integer primary key autoincrement,
        employee_id integer,
        checkin datetime,
        checkout datetime
    )""")
    
create_table_face_info()
create_table_timekeeping()
conn.close()