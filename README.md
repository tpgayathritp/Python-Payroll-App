A payroll application built with Python, designed to automate payroll calculations and generate reports.

A Python‑based payroll system that calculates employee salaries, overtime, and tax, and stores all payroll history in an SQLite database. The project includes a Tkinter GUI for local use and CI/CD pipelines in Jenkins and Azure DevOps for automated execution and artifact generation.

Features
-------------------------------------
Tkinter GUI for easy interaction
SQLite database for employee and payroll data
Payroll engine calculating:
Base salary
Overtime
Allowances
Deductions
Tax
Superannuation
Net pay
Automatic PDF payslip generation
CSV/Excel summary report generation
Logging and error handling
Modular, maintainable code structure

Technical
---------------------------------------
- Python 3
- SQLite
- Tkinter
- Jenkins
- Azure DevOps Pipelines
- GitHub

Project Structure
---------------------------------------

Python-Payroll-App/
 payroll.py          # Core payroll calculation logic
 gui.py              # Tkinter GUI
 database.py         # SQLite operations
 payroll.db          # Database storing payroll history

logs/               # Application logs
payslips/           # Generated payslip files
outputs/            # Payroll Summary file

Jenkinsfile         # Jenkins CI/CD pipeline
azure-pipelines.yml # Azure DevOps pipeline

CI/CD Pipelines
-----------------------------------
Jenkins
- Checkout code
- Install dependencies
- Run payroll script
- Generate logs and payslips
- Package outputs
- Publish artifacts

Azure DevOps
- YAML‑based pipeline
- Automated execution on push
- Artifact publishing
- Logs and output files stored for download


Future Enhancements
-------------------------------------
Add/Edit/Delete employee screens
Payroll history viewer
Modern UI using CustomTkinter
Password protected pdf payslips
REST API

