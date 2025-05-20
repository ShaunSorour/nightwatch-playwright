from playwright.sync_api import sync_playwright
from jobs.jobs import job_keywords
from pdf_writer import PDFWriter
from dotenv import load_dotenv
import os

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

pdf_writer = PDFWriter()


def normalize_text(text):
    return " ".join(text.lower().split())


def match_keywords(title, keywords):
    normalized_title = normalize_text(title)
    return all(keyword.lower() in normalized_title for keyword in keywords)


def login_to_linkedin(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.linkedin.com/login", timeout=60000)
    page.fill("input#username", LINKEDIN_EMAIL)
    page.fill("input#password", LINKEDIN_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_url("https://www.linkedin.com/feed/", timeout=15000)
    page.goto("https://www.linkedin.com/jobs/search/?currentJobId=4205806439&distance=25&geoId=104035573&keywords=Software%20Developer%20In%20Test&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true", timeout=60000)
    page.wait_for_timeout(2000)

    print("✅ Logged in to LinkedIn")
    return browser, context, page


def scan_linkedin_jobs(playwright):
    browser, context, page = login_to_linkedin(playwright)

    # Select all relevant job links
    job_links = page.query_selector_all("a.job-card-container__link")

    jobs = []

    for job_link in job_links:
        try:
            href = job_link.get_attribute("href")
            # Find the strong tag inside this a tag
            strong_tag = job_link.query_selector("strong")
            if not strong_tag:
                continue
            title = strong_tag.inner_text().strip()

            if href and title:
                # Complete relative URLs if necessary
                full_url = href if href.startswith("http") else f"https://www.linkedin.com{href}"
                jobs.append((title, full_url))

        except Exception as e:
            print(f"⚠️ Error processing job link: {e}")

    if jobs:
        print("✅ Extracted job titles and links:")
        for title, url in jobs:
            print(f"- {title}: {url}")
        pdf_writer.write_url_and_jobs("https://www.linkedin.com/jobs/", title)
    else:
        print("❌ No job titles and links found on LinkedIn.")

    browser.close()

