import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient


# Connect to MongoDB
def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["PayrollDB"]
        return db["PayrollCollection"]
    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to MongoDB: {e}")
        return None


# Function to add a payroll entry
def add_payroll_entry():
    employee_name = entry_name.get()
    employee_id = entry_id.get()
    position = entry_position.get()
    pay_period = entry_pay_period.get()
    gross_salary = entry_gross_salary.get()
    tax_rate = entry_tax_rate.get()
    other_deductions = entry_other_deductions.get()

    if not (employee_name and employee_id and position and pay_period and gross_salary and tax_rate and other_deductions):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        gross_salary = float(gross_salary)
        tax_rate = float(tax_rate)
        other_deductions = float(other_deductions)
    except ValueError:
        messagebox.showerror("Input Error", "Gross Salary, Tax Rate, and Other Deductions must be numbers!")
        return

    # Calculate deductions and net salary
    tax_deduction = gross_salary * (tax_rate / 100)
    total_deductions = tax_deduction + other_deductions
    net_salary = gross_salary - total_deductions

    # Create payroll record
    payroll_record = {
        "employee_name": employee_name,
        "employee_id": employee_id,
        "position": position,
        "pay_period": pay_period,
        "gross_salary": gross_salary,
        "tax_rate": tax_rate,
        "other_deductions": other_deductions,
        "net_salary": net_salary
    }

    # Insert record into MongoDB
    collection = connect_to_mongo()
    if collection is not None:  # Updated condition
        collection.insert_one(payroll_record)
        messagebox.showinfo("Success", f"Payroll entry for {employee_name} added successfully!")
        clear_entries()
    else:
        messagebox.showerror("Database Error", "Failed to connect to MongoDB!")


# Function to view payroll records
def view_payroll_entries():
    collection = connect_to_mongo()
    if collection is None:  # Updated condition
        messagebox.showerror("Database Error", "Failed to connect to MongoDB!")
        return

    records = collection.find()
    view_window = tk.Toplevel(root)
    view_window.title("Payroll Records")

    tree = ttk.Treeview(view_window, columns=("Name", "ID", "Position", "Pay Period", "Gross Salary", "Net Salary"), show="headings")
    tree.heading("Name", text="Employee Name")
    tree.heading("ID", text="Employee ID")
    tree.heading("Position", text="Position")
    tree.heading("Pay Period", text="Pay Period")
    tree.heading("Gross Salary", text="Gross Salary (₹)")
    tree.heading("Net Salary", text="Net Salary (₹)")

    for record in records:
        tree.insert("", tk.END, values=(
            record["employee_name"],
            record["employee_id"],
            record["position"],
            record["pay_period"],
            record["gross_salary"],
            record["net_salary"]
        ))

    tree.pack(fill=tk.BOTH, expand=True)



# Function to clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_pay_period.delete(0, tk.END)
    entry_gross_salary.delete(0, tk.END)
    entry_tax_rate.delete(0, tk.END)
    entry_other_deductions.delete(0, tk.END)


# GUI Setup
root = tk.Tk()
root.title("Payroll Entry System")

# Labels and Entry Widgets
tk.Label(root, text="Employee Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Employee ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_id = tk.Entry(root)
entry_id.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Position:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
entry_position = tk.Entry(root)
entry_position.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Pay Period:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
entry_pay_period = tk.Entry(root)
entry_pay_period.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Gross Salary (₹):").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
entry_gross_salary = tk.Entry(root)
entry_gross_salary.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Tax Rate (%):").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
entry_tax_rate = tk.Entry(root)
entry_tax_rate.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Other Deductions (₹):").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
entry_other_deductions = tk.Entry(root)
entry_other_deductions.grid(row=6, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Payroll Entry", command=add_payroll_entry, width=20).grid(row=7, column=0, padx=10, pady=20)
tk.Button(root, text="View Payroll Records", command=view_payroll_entries, width=20).grid(row=7, column=1, padx=10, pady=20)
tk.Button(root, text="Clear Fields", command=clear_entries, width=20).grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
