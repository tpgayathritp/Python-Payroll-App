def seed_employees(conn):
   # conn = get_connection()
    cursor = conn.cursor()

    employees = [
        ('101', 'John Smith', 55000, 1,1,1.5,300, 100),
        ('102', 'Sara Jones', 5200, 2,2,1, 250, 80),
        ('103', 'David Lee', 54800, 1,2,1,200, 120),
        ('104', 'Priya Nair', 5500, 3,2,1,350, 150),
        ('105', 'Alex Brown', 44700, 1,1,0.5,180, 90)
    ]

    cursor.executemany("""
        INSERT INTO employees (emp_id, name, base_salary, hours,rate,multiplier,allowances, deductions)
        VALUES (?, ?, ?, ?, ?,?,?,?)
    """, employees)

    conn.commit()
    conn.close()

    print("Employees inserted successfully.")




