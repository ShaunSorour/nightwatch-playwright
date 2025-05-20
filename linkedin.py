from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import os

load_dotenv()  # Load environment variables from .env

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")


def login_to_linkedin(playwright):
    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login", timeout=60000)
        page.fill("input#username", LINKEDIN_EMAIL)
        page.fill("input#password", LINKEDIN_PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_url("https://www.linkedin.com/feed/", timeout=10000)
        print("✅ Successfully logged into LinkedIn.")

        page.goto("https://www.linkedin.com/jobs/search/?currentJobId=4205806439&distance=25&geoId=104035573&keywords=Software%20Developer%20In%20Test&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true", timeout=60000)
        page.wait_for_timeout(5000)
        return browser, context, page

    except Exception as e:
        print(f"⚠️ LinkedIn login failed: {e}")
        return None, None, None
