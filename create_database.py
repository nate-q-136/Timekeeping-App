import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


db_name = os.getenv("DB_NAME")
conn = sqlite3.connect(db_name)

def create_table():
    cursor = conn.cursor()
    cursor.execute("""Create table if not exists EmployeeInfo (
        id integer primary key autoincrement,
        name text,
        image blob
    )""")

create_table()
conn.close()