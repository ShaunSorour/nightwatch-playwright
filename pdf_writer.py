from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path


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


    def write_jobs_with_links(self, url, jobs):
        print(f"Writing jobs to PDF: {jobs}")
        """
        Writes the main page URL and a list of (title, job_url) pairs
        to the PDF, each job title linked to its URL.
        """
        if self.y < 60:
            self._new_page()

        self.c.setFont("Helvetica-Bold", 11)
        self.c.drawString(40, self.y, f"📍 {url}")
        self.c.linkURL(url, (40, self.y - 2, 540, self.y + 10), relative=0)
        self.y -= self.line_height * 1.5

        self.c.setFont("Helvetica", 10)
        for idx, (title, job_url) in enumerate(jobs, start=1):
            line_text = f"{idx}. {title}"
            self.c.drawString(60, self.y, line_text)
            text_width = self.c.stringWidth(line_text, "Helvetica", 10)
            # Add clickable link only over the title text
            self.c.linkURL(job_url, (60, self.y - 2, 60 + text_width, self.y + 10), relative=0)
            self.y -= self.line_height

            if self.y < 40:
                self._new_page()

        self.y -= self.line_height


    def _new_page(self):
        self.c.showPage()
        self.y = self.height - 40

    def save(self):
        print(f"Saving PDF to {self.filepath}")
        self.c.save()
        print("PDF saved successfully.")
