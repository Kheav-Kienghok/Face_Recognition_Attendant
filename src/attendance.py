import sqlite3
import os
from datetime import datetime, time

db_path = 'data/database.sqlite'
if not os.path.exists(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)

def initialize():

    conn.executescript('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name VARCHAR(100) NOT NULL,
            gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            attendance_status TEXT CHECK (attendance_status IN ('Present', 'Absent', 'Late')) NOT NULL
        )
    ''')

    conn.commit()
    return "Ok"


# C: Create 
def insert_attendance(student_name, gender, date, time, attendance_status):

    query = '''
        INSERT INTO attendance (student_name, gender, date, time, attendance_status)
        VALUES (?, ?, ?, ?, ?)
    '''
    conn.execute(query, (student_name, gender, date, time, attendance_status))
    conn.commit()
    
    return "Ok"


# R: Read
def get_all_attendance():
    query = "SELECT * FROM attendance"
    
    cursor = conn.execute(query)
    records = cursor.fetchall()
    
    return records

def check_attendance_exists(student_name, date):
    query = "SELECT student_name FROM attendance WHERE student_name = ? AND date = ?"
    cursor = conn.execute(query, (student_name, date))
    result = cursor.fetchall()
    
    if len(result) > 0: 
        return True
    return False

def check_and_mark_attendance(student_name, date):
    if check_attendance_exists(student_name, date):
        return "Already exists"
    
    current_time = datetime.now().time()
    
    # Define the time ranges for Present, Late, and Absent
    start_time_present = time(1, 20)
    end_time_present = time(1, 30)
    start_time_late = time(1, 30)
    end_time_late = time(2, 20)

    if start_time_present <= current_time <= end_time_present:
        attendance_status = 'Present'
    elif start_time_late <= current_time <= end_time_late:
        attendance_status = 'Late'
    else:
        attendance_status = 'Absent'

    insert_attendance(student_name, "Male", date, current_time.strftime("%H:%M:%S"), attendance_status)

    return attendance_status

if __name__ == '__main__':
    initialize()

    student_names = ['Keanghok', 'Dara', 'Sna']
    current_date = datetime.now().strftime("%Y-%m-%d")

    for student_name in student_names:
        status = check_and_mark_attendance(student_name, current_date)
        print(f"Student: {student_name}, Attendance Status: {status}")

    attendance_records = get_all_attendance()
    for record in attendance_records:
        print(record)
