from playwright.sync_api import sync_playwright
from utilities.pdf_writer import PDFWriter
from scanners.linkedin import scan_linkedin_jobs
from scanners.company import scan_company_careers
from scanners.spy import spy
pdf_writer = PDFWriter()



if __name__ == "__main__":
    with sync_playwright() as p:
        scan_company_careers(p)
        scan_linkedin_jobs(p)
        spy()
        pdf_writer.merge_pdfs('results/final.pdf')