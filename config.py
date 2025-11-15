

# ============================================================================
# WINDOW CONFIGURATION
# ============================================================================
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Student Database Management System"

# ============================================================================
# COLORS - THEME
# ============================================================================
PRIMARY_COLOR = "#B0E0E6"          # Powder Blue (main background)
SECONDARY_COLOR = "#E0F6FF"        # Light Cyan (form background)
ACCENT_COLOR = "#4682B4"           # Steel Blue (buttons)
SUCCESS_COLOR = "#87CEEB"          # Sky Blue
ERROR_COLOR = "#FF6B6B"            # Light Red (errors)
PASS_COLOR = "#90EE90"             # Light Green (PASS)
FAIL_COLOR = "#FF6B6B"             # Light Red (FAIL)
HEADER_COLOR = "#1E90FF"           # Dodger Blue (header)
TEXT_COLOR = "#000000"             # Black text
LIST_BG = "#F0F8FF"                # Alice Blue (lists)

# ============================================================================
# FONTS
# ============================================================================
TITLE_FONT = ("Arial", 32, "bold")
LABEL_FONT = ("Arial", 11, "bold")
ENTRY_FONT = ("Arial", 10)
BUTTON_FONT = ("Arial", 11, "bold")
LIST_FONT = ("Arial", 9, "bold")
HEADER_FONT = ("Arial", 14, "bold")

# ============================================================================
# DATABASE
# ============================================================================
DEFAULT_DB_PATH = "students.db"

# ============================================================================
# CSV COLUMNS
# ============================================================================
CSV_COLUMNS = ["StudentID", "Name", "Age", "Email", "Department", "GPA", "GraduationYear"]

# ============================================================================
# DEPARTMENTS
# ============================================================================
DEPARTMENTS = ["Mathematics", "Chemistry", "Physics", "Computer Science", "Biology"]

# ============================================================================
# PASS/FAIL THRESHOLD
# ============================================================================
PASS_FAIL_THRESHOLD = 2.2  # GPA < 2.2 is FAIL

# ============================================================================
# VALIDATION CONSTRAINTS
# ============================================================================
MIN_GPA = 0.0
MAX_GPA = 4.0