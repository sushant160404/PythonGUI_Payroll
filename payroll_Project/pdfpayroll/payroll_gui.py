from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import os
from tkinter import Tk, Label, Entry, Button, StringVar, DoubleVar, filedialog, messagebox



def generate_payroll_pdf(employee_name, employee_id, position, pay_period, gross_salary, tax_rate, other_deductions, output_file):
    """
    Generates a customized payroll PDF with additional styling and a company logo.
    """
    # Calculate deductions and net salary
    tax_deduction = gross_salary * (tax_rate / 100)
    total_deductions = tax_deduction + other_deductions
    net_salary = gross_salary - total_deductions

    # Create the document
    pdf = SimpleDocTemplate(output_file, pagesize=A4)
    elements = []

    # Add company logo (Optional: Replace "logo.png" with the actual path to your logo)
    logo_path = "logo.png"  # Replace with your logo file path
    if os.path.exists(logo_path):
        logo = Image(logo_path, 2 * inch, 1 * inch)
        elements.append(logo)

    # Add document title
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    title_style = ParagraphStyle(name='Title', fontSize=18, alignment=1, spaceAfter=20)
    title = Paragraph("Payroll Statement", title_style)
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

    elements.append(Paragraph("<br/>", title_style))  # Add a space between tables

    # Salary Details
    salary_data = [
        ["Description", "Amount (₹)"],
        ["Gross Salary", f"{gross_salary:,.2f}"],
        ["Tax Deduction ({}%)".format(tax_rate), f"{tax_deduction:,.2f}"],
        ["Other Deductions", f"{other_deductions:,.2f}"],
        ["Total Deductions", f"{tax_deduction + other_deductions:,.2f}"],
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
        ('TEXTCOLOR', (-1, -1), (-1, -1), colors.green),  # Highlight Net Salary
        ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey)
    ]))
    elements.append(salary_table)

    # Save the PDF
    pdf.build(elements)
    messagebox.showinfo("Success", f"Customized Payroll PDF generated: {output_file}")



# GUI Application
def generate_pdf():
    try:
        # Collect input values
        employee_name = employee_name_var.get()
        employee_id = employee_id_var.get()
        position = position_var.get()
        pay_period = pay_period_var.get()
        gross_salary = gross_salary_var.get()
        tax_rate = tax_rate_var.get()
        other_deductions = other_deductions_var.get()

        if not all([employee_name, employee_id, position, pay_period]):
            messagebox.showerror("Error", "Please fill out all fields!")
            return

        # Select output file
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Payroll PDF"
        )
        if not output_file:
            return

        # Generate PDF
        generate_payroll_pdf(
            employee_name, employee_id, position, pay_period, gross_salary, tax_rate, other_deductions, output_file
        )

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Main Window
app = Tk()
app.title("Payroll PDF Generator")
app.geometry("400x500")

# Labels and Entry Widgets
Label(app, text="Employee Name:").pack(pady=5)
employee_name_var = StringVar()
Entry(app, textvariable=employee_name_var, width=30).pack()

Label(app, text="Employee ID:").pack(pady=5)
employee_id_var = StringVar()
Entry(app, textvariable=employee_id_var, width=30).pack()

Label(app, text="Position:").pack(pady=5)
position_var = StringVar()
Entry(app, textvariable=position_var, width=30).pack()

Label(app, text="Pay Period:").pack(pady=5)
pay_period_var = StringVar()
Entry(app, textvariable=pay_period_var, width=30).pack()

Label(app, text="Gross Salary (₹):").pack(pady=5)
gross_salary_var = DoubleVar()
Entry(app, textvariable=gross_salary_var, width=30).pack()

Label(app, text="Tax Rate (%):").pack(pady=5)
tax_rate_var = DoubleVar()
Entry(app, textvariable=tax_rate_var, width=30).pack()

Label(app, text="Other Deductions (₹):").pack(pady=5)
other_deductions_var = DoubleVar()
Entry(app, textvariable=other_deductions_var, width=30).pack()

# Generate Button
Button(app, text="Generate Payroll PDF", command=generate_pdf, bg="green", fg="white").pack(pady=20)

# Run the Application
app.mainloop()
