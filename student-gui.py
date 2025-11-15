"""
Student Database Management System - GUI
Features:
- Search by Student ID only
- Add/Update/Delete with pop-ups
- Detailed error messages
- Age: any number allowed
- Graduation Year: YYYY format only

"""

from tkinter import *
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import database
import config
import csv
import re


class StudentApp:
    """Student Database Management System GUI Application."""
    
    def __init__(self, root):
        """Initialize the Student Management System GUI."""
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+0+0")
        self.root.config(bg=config.PRIMARY_COLOR)
        
        try:
            database.init_database()
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e))
            return
        
        self.selected_record = None
        self.db_id = None
        
        self._create_widgets()
        self._setup_layout()
        self._start_clock()
        
        self.display_all_records()
        self.update_statistics()
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        self.main_frame = Frame(self.root, bg=config.PRIMARY_COLOR)
        self._create_header()
        self._create_search_section()
        self._create_table_section()
        self._create_stats_section()
        self._create_bottom_section()
    
    def _create_header(self):
        """Create header with title and logout button"""
        self.header_frame = Frame(self.main_frame, bg=config.HEADER_COLOR, height=80)
        
        title_label = Label(
            self.header_frame,
            text=config.WINDOW_TITLE,
            font=config.TITLE_FONT,
            bg=config.HEADER_COLOR,
            fg="white"
        )
        title_label.pack(side=LEFT, expand=True, fill=BOTH, padx=20, pady=10)
        
        logout_btn = Button(
            self.header_frame,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="#FF6B6B",
            fg="white",
            padx=15,
            pady=5,
            command=self.exit_application
        )
        logout_btn.pack(side=RIGHT, padx=20, pady=10)
    
    def _create_search_section(self):
        """Create search section"""
        search_frame = LabelFrame(
            self.main_frame,
            text="Search Students",
            font=config.HEADER_FONT,
            bg=config.SECONDARY_COLOR,
            fg=config.HEADER_COLOR,
            padx=10,
            pady=10
        )
        
        search_label = Label(search_frame, text="Enter Student ID:", font=("Arial", 10, "bold"),
                            bg=config.SECONDARY_COLOR, fg=config.TEXT_COLOR)
        search_label.pack(side=LEFT, padx=5)
        
        self.search_term = StringVar()
        search_entry = Entry(search_frame, textvariable=self.search_term, width=25,
                            font=config.ENTRY_FONT, bg=config.LIST_BG)
        search_entry.pack(side=LEFT, padx=5)
        
        search_btn = Button(search_frame, text="Search", font=("Arial", 10, "bold"),
                           bg=config.ACCENT_COLOR, fg="white", command=self.search_student)
        search_btn.pack(side=LEFT, padx=5)
        
        clear_search_btn = Button(search_frame, text="Clear Search", font=("Arial", 10, "bold"),
                                 bg="#FFD700", fg="white", command=self.clear_search)
        clear_search_btn.pack(side=LEFT, padx=5)
        
        search_frame.pack(side=TOP, fill=X, padx=10, pady=5)
    
    def _create_table_section(self):
        """Create data table section"""
        table_frame = LabelFrame(
            self.main_frame,
            text="Student Records",
            font=config.HEADER_FONT,
            bg=config.SECONDARY_COLOR,
            fg=config.HEADER_COLOR,
            padx=5,
            pady=5
        )
        
        columns = ("student_id", "name", "age", "email", "department", "gpa", "year", "status")
        
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            height=5,
            show="headings"
        )
        
        headings = {
            "student_id": ("Student ID", 70),
            "name": ("Name", 100),
            "age": ("Age", 40),
            "email": ("Email", 120),
            "department": ("Department", 90),
            "gpa": ("GPA", 50),
            "year": ("Year", 50),
            "status": ("Status", 60)
        }
        
        for col, (heading, width) in headings.items():
            self.table.heading(col, text=heading)
            self.table.column(col, width=width)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=config.LIST_BG, fieldbackground=config.LIST_BG)
        style.configure("Treeview.Heading", background=config.ACCENT_COLOR, foreground="white")
        
        vsb = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.table.yview)
        hsb = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.table.xview)
        
        self.table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.table.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.table.bind('<ButtonRelease-1>', self.on_table_click)
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        button_frame = Frame(table_frame, bg=config.SECONDARY_COLOR)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=EW, padx=5, pady=5)
        
        import_btn = Button(button_frame, text="📥 IMPORT CSV", font=config.BUTTON_FONT,
                           bg=config.SUCCESS_COLOR, fg="white", command=self.import_csv)
        import_btn.pack(side=LEFT, padx=5)
        
        export_btn = Button(button_frame, text="📤 EXPORT CSV", font=config.BUTTON_FONT,
                           bg=config.SUCCESS_COLOR, fg="white", command=self.export_csv)
        export_btn.pack(side=LEFT, padx=5)
        
        table_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
    
    def _create_stats_section(self):
        """Create statistics section"""
        stats_frame = LabelFrame(
            self.main_frame,
            text="Statistics",
            font=config.HEADER_FONT,
            bg=config.SECONDARY_COLOR,
            fg=config.HEADER_COLOR,
            padx=15,
            pady=10
        )
        
        self.total_label = Label(stats_frame, text="Total: 0", font=("Arial", 10, "bold"),
                                bg=config.SECONDARY_COLOR, fg=config.TEXT_COLOR)
        self.total_label.pack(side=LEFT, padx=20)
        
        self.pass_label = Label(stats_frame, text="PASS: 0", font=("Arial", 10, "bold"),
                               bg=config.SECONDARY_COLOR, fg=config.PASS_COLOR)
        self.pass_label.pack(side=LEFT, padx=20)
        
        self.fail_label = Label(stats_frame, text="FAIL: 0", font=("Arial", 10, "bold"),
                               bg=config.SECONDARY_COLOR, fg=config.FAIL_COLOR)
        self.fail_label.pack(side=LEFT, padx=20)
        
        self.gpa_label = Label(stats_frame, text="Avg GPA: 0.0", font=("Arial", 10, "bold"),
                              bg=config.SECONDARY_COLOR, fg=config.ACCENT_COLOR)
        self.gpa_label.pack(side=LEFT, padx=20)
        
        stats_frame.pack(side=TOP, fill=X, padx=10, pady=5)
    
    def _create_bottom_section(self):
        """Create bottom section"""
        bottom_frame = Frame(self.main_frame, bg=config.PRIMARY_COLOR)
        
        info_frame = Frame(bottom_frame, bg=config.PRIMARY_COLOR)
        
        info_label = Label(info_frame, text="Clock: ", font=("Arial", 10),
                          bg=config.PRIMARY_COLOR, fg=config.TEXT_COLOR)
        info_label.pack(side=LEFT, padx=10)
        
        self.clock_label = Label(info_frame, text="00:00:00", font=("Arial", 10, "bold"),
                                bg=config.PRIMARY_COLOR, fg=config.ACCENT_COLOR)
        self.clock_label.pack(side=LEFT, padx=5)
        
        date_label = Label(info_frame, text="Date: ", font=("Arial", 10),
                          bg=config.PRIMARY_COLOR, fg=config.TEXT_COLOR)
        date_label.pack(side=LEFT, padx=10)
        
        self.date_label = Label(info_frame, text="", font=("Arial", 10, "bold"),
                               bg=config.PRIMARY_COLOR, fg=config.ACCENT_COLOR)
        self.date_label.pack(side=LEFT, padx=5)
        
        info_frame.pack(side=LEFT, expand=True, fill=X, padx=10, pady=10)
        
        bottom_frame.pack(side=BOTTOM, fill=X)
    
    def _setup_layout(self):
        """Arrange all frames"""
        self.main_frame.pack(fill=BOTH, expand=True)
        self.header_frame.pack(side=TOP, fill=X)
    
    def _start_clock(self):
        """Start updating clock and date"""
        self._update_clock()
    
    def _update_clock(self):
        """Update clock display"""
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%a %d/%m/%Y"))
        self.root.after(1000, self._update_clock)
    
    def on_table_click(self, event):
        """Store selected record info"""
        item = self.table.selection()
        if item:
            values = self.table.item(item, 'values')
            records = database.view_all_records()
            for record in records:
                if record[1] == values[0]:
                    self.db_id = record[0]
                    self.selected_record = record
                    break
    
    def search_student(self):
        """Search for student by Student ID"""
        search_term = self.search_term.get().strip()
        
        if not search_term:
            messagebox.showerror("Search Error", "❌ Empty Search Field: Please enter a Student ID to search. The search field cannot be empty.")
            return
        
        try:
            record = database.search_by_student_id(search_term)
            self._highlight_record(record)
            messagebox.showinfo("✅ Found", f"Student found: {record[2]}")
        except ValueError as e:
            messagebox.showerror("Search Error", str(e))
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e))
    
    def _highlight_record(self, record):
        """Highlight matching record in table"""
        for item in self.table.get_children():
            values = self.table.item(item, 'values')
            if values[0] == record[1]:
                self.table.selection_set(item)
                self.table.see(item)
                self.db_id = record[0]
                self.selected_record = record
                break
    
    def clear_search(self):
        """Clear search and reload all records"""
        self.search_term.set("")
        self.display_all_records()
    
    def display_all_records(self):
        """Display all records in table"""
        for item in self.table.get_children():
            self.table.delete(item)
        
        try:
            records = database.view_all_records()
            for row in records:
                self.table.insert("", END, values=(
                    row[1], row[2], row[3], row[4], row[5], 
                    f"{row[6]:.2f}", row[7], row[8]
                ))
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e))
    
    def update_statistics(self):
        """Update statistics display"""
        try:
            stats = database.get_statistics()
            self.total_label.config(text=f"Total: {stats['total']}")
            self.pass_label.config(text=f"PASS: {stats['pass']}")
            self.fail_label.config(text=f"FAIL: {stats['fail']}")
            self.gpa_label.config(text=f"Avg GPA: {stats['avg_gpa']}")
        except RuntimeError:
            pass
    
    def show_add_dialog(self):
        """Show Add Student dialog"""
        dialog = Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x400")
        dialog.config(bg=config.SECONDARY_COLOR)
        
        title_label = Label(dialog, text="Add New Student", font=config.HEADER_FONT,
                           bg=config.SECONDARY_COLOR, fg=config.HEADER_COLOR)
        title_label.pack(pady=10)
        
        fields = {}
        field_list = ["Student ID", "Name", "Age", "Email", "Department", "GPA", "Graduation Year"]
        
        for field in field_list:
            frame = Frame(dialog, bg=config.SECONDARY_COLOR)
            frame.pack(fill=X, padx=10, pady=5)
            
            label = Label(frame, text=field, font=config.LABEL_FONT,
                         bg=config.SECONDARY_COLOR, fg=config.TEXT_COLOR, width=15)
            label.pack(side=LEFT)
            
            if field == "Department":
                var = StringVar(value="Select Department")
                combo = ttk.Combobox(frame, textvariable=var, values=config.DEPARTMENTS,
                                    state="readonly", width=20)
                combo.pack(side=LEFT, padx=5)
                fields[field] = var
            else:
                entry = Entry(frame, font=config.ENTRY_FONT, width=25, bg=config.LIST_BG)
                entry.pack(side=LEFT, padx=5)
                fields[field] = entry
        
        btn_frame = Frame(dialog, bg=config.SECONDARY_COLOR)
        btn_frame.pack(pady=10)
        
        def save():
            try:
                if not fields["Student ID"].get().strip():
                    raise ValueError("❌ Student ID Required: Student ID field is empty. Please enter a unique Student ID.")
                if not fields["Name"].get().strip():
                    raise ValueError("❌ Name Required: Name field is empty. Please enter the student's full name.")
                if fields["Department"].get() == "Select Department":
                    raise ValueError("❌ Department Required: Please select a department from the dropdown menu.")
                
                try:
                    age = int(fields["Age"].get())
                except ValueError:
                    raise ValueError(f"❌ Age Invalid Format: Age must be a whole number. You entered '{fields['Age'].get()}'.")
                
                try:
                    gpa = float(fields["GPA"].get())
                    if gpa < config.MIN_GPA or gpa > config.MAX_GPA:
                        raise ValueError(f"❌ Invalid GPA: GPA must be between {config.MIN_GPA} and {config.MAX_GPA}. You entered {gpa}.")
                except ValueError as e:
                    if "Invalid GPA" in str(e):
                        raise
                    raise ValueError(f"❌ GPA Invalid Format: GPA must be a decimal number. You entered '{fields['GPA'].get()}'.")
                
                year_str = fields["Graduation Year"].get().strip()
                if not re.match(r'^\d{4}$', year_str):
                    raise ValueError(f"❌ Year Invalid Format: Graduation year must be in YYYY format (4 digits). You entered '{year_str}'.")
                year = int(year_str)
                
                database.add_student_record(
                    fields["Student ID"].get().strip(),
                    fields["Name"].get().strip(),
                    age,
                    fields["Email"].get().strip(),
                    fields["Department"].get(),
                    gpa,
                    year
                )
                messagebox.showinfo("✅ Success", "Student added successfully!")
                dialog.destroy()
                self.display_all_records()
                self.update_statistics()
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
            except RuntimeError as e:
                messagebox.showerror("Database Error", str(e))
        
        save_btn = Button(btn_frame, text="Save", font=config.BUTTON_FONT,
                         bg=config.ACCENT_COLOR, fg="white", width=15, command=save)
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = Button(btn_frame, text="Cancel", font=config.BUTTON_FONT,
                           bg="#FFD700", fg="white", width=15, command=dialog.destroy)
        cancel_btn.pack(side=LEFT, padx=5)
    
    def show_update_dialog(self):
        """Show Update Student dialog"""
        if not self.selected_record:
            messagebox.showwarning("Selection Error", "❌ No Student Selected: Please click on a student row in the table to select them before updating.")
            return
        
        dialog = Toplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("400x400")
        dialog.config(bg=config.SECONDARY_COLOR)
        
        title_label = Label(dialog, text="Update Student", font=config.HEADER_FONT,
                           bg=config.SECONDARY_COLOR, fg=config.HEADER_COLOR)
        title_label.pack(pady=10)
        
        fields = {}
        field_list = ["Student ID", "Name", "Age", "Email", "Department", "GPA", "Graduation Year"]
        values = [self.selected_record[1], self.selected_record[2], self.selected_record[3],
                 self.selected_record[4], self.selected_record[5], self.selected_record[6],
                 self.selected_record[7]]
        
        for i, field in enumerate(field_list):
            frame = Frame(dialog, bg=config.SECONDARY_COLOR)
            frame.pack(fill=X, padx=10, pady=5)
            
            label = Label(frame, text=field, font=config.LABEL_FONT,
                         bg=config.SECONDARY_COLOR, fg=config.TEXT_COLOR, width=15)
            label.pack(side=LEFT)
            
            if field == "Department":
                var = StringVar(value=values[i])
                combo = ttk.Combobox(frame, textvariable=var, values=config.DEPARTMENTS,
                                    state="readonly", width=20)
                combo.pack(side=LEFT, padx=5)
                fields[field] = var
            else:
                entry = Entry(frame, font=config.ENTRY_FONT, width=25, bg=config.LIST_BG)
                entry.insert(0, str(values[i]))
                entry.pack(side=LEFT, padx=5)
                fields[field] = entry
        
        btn_frame = Frame(dialog, bg=config.SECONDARY_COLOR)
        btn_frame.pack(pady=10)
        
        def update():
            try:
                if not fields["Student ID"].get().strip():
                    raise ValueError("❌ Student ID Required: Student ID field is empty. Please enter a Student ID.")
                if not fields["Name"].get().strip():
                    raise ValueError("❌ Name Required: Name field is empty. Please enter the student's name.")
                if fields["Department"].get() == "Select Department":
                    raise ValueError("❌ Department Required: Please select a department from the dropdown menu.")
                
                try:
                    age = int(fields["Age"].get())
                except ValueError:
                    raise ValueError(f"❌ Age Invalid Format: Age must be a whole number. You entered '{fields['Age'].get()}'.")
                
                try:
                    gpa = float(fields["GPA"].get())
                    if gpa < config.MIN_GPA or gpa > config.MAX_GPA:
                        raise ValueError(f"❌ Invalid GPA: GPA must be between {config.MIN_GPA} and {config.MAX_GPA}. You entered {gpa}.")
                except ValueError as e:
                    if "Invalid GPA" in str(e):
                        raise
                    raise ValueError(f"❌ GPA Invalid Format: GPA must be a decimal number. You entered '{fields['GPA'].get()}'.")
                
                year_str = fields["Graduation Year"].get().strip()
                if not re.match(r'^\d{4}$', year_str):
                    raise ValueError(f"❌ Year Invalid Format: Graduation year must be in YYYY format (4 digits). You entered '{year_str}'.")
                year = int(year_str)
                
                database.update_record(
                    self.db_id,
                    fields["Student ID"].get().strip(),
                    fields["Name"].get().strip(),
                    age,
                    fields["Email"].get().strip(),
                    fields["Department"].get(),
                    gpa,
                    year
                )
                messagebox.showinfo("✅ Success", "Student updated successfully!")
                dialog.destroy()
                self.display_all_records()
                self.update_statistics()
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
            except RuntimeError as e:
                messagebox.showerror("Database Error", str(e))
        
        save_btn = Button(btn_frame, text="Update", font=config.BUTTON_FONT,
                         bg=config.SUCCESS_COLOR, fg="white", width=15, command=update)
        save_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = Button(btn_frame, text="Cancel", font=config.BUTTON_FONT,
                           bg="#FFD700", fg="white", width=15, command=dialog.destroy)
        cancel_btn.pack(side=LEFT, padx=5)
    
    def show_delete_dialog(self):
        """Show Delete Student dialog"""
        if not self.selected_record:
            messagebox.showwarning("Selection Error", "❌ No Student Selected: Please click on a student row in the table to select them before deleting.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete",
            f"Delete student: {self.selected_record[2]}?\n\nThis action CANNOT be undone and will permanently remove this student from the database.")
        
        if confirm:
            try:
                database.delete_record(self.db_id)
                messagebox.showinfo("✅ Success", "Student deleted successfully!")
                self.display_all_records()
                self.update_statistics()
            except Exception as e:
                messagebox.showerror("Delete Error", str(e))
    
    def import_csv(self):
        """Import CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file to import",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                if not csv_reader.fieldnames:
                    messagebox.showerror("CSV Error", "❌ Empty CSV File: The selected CSV file is empty or has no header row. Please select a valid CSV file with data.")
                    return
                
                imported = 0
                skipped = 0
                
                for row in csv_reader:
                    try:
                        database.add_student_record(
                            row.get('StudentID', '').strip(),
                            row.get('Name', '').strip(),
                            int(row.get('Age', 0)),
                            row.get('Email', '').strip(),
                            row.get('Department', '').strip(),
                            float(row.get('GPA', 0)),
                            int(row.get('GraduationYear', 0))
                        )
                        imported += 1
                    except (ValueError, KeyError):
                        skipped += 1
                        continue
                
                self.display_all_records()
                self.update_statistics()
                messagebox.showinfo("✅ Import Complete", f"Successfully imported {imported} students\nSkipped {skipped} invalid rows")
        except Exception as e:
            messagebox.showerror("Import Error", f"❌ Failed to import CSV: {str(e)}")
    
    def export_csv(self):
        """Export to CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if not file_path:
            return
        
        try:
            records = database.view_all_records()
            
            if not records:
                messagebox.showwarning("No Data", "❌ No Records to Export: The database is empty. Please add some student records before exporting.")
                return
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['StudentID', 'Name', 'Age', 'Email', 'Department', 'GPA', 'GraduationYear', 'Status']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                writer.writeheader()
                for record in records:
                    writer.writerow({
                        'StudentID': record[1],
                        'Name': record[2],
                        'Age': record[3],
                        'Email': record[4],
                        'Department': record[5],
                        'GPA': record[6],
                        'GraduationYear': record[7],
                        'Status': record[8]
                    })
            
            messagebox.showinfo("✅ Export Success", f"Data exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"❌ Failed to export CSV: {str(e)}")
    
    def exit_application(self):
        """Exit application"""
        confirm = messagebox.askyesno("Exit Application", "Are you sure you want to exit the Student Database Management System?")
        if confirm:
            self.root.destroy()


def show_context_menu(app, event):
    """Show context menu on right-click"""
    item = app.table.selection()
    if not item:
        messagebox.showinfo("Selection Required", "❌ No Row Selected: Right-click on a student row to open the context menu.")
        return
    
    values = app.table.item(item, 'values')
    records = database.view_all_records()
    for record in records:
        if record[1] == values[0]:
            app.db_id = record[0]
            app.selected_record = record
            break
    
    menu = Toplevel(app.root)
    menu.wm_overrideredirect(True)
    menu.wm_geometry(f"+{event.x_root}+{event.y_root}")
    
    add_btn = Button(menu, text="Add New", width=20, command=app.show_add_dialog)
    add_btn.pack()
    
    update_btn = Button(menu, text="Update Selected", width=20, command=app.show_update_dialog)
    update_btn.pack()
    
    delete_btn = Button(menu, text="Delete Selected", width=20, command=app.show_delete_dialog)
    delete_btn.pack()


if __name__ == "__main__":
    root = Tk()
    app = StudentApp(root)
    
    app.table.bind("<Button-3>", lambda e: show_context_menu(app, e))
    
    root.mainloop()