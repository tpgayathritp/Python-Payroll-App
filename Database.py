import sqlite3
import os
from seed_employees import seed_employees

DB_NAME = "payroll.db"

def get_connection():
  #  return sqlite3.connect("C:\\Users\\gayathri\\Desktop\\Python\\Projects\\Payroll Calculator\\payroll.db")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "payroll.db")
    return sqlite3.connect(db_path)



def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            name TEXT,
            base_salary REAL,
            hours REAL,
            rate REAL,
            multiplier REAL,
            allowances REAL,
            deductions REAL
        )
    """)

    # Payroll run summary table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payroll_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_timestamp TEXT,
            total_employees INTEGER,
            total_gross REAL,
            total_net REAL
        )
    """)

    # Individual payslips table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payslips (
            slip_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            emp_id TEXT,
            base_salary REAL,
            overtime REAL,
            allowances REAL,
            deductions REAL,
            gross REAL,
            tax REAL,
            super REAL,
            net REAL,
            FOREIGN KEY(run_id) REFERENCES payroll_runs(run_id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")

init_db()
get_connection()
seed_employees()
