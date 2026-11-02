from fpdf import FPDF

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EMPLOYMENT CONTRACT & CLEARANCE EVIDENCE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Body
    pdf.set_font("Helvetica", "", 11)
    content = """
    EMPLOYMENT DETAILS & SALARY CLAIM PROOF

    Employee Name: Ayesha Tariq
    Designation: Senior Software Engineer
    Company: TechVision Solutions Pvt. Ltd., Blue Area, Islamabad
    Employment Tenure: March 01, 2025 - August 31, 2026

    STATEMENT OF CLAIM & PENDING DUES:
    --------------------------------------------------
    1. Monthly Net Agreed Salary: PKR 250,000
    2. Pending Salary (June 2026): PKR 250,000 (Unpaid)
    3. Pending Salary (July 2026): PKR 250,000 (Unpaid)
    4. Pending Salary (August 2026): PKR 250,000 (Unpaid)
    5. Provident Fund & Gratuity Clearance: PKR 200,000 (Unpaid)
    --------------------------------------------------
    TOTAL OUTSTANDING CLAIM: PKR 950,000

    SUMMARY OF INCIDENT:
    The employee formally submitted a 30-day resignation notice on July 31, 2026, 
    completing all handovers and receiving HR clearance on August 31, 2026. 
    Despite official clearance and multiple written reminders sent to HR and Management, 
    the employer has intentionally withheld final settlement dues exceeding 90 days.

    ATTACHED PROOFS:
    - Signed HR Exit Clearance Form
    - Resignation Acknowledgement Email dated July 31, 2026
    - Bank Statement showing non-receipt of salaries for 3 consecutive months
    """
    
    for line in content.split('\n'):
        pdf.multi_cell(0, 6, line.strip(), new_x="LMARGIN", new_y="NEXT")
        
    pdf.output("sample_evidence_employment.pdf")
    print("PDF generated successfully as 'sample_evidence_employment.pdf'")

if __name__ == "__main__":
    create_sample_pdf()