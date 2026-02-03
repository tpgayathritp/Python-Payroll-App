import tkinter as tk
from tkinter import ttk, messagebox

from Payroll_from_db import run_payroll
from Database import get_connection


# -----------------------------
# Run Payroll Button Action
# -----------------------------
def run_payroll_gui():
    try:
        run_payroll()
        messagebox.showinfo("Success", "Payroll run completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Payroll failed:\n{e}")


# -----------------------------
# View Employees Window
# -----------------------------
def show_employees():
    win = tk.Toplevel(root)
    win.title("Employees")
    win.geometry("800x400")

    columns = ("ID", "Name", "Base Salary", "Hours", "Rate", "Multiplier", "Allowances", "Deductions")

    tree = ttk.Treeview(win, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("Payroll System")
root.geometry("300x200")

title_label = ttk.Label(root, text="Payroll System", font=("Arial", 16))
title_label.pack(pady=10)

run_button = ttk.Button(root, text="Run Payroll", command=run_payroll_gui)
run_button.pack(pady=10)

view_button = ttk.Button(root, text="View Employees", command=show_employees)
view_button.pack(pady=10)

exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

root.mainloop()