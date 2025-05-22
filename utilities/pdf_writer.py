from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import blue
import PyPDF2
import os


class PDFWriter:
    def __init__(self, filepath="results/jobs_found.pdf"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(self.filepath), pagesize=A4)
        self.width, self.height = A4
        self.y = self.height - 40
        self.line_height = 14

        self._write_header()

    def _write_header(self):
        timestamp = datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(40, self.y, f"📅 {timestamp}")
        self.y -= self.line_height * 2


    def write_url_and_jobs(self, url, job_titles):
        print(f"Writing URL and jobs to PDF: {url}, {job_titles}")
        if self.y < 60:
            self._new_page()

        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawString(40, self.y, f"📍 {url}")

        self.c.linkURL(url, (40, self.y - 2, 540, self.y + 10), relative=0)

        self.y -= self.line_height

        self.c.setFont("Helvetica", 10)
        for idx, title in enumerate(job_titles, start=1):
            self.c.drawString(60, self.y, f"{idx}. {title}")
            self.y -= self.line_height
            if self.y < 40:
                self._new_page()

        self.y -= self.line_height


    def write_jobs_to_pdf(self, jobs_list, filename="results/linkedin_jobs.pdf"):
        """
        Writes a list of job titles with embedded links to a PDF document
        using ReportLab's platypus engine.

        Args:
            jobs_list (list): A list of tuples, where each tuple contains
                              (job_title, job_link).
            filename (str): Optional override for the output PDF file name.
        """
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        link_style = styles['Normal']
        link_style.textColor = blue
        link_style.underline = 1

        story.append(Paragraph("<b>Linkedin :</b>", styles['h2']))
        story.append(Paragraph("<br/>", styles['Normal']))  # Add some space

        for title, link in jobs_list:
            p_text = f'<link href="{link}">{title}</link>'
            story.append(Paragraph(p_text, link_style))
            story.append(Paragraph("<br/>", styles['Normal']))  # Line break

        doc.build(story)
        print(f"PDF '{output_path}' created successfully with job listings.")


    def merge_pdfs(self, pdf1_path, pdf2_path, output_path):
        merger = PyPDF2.PdfMerger()

        files_added = 0

        if os.path.exists(pdf1_path):
            merger.append(pdf1_path)
            files_added += 1
        else:
            print(f"Warning: {pdf1_path} not found. Skipping.")

        if os.path.exists(pdf2_path):
            merger.append(pdf2_path)
            files_added += 1
        else:
            print(f"Warning: {pdf2_path} not found. Skipping.")

        if files_added > 0:
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            print(f"PDFs merged successfully into {output_path}")
        else:
            print("No input PDFs were found. Merge not performed.")

    def _new_page(self):
        self.c.showPage()
        self.y = self.height - 40

    def save(self):
        print(f"Saving PDF to {self.filepath}")
        self.c.save()
        print("PDF saved successfully.")
