from utilities.pdf_writer import PDFWriter

pdf_writer = PDFWriter()

def scan_google_jobs(playwright):
    print("🔍 Scanning Google job search results...")
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url = "https://www.google.com/search?sca_esv=9bb6a8d79ae60b0c&sxsrf=AE3TifPG40aMqN4Cl4DLN08co_487bVdVw:1748437691216&q=qa+engineer+jobs+in+the+last+3+days&udm=8"
        page.goto(url, timeout=60000)
        page.wait_for_timeout(2000)

        # Select all job cards
        job_cards = page.query_selector_all('a.MQUd2b')
        jobs = []

        print(f"Debug: {len(job_cards)} job cards found.")

        for card in job_cards:
            title_elem = card.query_selector('.tNxQIb')
            company_elem = card.query_selector('.wHYlTd.MKCbgd.a3jPc')
            href = card.get_attribute("href")

            title = title_elem.inner_text().strip() if title_elem else None
            company = company_elem.inner_text().strip() if company_elem else None

            if title and company:
                full_title = f"{company} - {title}"
            else:
                full_title = title or "Unknown Title"

            if href and not href.startswith("http"):
                href = f"https://www.google.com{href}"

            if full_title and href:
                jobs.append((full_title, href))

        if jobs:
            print("✅ Extracted job titles and links:")
            pdf_writer.write_jobs_to_pdf(jobs, 'Google', 'results/google_jobs.pdf')
        else:
            print("❌ No job titles and links found on Google.")

        browser.close()
    except Exception as e:
        print(f"⚠️ Google job scan failed: {e}")