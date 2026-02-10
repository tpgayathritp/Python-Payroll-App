import os
import csv
import logging
from datetime import datetime
from fpdf import FPDF
from Database import get_connection, init_db
from seed_employees import seed_employees

# Initialize DB
init_db()

# Seed employees
conn = get_connection()
seed_employees(conn)


# -----------------------------
# Log files
# -----------------------------

payrun_timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
payrun_date = datetime.now().strftime("%Y-%m-%d")


#if not os.path.exists("logs"):
 #   os.makedirs("logs")

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

info_logfile = os.path.join(LOG_DIR, f"payroll_{payrun_date}_info.log")
error_logfile = os.path.join(LOG_DIR, f"payroll_{payrun_date}_error.log")
#info_logfile = f"logs/payroll_{payrun_date}_info.log"
#error_logfile = f"logs/payroll_{payrun_date}_error.log"

logger = logging.getLogger("payroll")
logger.setLevel(logging.INFO)

payroll_info = logging.FileHandler(info_logfile)
payroll_info.setLevel(logging.INFO)

payroll_error = logging.FileHandler(error_logfile)
payroll_error.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
payroll_info.setFormatter(formatter)
payroll_error.setFormatter(formatter)

logger.addHandler(payroll_info)
logger.addHandler(payroll_error)

#-----------------
#--- Database setup--
#-----------------


def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT emp_id, name, base_salary, hours, rate, multiplier, allowances, deductions
        FROM employees
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows


def save_payroll_run(total_employees, total_gross, total_net, timestamp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payroll_runs (run_timestamp, total_employees, total_gross, total_net)
        VALUES (?, ?, ?, ?)
    """, (timestamp, total_employees, total_gross, total_net))

    conn.commit()
    run_id = cursor.lastrowid
    conn.close()
    return run_id


def save_payslip(run_id, emp_id, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payslips (
            run_id, emp_id,
            base_salary, overtime, allowances, deductions,
            gross, tax, super, net
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        emp_id,
        result["base_salary"],
        result["overtime"],
        result["allowances"],
        result["deductions"],
        result["gross"],
        result["tax"],
        result["super"],
        result["net"],
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Output files
# -----------------------------
#if not os.path.exists("payslips"):
  #  os.makedirs("payslips")

PAYSLIPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "payslips")
if not os.path.exists(PAYSLIPS_DIR):
    os.makedirs(PAYSLIPS_DIR)
    
def generate_payslip_pdf(emp_id, name, result, payrun_timestamp):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 16)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 12, "Employee Payslip", ln=True, align="C", fill=True)
    pdf.ln(5)


    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Employee Details", ln=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(90, 8, f"Employee ID: {emp_id}", ln=False)
    pdf.cell(90, 8, f"Name: {name}", ln=True)
    pdf.ln(3)


    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Earnings", ln=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(90, 8, f"Basic Salary: {result['base_salary']}", ln=False)
    pdf.cell(90, 8, f"Overtime: {result['overtime']}", ln=True)
    pdf.cell(90, 8, f"Allowances: {result['allowances']}", ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Deductions", ln=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(90, 8, f"Deductions: {result['deductions']}", ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Summary", ln=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(90, 8, f"Gross Salary: {result['gross']}", ln=False)
    pdf.cell(90, 8, f"Tax: {result['tax']}", ln=True)
    pdf.cell(90, 8, f"Super: {result['super']}", ln=False)
    pdf.cell(90, 8, f"Net Salary: {result['net']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, f"Pay run: {payrun_timestamp}", ln=True, align="C")
    pdf.cell(0, 8, "This is a system-generated payslip.", ln=True, align="C")

    #filename = f"payslips/payslip_{emp_id}.pdf"
    filename = os.path.join(PAYSLIPS_DIR, f"payslip_{emp_id}.pdf")
    pdf.output(filename)
    logger.info(f"Generated payslip PDF: {filename}")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_summary_csv(summary_rows, payrun_timestamp):
   # filename = f"output/payroll_summary_{payrun_timestamp.replace(':', '').replace(' ', '_')}.csv"
    filename = os.path.join(OUTPUT_DIR, f"payroll_summary_{payrun_timestamp.replace(':', '').replace(' ', '_')}.csv")
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Emp ID", "Name",
            "Base Salary", "Hours", "Rate", "Multiplier",
            "Allowances", "Deductions",
            "Overtime", "Gross", "Tax", "Super", "Net"
        ])
        writer.writerows(summary_rows)

    logger.info(f"Generated summary CSV: {filename}")


# -----------------------------
# Payroll logic
# -----------------------------

def calculate_tax(gross):
    if gross <= 18200:
        return 0
    elif gross <= 45000:
        return (gross - 18200) * 0.19
    elif gross <= 120000:
        return 5092 + (gross - 45000) * 0.325
    elif gross <= 180000:
        return 29467 + (gross - 120000) * 0.37
    else:
        return 51667 + (gross - 180000) * 0.45

def calculate_payroll_for_employee(emp_row):
    emp_id, name, base_salary, hours, rate, multiplier, allowances, deductions = emp_row
# unpakcing
    overtime = hours * rate * multiplier
    gross = base_salary + overtime + allowances
    tax = calculate_tax(gross)
    super_amt = gross * 0.095
    net = gross - tax - deductions

    result = {
        "base_salary": base_salary,
        "hours": hours,
        "rate": rate,
        "multiplier": multiplier,
        "allowances": allowances,
        "deductions": deductions,
        "overtime": overtime,
        "gross": gross,
        "tax": tax,
        "super": super_amt,
        "net": net,
    }

    return emp_id, name, result

def run_payroll():
    logger.info("Starting payroll run")

    init_db() 

    employees = get_all_employees()
    if not employees:
        logger.warning("No employees found in database. Payroll run aborted.")
        print("No employees found in database.")
        return

    summary_rows = []
    total_gross = 0.0
    total_net = 0.0

    
    calculated_results = []

    for emp in employees:
        emp_id, name, result = calculate_payroll_for_employee(emp)

        calculated_results.append((emp_id, name, result))

        summary_rows.append([
            emp_id,
            name,
            result["base_salary"],
            result["hours"],
            result["rate"],
            result["multiplier"],
            result["allowances"],
            result["deductions"],
            result["overtime"],
            result["gross"],
            result["tax"],
            result["super"],
            result["net"],
        ])

        total_gross += result["gross"]
        total_net += result["net"]

        logger.info(f"Processed employee {emp_id} - Net: {result['net']:.2f}")

    
    run_id = save_payroll_run(
        total_employees=len(employees),
        total_gross=total_gross,
        total_net=total_net,
        timestamp=payrun_timestamp,
    )
    logger.info(f"Saved payroll run {run_id} - Employees: {len(employees)}, Total Net: {total_net:.2f}")

    
    for emp_id, name, result in calculated_results:
        generate_payslip_pdf(emp_id, name, result, payrun_timestamp)
        save_payslip(run_id, emp_id, result)

    generate_summary_csv(summary_rows, payrun_timestamp)

    logger.info("Payroll run completed")
    print("Payroll run completed successfully.")



if __name__ == "__main__":
    try:
        run_payroll()
    except Exception as e:
        logger.exception(f"Unhandled error in payroll run: {e}")
        print("ERROR:", e)
       # which line which function the exact error on console
        import traceback
        traceback.print_exc() 
        raise

