from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_payroll_pdf(employee_name, employee_id, position, pay_period, gross_salary, tax_rate, other_deductions, output_file):
    """
    Generates a payroll PDF with the given employee details and saves it to a file.
    """
    # Calculate deductions and net salary
    tax_deduction = gross_salary * (tax_rate / 100)
    total_deductions = tax_deduction + other_deductions
    net_salary = gross_salary - total_deductions

    # Create the PDF
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Payroll Statement")

    # Company Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Company Name: XYZ Pvt. Ltd.")
    c.drawString(50, height - 120, "Address: 123 Software Lane, Tech City, India")
    c.drawString(50, height - 140, "Phone: +91-123-456-7890")

    # Employee Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 180, "Employee Details:")
    c.setFont("Helvetica", 12)
    c.drawString(70, height - 200, f"Name: {employee_name}")
    c.drawString(70, height - 220, f"Employee ID: {employee_id}")
    c.drawString(70, height - 240, f"Position: {position}")
    c.drawString(70, height - 260, f"Pay Period: {pay_period}")

    # Earnings and Deductions
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 300, "Salary Details:")
    c.setFont("Helvetica", 12)
    c.drawString(70, height - 320, f"Gross Salary: ₹{gross_salary:,.2f}")
    c.drawString(70, height - 340, f"Tax Deduction ({tax_rate}%): ₹{tax_deduction:,.2f}")
    c.drawString(70, height - 360, f"Other Deductions: ₹{other_deductions:,.2f}")
    c.drawString(70, height - 380, f"Total Deductions: ₹{total_deductions:,.2f}")
    c.drawString(70, height - 400, f"Net Salary: ₹{net_salary:,.2f}")

    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "This is a system-generated document and does not require a signature.")

    # Save the PDF
    c.save()
    print(f"Payroll PDF generated: {output_file}")


# Main program
if __name__ == "__main__":
    # Sample input
    employee_name = input("Enter employee name: ")
    employee_id = input("Enter employee ID: ")
    position = input("Enter position: ")
    pay_period = input("Enter pay period (e.g., Dec 2024): ")
    gross_salary = float(input("Enter gross salary (in ₹): "))
    tax_rate = float(input("Enter tax rate (in %): "))
    other_deductions = float(input("Enter other deductions (in ₹): "))

    # Output file
    output_file = os.path.join(os.getcwd(), f"Payroll_{employee_id}.pdf")

    # Generate payroll PDF
    generate_payroll_pdf(employee_name, employee_id, position, pay_period, gross_salary, tax_rate, other_deductions, output_file)
