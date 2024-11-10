import sqlite3
from datetime import datetime
import os

DB_PATH = "attendance/student_attendance.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def create_table(db_name=DB_PATH):
    """Create attendance table if it doesn't already exist."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    student_name TEXT,
                    attendance_status TEXT)''')
    conn.commit()
    conn.close()

def record_attendance(student_name, db_name=DB_PATH):
    """Mark a student as 'Present' if not already marked for today."""
    today = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Check if the student is already marked present for today
    c.execute("SELECT * FROM attendance WHERE date = ? AND student_name = ?", (today, student_name))
    if not c.fetchone():  # Only insert if no record found for today
        c.execute("INSERT INTO attendance (date, student_name, attendance_status) VALUES (?, ?, ?)",
                  (today, student_name, "Present"))
        conn.commit()
        print(f"Attendance recorded for {student_name} on {today}")
    conn.close()

# Create the attendance table (run once to initialize the database)
create_table()
