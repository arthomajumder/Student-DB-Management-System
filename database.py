"""
Student Database Management System - Database
SQLite database operations for CSV-based student records
Pass/Fail calculated based on GPA < 2.2
Detailed error messages for debugging
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Tuple
import config

DEFAULT_DB_PATH = config.DEFAULT_DB_PATH


@contextmanager
def get_db_connection(db_path: str = DEFAULT_DB_PATH):
    """Context manager for database connections."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Database Connection Error: Unable to connect to database '{db_path}'. Error details: {str(e)}")
    finally:
        if conn:
            conn.close()


def calculate_status(gpa: float) -> str:
    """Calculate PASS or FAIL based on GPA threshold."""
    try:
        gpa_val = float(gpa)
        return "FAIL" if gpa_val < config.PASS_FAIL_THRESHOLD else "PASS"
    except (ValueError, TypeError):
        return "FAIL"


def init_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initialize the student database and create table if not exists."""
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    age INTEGER,
                    email TEXT,
                    department TEXT,
                    gpa REAL,
                    graduation_year INTEGER,
                    status TEXT
                )
            """)
            conn.commit()
            print("[INFO] Database initialized successfully")
    except sqlite3.Error as e:
        raise RuntimeError(f"Database Initialization Error: Failed to create database table. Error: {str(e)}")


def add_student_record(
    student_id: str,
    name: str,
    age: int,
    email: str,
    department: str,
    gpa: float,
    graduation_year: int,
    db_path: str = DEFAULT_DB_PATH
) -> bool:
    """Add a new student record with calculated status."""
    
    if not student_id or not student_id.strip():
        raise ValueError("❌ Student ID is Empty: You must provide a Student ID. Student ID cannot be blank or contain only spaces.")
    if not name or not name.strip():
        raise ValueError("❌ Name is Empty: You must provide a Student Name. Name field cannot be blank or contain only spaces.")
    
    status = calculate_status(gpa)
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student 
                (student_id, name, age, email, department, gpa, graduation_year, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, name, age, email, department, gpa, graduation_year, status))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        raise ValueError(f"❌ Duplicate Student ID: Student ID '{student_id}' already exists in the database. Please use a unique Student ID.")
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ Database Insert Error: Failed to add student record. Details: {str(e)}")


def view_all_records(db_path: str = DEFAULT_DB_PATH) -> List[Tuple]:
    """Retrieve all student records from the database."""
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, student_id, name, age, email, department, gpa, 
                       graduation_year, status
                FROM student 
                ORDER BY name
            """)
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ Database Read Error: Failed to retrieve student records from database. Details: {str(e)}")


def search_by_student_id(student_id: str, db_path: str = DEFAULT_DB_PATH) -> Tuple:
    """Search for student by Student ID (exact match)."""
    if not student_id or not student_id.strip():
        raise ValueError("❌ Empty Search: You must enter a Student ID to search. Search field cannot be blank.")
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, student_id, name, age, email, department, gpa, 
                       graduation_year, status
                FROM student 
                WHERE student_id = ?
            """, (student_id,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"❌ Student Not Found: No student record found with ID '{student_id}'. Please verify the Student ID and try again.")
            return result
    except ValueError:
        raise
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ Database Search Error: Failed to search for student. Details: {str(e)}")


def update_record(
    record_id: int,
    student_id: str,
    name: str,
    age: int,
    email: str,
    department: str,
    gpa: float,
    graduation_year: int,
    db_path: str = DEFAULT_DB_PATH
) -> bool:
    """Update an existing student record."""
    
    if not student_id or not student_id.strip():
        raise ValueError("❌ Student ID is Empty: You must provide a Student ID. Student ID cannot be blank.")
    if not name or not name.strip():
        raise ValueError("❌ Name is Empty: You must provide a Student Name. Name field cannot be blank.")
    
    status = calculate_status(gpa)
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE student 
                SET student_id=?, name=?, age=?, email=?, department=?, 
                    gpa=?, graduation_year=?, status=?
                WHERE id=?
            """, (student_id, name, age, email, department, gpa, graduation_year, status, record_id))
            
            if cursor.rowcount == 0:
                raise ValueError(f"❌ Record Not Found: No student record found with ID {record_id}. The record may have been deleted.")
            
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ Database Update Error: Failed to update student record. Details: {str(e)}")


def delete_record(record_id: int, db_path: str = DEFAULT_DB_PATH) -> bool:
    """Delete a student record by ID."""
    if not isinstance(record_id, int) or record_id <= 0:
        raise ValueError("❌ Invalid Record ID: Record ID must be a positive number. The ID you provided is invalid.")
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student WHERE id = ?", (record_id,))
            
            if cursor.rowcount == 0:
                raise ValueError(f"❌ Record Not Found: No student record found with ID {record_id}. Cannot delete a non-existent record.")
            
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ Database Delete Error: Failed to delete student record. Details: {str(e)}")


def get_statistics(db_path: str = DEFAULT_DB_PATH) -> dict:
    """Get database statistics (Pass/Fail counts, etc)."""
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM student")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM student WHERE status='PASS'")
            pass_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM student WHERE status='FAIL'")
            fail_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(gpa) FROM student")
            avg_gpa = cursor.fetchone()[0] or 0.0
            
            return {
                'total': total,
                'pass': pass_count,
                'fail': fail_count,
                'avg_gpa': round(avg_gpa, 2)
            }
    except sqlite3.Error as e:
        raise RuntimeError(f"❌ Statistics Error: Failed to calculate statistics. Details: {str(e)}")


if __name__ == "__main__":
    try:
        init_database()
        print("Database initialized successfully")
    except RuntimeError as e:
        print(f"Error: {e}")