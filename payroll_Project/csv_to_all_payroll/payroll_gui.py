import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch


def generate_all_payrolls_pdf(employees, output_file):
    """
    Generates a single PDF containing payroll details for multiple employees.
    """
    pdf = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []

    for employee in employees:
        employee_name = employee.get("name")
        employee_id = employee.get("id")
        position = employee.get("position")
        pay_period = employee.get("pay_period")
        gross_salary = employee.get("gross_salary", 0)
        tax_rate = employee.get("tax_rate", 0)
        other_deductions = employee.get("other_deductions", 0)

        tax_deduction = gross_salary * (tax_rate / 100)
        total_deductions = tax_deduction + other_deductions
        net_salary = gross_salary - total_deductions

        # Add title
        title_style = ParagraphStyle(name='Title', fontSize=18, alignment=1, spaceAfter=20)
        title = Paragraph(f"Payroll Statement for {employee_name}", title_style)
        elements.append(title)

        # Employee Information
        employee_data = [
            ["Employee Name", employee_name],
            ["Employee ID", employee_id],
            ["Position", position],
            ["Pay Period", pay_period]
        ]
        employee_table = Table(employee_data, colWidths=[150, 300])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(employee_table)

        # Add a space
        elements.append(Paragraph("<br/>", title_style))

        # Salary Details
        salary_data = [
            ["Description", "Amount (₹)"],
            ["Gross Salary", f"{gross_salary:,.2f}"],
            ["Tax Deduction ({}%)".format(tax_rate), f"{tax_deduction:,.2f}"],
            ["Other Deductions", f"{other_deductions:,.2f}"],
            ["Total Deductions", f"{total_deductions:,.2f}"],
            ["Net Salary", f"{net_salary:,.2f}"],
        ]
        salary_table = Table(salary_data, colWidths=[250, 200])
        salary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TEXTCOLOR', (-1, -1), (-1, -1), colors.green),
            ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey)
        ]))
        elements.append(salary_table)

        # Add a page break
        elements.append(PageBreak())

    pdf.build(elements)
    messagebox.showinfo("Success", f"All payrolls generated in: {output_file}")


def upload_csv():
    """
    Opens a file dialog to select a CSV file and processes the data.
    """
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        employees = []
        with open(file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert data types
                row["gross_salary"] = float(row.get("gross_salary", 0))
                row["tax_rate"] = float(row.get("tax_rate", 0))
                row["other_deductions"] = float(row.get("other_deductions", 0))
                employees.append(row)

        # Ask for output file
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_file:
            return

        # Generate the PDF
        generate_all_payrolls_pdf(employees, output_file)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Setup
root = tk.Tk()
root.title("Payroll PDF Generator")

# GUI Elements
tk.Label(root, text="Bulk Payroll PDF Generator", font=("Helvetica", 16)).pack(pady=10)
tk.Button(root, text="Upload Employee Data (CSV)", command=upload_csv, width=30, height=2).pack(pady=20)

# Run the GUI
root.mainloop()
