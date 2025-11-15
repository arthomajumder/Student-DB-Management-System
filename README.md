# Student-DB-Management-System
A Student Database Management System built with Python Tkinter GUI and SQLite database. Features include student record management, CSV import/export, automatic pass/fail calculation, and comprehensive error handling.

---

## 🚀 Quick Start

### Installation

1. **Download all 3 files:**
   - `config.py`
   - `database.py`
   - `student_gui.py` (rename from `student-gui.py` if needed)

2. **Save in the same folder**

3. **Run the application:**
   ```bash
   python student_gui.py
   ```

### Requirements

- Python 3.x
- Tkinter (included with Python)
- SQLite3 (included with Python)

No additional packages needed!

---

## 🔧 Troubleshooting

### Application Won't Start
- Ensure Python 3.x is installed
- Check all 3 files are in the same folder
- Run: `python student_gui.py`

### Database Errors
- Delete `students.db` to reset
- Application will recreate it
- All data will be lost

### Import Fails
- Verify CSV has correct columns
- Check encoding is UTF-8
- Ensure valid data types

### GUI Issues
- Ensure Tkinter is installed
- On Linux: `sudo apt-get install python3-tk`
- On Mac: Included with Python

---

## 📚 Technologies Used

- **GUI:** Python Tkinter
- **Database:** SQLite3
- **Data Format:** CSV
- **Language:** Python 3.x

---

## 📁 File Structure

### 1. `config.py` - Configuration
All settings and constants in one place.

**Includes:**
- Window dimensions: 1400x800
- Color scheme (light blue theme):
  - Primary: #B0E0E6 (Powder Blue)
  - Secondary: #E0F6FF (Light Cyan)
  - Accent: #4682B4 (Steel Blue)
- Font definitions
- Database path: `students.db`
- Departments: Mathematics, Chemistry, Physics, Computer Science, Biology
- Pass/Fail threshold: 2.2 (GPA < 2.2 = FAIL)
- GPA validation: 0.0 - 4.0

### 2. `database.py` - Backend Operations
SQLite database management with all CRUD operations.

**Functions:**
- `init_database()` - Creates database table
- `add_student_record()` - Adds new student
- `view_all_records()` - Retrieves all students
- `search_by_student_id()` - Searches by ID
- `update_record()` - Updates student data
- `delete_record()` - Deletes student
- `get_statistics()` - Calculates statistics
- `calculate_status()` - Auto PASS/FAIL based on GPA

**Error Handling:**
- Detailed error messages with ❌ emoji
- Explains WHY each error occurred
- Provides actionable guidance

### 3. `student_gui.py` - User Interface
Professional Tkinter GUI with all functionality.

**Features:**
- Search by Student ID
- Add/Update/Delete via pop-up dialogs
- Right-click context menu
- Import/Export CSV
- Real-time statistics
- Clock and date display
- Light blue professional theme

---

## 📊 Database Schema

### Table: `student`

```sql
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
```

**Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique auto-incrementing ID |
| `student_id` | TEXT | Unique Student ID (from CSV) |
| `name` | TEXT | Student full name |
| `age` | INTEGER | Student age (any number) |
| `email` | TEXT | Email address |
| `department` | TEXT | Department name |
| `gpa` | REAL | Grade Point Average (0.0-4.0) |
| `graduation_year` | INTEGER | Graduation year (YYYY format) |
| `status` | TEXT | PASS or FAIL (auto-calculated) |

---

## 🔍 SQL Queries Used

### 1. Create Table
```sql
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
```

### 2. Insert Record
```sql
INSERT INTO student 
(student_id, name, age, email, department, gpa, graduation_year, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
```

### 3. Select All Records (Ordered by Name)
```sql
SELECT id, student_id, name, age, email, department, gpa, 
       graduation_year, status
FROM student 
ORDER BY name
```

### 4. Search by Student ID
```sql
SELECT id, student_id, name, age, email, department, gpa, 
       graduation_year, status
FROM student 
WHERE student_id = ?
```

### 5. Update Record
```sql
UPDATE student 
SET student_id=?, name=?, age=?, email=?, department=?, 
    gpa=?, graduation_year=?, status=?
WHERE id=?
```

### 6. Delete Record
```sql
DELETE FROM student WHERE id = ?
```

### 7. Count Total Records
```sql
SELECT COUNT(*) FROM student
```

### 8. Count PASS Records
```sql
SELECT COUNT(*) FROM student WHERE status='PASS'
```

### 9. Count FAIL Records
```sql
SELECT COUNT(*) FROM student WHERE status='FAIL'
```

### 10. Calculate Average GPA
```sql
SELECT AVG(gpa) FROM student
```

---

## 💾 CSV Format

### Import CSV Structure
Your CSV file should have these columns:

```
StudentID,Name,Age,Email,Department,GPA,GraduationYear
5446,Christine Smith,21,nicholasmeja@hotmail.com,Computer Science,3.43,2027
9985,Christopher Henry,19,steeleJohn@nguyen.com,Chemistry,3.07,2030
```

### Export CSV Structure
When exporting, includes an additional `Status` column:

```
StudentID,Name,Age,Email,Department,GPA,GraduationYear,Status
5446,Christine Smith,21,nicholasmeja@hotmail.com,Computer Science,3.43,2027,PASS
9985,Christopher Henry,19,steeleJohn@nguyen.com,Chemistry,3.07,2030,PASS
```

---

## ✨ Features & Functionality

### 🔍 Search
- **Search by Student ID** only
- Exact match search
- Highlights matching record in table
- Shows success/error message

### ➕ Add Student
Pop-up dialog with fields:
- Student ID (required, unique)
- Name (required)
- Age (any integer)
- Email
- Department (dropdown selector)
- GPA (0.0-4.0 validation)
- Graduation Year (YYYY format only)
- Status (auto-calculated)

### ✏️ Update Student
- Right-click table row or select and click Update
- Pre-populated with current values
- All fields editable
- GPA re-validated
- Status auto-recalculated

### 🗑️ Delete Student
- Right-click table row or select and click Delete
- Confirmation dialog prevents accidental deletion
- Cannot be undone

### 📥 Import CSV
- Select CSV file
- Validates header row
- Imports all valid records
- Shows count of imported/skipped records

### 📤 Export CSV
- Save all records to CSV
- Includes PASS/FAIL status
- Timestamp in filename
- Prevents export if no records exist

### 📊 Statistics
Real-time display showing:
- **Total:** Total number of students
- **PASS:** Count of passing students (GPA >= 2.2)
- **FAIL:** Count of failing students (GPA < 2.2)
- **Avg GPA:** Average GPA of all students

---

## ✅ Validation Rules

### Field Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| Student ID | Must not be empty | ❌ Student ID is Empty |
| Student ID | Must be unique | ❌ Duplicate Student ID |
| Name | Must not be empty | ❌ Name is Empty |
| Age | Must be integer | ❌ Age Invalid Format |
| Email | No validation | - |
| Department | Must select from list | ❌ Department Required |
| GPA | 0.0-4.0 range | ❌ Invalid GPA |
| GPA | Must be decimal | ❌ GPA Invalid Format |
| Year | YYYY format (4 digits) | ❌ Year Invalid Format |

### Pass/Fail Calculation

```
IF GPA < 2.2 THEN Status = "FAIL"
ELSE Status = "PASS"
```

---

## 🎨 UI Components

### Header
- Application title
- Logout button (exit)

### Search Section
- Student ID input field
- Search button
- Clear Search button

### Student Records Table
- Columns: Student ID, Name, Age, Email, Department, GPA, Year, Status
- Scrollable (horizontal & vertical)
- Click row to select
- Right-click for context menu

### Statistics Panel
- Total count
- PASS count (green)
- FAIL count (red)
- Average GPA

### Action Buttons
- IMPORT CSV
- EXPORT CSV

### Bottom Section
- Real-time clock (HH:MM:SS)
- Current date (Day DD/MM/YYYY)

### Context Menu (Right-Click)
- Add New
- Update Selected
- Delete Selected

---

## 🛡️ Error Handling

All errors include:
- ❌ Icon for visibility
- Clear error type
- Reason WHY it's an error
- Suggested action

### Error Examples

```
❌ Student ID is Empty: You must provide a Student ID. 
Student ID cannot be blank or contain only spaces.

❌ Duplicate Student ID: Student ID '5446' already exists 
in the database. Please use a unique Student ID.

❌ Year Invalid Format: Graduation year must be in YYYY 
format (4 digits). You entered '25'.

❌ Student Not Found: No student record found with ID '9999'. 
Please verify the Student ID and try again.
```

---

## 📝 Color Scheme

| Element | Color | Hex Code |
|---------|-------|----------|
| Primary Background | Powder Blue | #B0E0E6 |
| Forms/Secondary | Light Cyan | #E0F6FF |
| Buttons/Accent | Steel Blue | #4682B4 |
| Success Actions | Sky Blue | #87CEEB |
| PASS Status | Light Green | #90EE90 |
| FAIL Status | Light Red | #FF6B6B |
| Header | Dodger Blue | #1E90FF |
| Text | Black | #000000 |
| Lists | Alice Blue | #F0F8FF |

---

## 📋 CSV Import/Export

### How to Import
1. Click **📥 IMPORT CSV** button
2. Select your CSV file
3. File must have these columns:
   - StudentID
   - Name
   - Age
   - Email
   - Department
   - GPA
   - GraduationYear
4. System imports valid records
5. Shows count of imported/skipped

### How to Export
1. Click **📤 EXPORT CSV** button
2. Choose save location
3. Filename: `students_YYYYMMDD_HHMMSS.csv`
4. Includes all records with PASS/FAIL status

---

## 🎯 Use Cases

✅ School/University student management  
✅ Training center enrollment tracking  
✅ Employee database management  
✅ Batch processing CSV data  
✅ Academic performance tracking  
✅ Learning projects for Python/GUI development  

---

## 📄 License

This project is open source and free to use.

---

## 💬 Support

For issues or questions:
1. Check error message details
2. Review validation rules
3. Verify CSV format
4. Check database file exists

---

## ✨ Version

**Version 1.0**
- Search by Student ID
- Add/Update/Delete operations
- CSV Import/Export
- Auto Pass/Fail calculation
- Detailed error messages
- Light blue professional theme

**Last Updated:** November 16, 2025

---

## 📊 Project Summary

| Aspect | Details |
|--------|---------|
| **Files** | 3 Python files (config, database, GUI) |
| **Database** | SQLite with 9 fields |
| **Records** | Unlimited student records |
| **Search** | By Student ID |
| **Operations** | Add, Update, Delete, Import, Export |
| **Validation** | 8+ field validation rules |
| **Theme** | Light blue professional |
| **UI Components** | 10+ interactive elements |
| **Error Messages** | 20+ detailed error scenarios |
| **SQL Queries** | 10 core database queries |

---

**Enjoy your Student Database Management System!**
