import os
import logging
from fpdf import FPDF
import csv
from datetime import datetime

payrun_timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
payrun_date = datetime.now().strftime("%Y-%m-%d")


if not os.path.exists("logs"):
    os.makedirs("logs")

info_logfile = f"logs/payroll_{payrun_date}_info.log"
error_logfile = f"logs/payroll_{payrun_date}_error.log"

logger = logging.getLogger("PayrollLogger")
logger.setLevel(logging.DEBUG)   

info_handler = logging.FileHandler(info_logfile)
info_handler.setLevel(logging.DEBUG)  
info_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
info_handler.setFormatter(info_format)

error_handler = logging.FileHandler(error_logfile)
error_handler.setLevel(logging.ERROR)  
error_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_format)

logger.addHandler(info_handler)
logger.addHandler(error_handler)


if not os.path.exists("payslips"):
    os.makedirs("payslips")



def export_to_pdf(Emp_id, Emp_name, base_salary, overtime, allowances, deductions, result):
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

    pdf.cell(90, 8, f"Employee ID: {Emp_id}", ln=False)
    pdf.cell(90, 8, f"Name: {Emp_name}", ln=True)
    pdf.ln(3)


    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Earnings", ln=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(90, 8, f"Basic Salary: {base_salary}", ln=False)
    pdf.cell(90, 8, f"Overtime: {overtime}", ln=True)
    pdf.cell(90, 8, f"Allowances: {allowances}", ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Deductions", ln=True)
    pdf.set_font("Arial", size=11)

    pdf.cell(90, 8, f"Deductions: {deductions}", ln=True)
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

    filename = f"payslips/payslip_{Emp_id}.pdf"
    pdf.output(filename)

    print(f"PDF payslip created: {filename}")


def write_master_summary(summary_row):

    filename = "master_payroll_summary.csv"
    header1 = ["Timestamp: " + payrun_timestamp]
    header = ["Employee ID","Employee Name","Basic Salary","Overtime","Allowances",
              "Deductions","Gross Salary","Tax","Super","Net Salary"]
    
    # Calculate totals
    total_basic = sum(row[2] for row in summary_row)
    total_overtime = sum(row[3] for row in summary_row)
    total_allowances = sum(row[4] for row in summary_row)
    total_deductions = sum(row[5] for row in summary_row)
    total_gross = sum(row[6] for row in summary_row)
    total_tax = sum(row[7] for row in summary_row)
    total_super = sum(row[8] for row in summary_row)
    total_net = sum(row[9] for row in summary_row)

    totals_row = [
        "", "TOTAL", total_basic, total_overtime, total_allowances,
        total_deductions, total_gross, total_tax, total_super, total_net]
       
    with open(filename,"w",newline="") as file:
        writer=csv.writer(file)
        writer.writerow(header1)
        writer.writerow(header)
        writer.writerows(summary_row)
        writer.writerow([])  
        writer.writerow(totals_row)


    print(f"Summary file created")

def export_to_csv(Emp_id,Emp_name,base_salary,overtime,allowances,deductions,result):
    header1 = ["Timestamp: " + payrun_timestamp]
    header = ["Employee ID","Employee Name","Basic Salary","Overtime","Allowances",
              "Deductions","Gross Salary","Tax","Super","Net Salary"]
    row = [Emp_id,Emp_name,base_salary,overtime,allowances,deductions,
           result["gross"],result['tax'],result['super'],result['net']]
    
    filename = f"payslip_{Emp_id}.csv"

    #try:
    with open(filename,"w",newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header1)
            writer.writerow(header)
            writer.writerow(row)
    #except FileExistsError:
    #    with open(filename,"a",newline="") as file:
    #        writer = csv.writer(file)
    #        writer.writerow(row)

def calculate_tax(gross_salary):
    if gross_salary <= 18200:
        return 0
    elif gross_salary <= 45000:
        return (gross_salary - 18200) * 0.19
    elif gross_salary <= 120000:
        return 5092 + (gross_salary - 45000) * 0.325
    elif gross_salary <= 180000:
        return 29467 + (gross_salary - 120000) * 0.37
    else:
        return 51667 + (gross_salary - 180000) * 0.45


def overtime_calc(hours , rate, multiplier=1.5):
    return hours*rate*multiplier

def calculate_pay(base_salary, allowances,deductions,overtime, super_rate=0.11):
    gross_salary = base_salary + overtime + allowances 
    tax = calculate_tax(gross_salary)
    super_amount = gross_salary * super_rate
    net_salary = gross_salary - tax - super_amount - deductions
    return {
        "gross": gross_salary,
        "tax": tax,
        "super": super_amount,
        "net": net_salary
    }

# Program starts here
def batch_payroll(datafile):
    
    summary_row =[]

    try:
        logger.info(f"Opening data file: {datafile}")

        with open(datafile,"r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                Emp_id = row["Employee ID"]
                Emp_name = row["Employee Name"]

                logger.info(f"Processing employee {Emp_id} - {Emp_name}")
                
                try:

                    base_salary = float(row["Basic Salary"])
                    hours = float(row["hours"])
                    rate = float(row["rate"])
                    multiplier = float(row["multiplier"])
                    allowances = float(row["Allowances"])
                    deductions = float(row["Deductions"])
                 
                except ValueError as e:
                    logger.error(f"Invalid numeric value for {Emp_id}: {e}")
                    continue


                overtime= overtime_calc(hours,rate,multiplier)
                logging.debug(f"Overtime for {Emp_id}: {overtime}")
                result = calculate_pay(base_salary,allowances,deductions,overtime)
        
                export_to_csv(Emp_id,Emp_name,base_salary,overtime,allowances,deductions,result)
                export_to_pdf(Emp_id,Emp_name,base_salary,overtime,allowances,deductions,result)


                summary_row.append([Emp_id,
                                   Emp_name,
                                   base_salary,
                                   overtime,
                                   allowances,
                                   deductions,
                                   result["gross"],
                                   result["tax"],
                                   result["super"],
                                   result["net"]])
        
                logging.info(f"Completed payroll for {Emp_id}")

        logging.info(f"Completed Batch Processing")

        
        write_master_summary(summary_row)
        logging.info("Master summary created successfully.")
        logging.info("Payroll run completed.")


    except FileNotFoundError:
        logging.error("CSV File not found.\n")
    except KeyError as e:
        logging.error(f"Missing column in CSV: {e}")
    except ValueError as e:
        logging.critical(f"Unexpected system error: {e}")


batch_payroll("datafile.csv")