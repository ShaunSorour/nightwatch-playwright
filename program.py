from playwright.sync_api import sync_playwright

# from companies.companies_local import company_urls
from companies.companies_foreign import company_urls
from jobs.jobs import job_keywords
from pdf_writer import PDFWriter

pdf_writer = PDFWriter()


def normalize_text(text):
    return " ".join(text.lower().split())


def match_keywords(title, keywords):
    normalized_title = normalize_text(title)
    return all(keyword.lower() in normalized_title for keyword in keywords)


def scan_job_page(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(f"{url}", timeout=60000)
            page.wait_for_timeout(5000)

            job_titles = []
            for job in page.query_selector_all("a, h3, h4, h5"):
                job_title = job.inner_text().strip()
                for keyword in job_keywords:
                    keyword_parts = keyword.split(",")
                    if match_keywords(job_title, keyword_parts):
                        job_titles.append(job_title)

            if job_titles:
                print(f"✅ Matching job titles on {url}:")
                for title in job_titles:
                    print(f"- {title}")
                pdf_writer.write_url_and_jobs(url, job_titles)
            else:
                print(f"❌ No matching job titles on {url}.")

            browser.close()

    except Exception as e:
        print(f"⚠️ Skipping {url} due to error: {e}")


def scan_github_jobs():
    for url in company_urls:
        scan_job_page(url)


if __name__ == "__main__":
    scan_github_jobs()
    pdf_writer.save()
