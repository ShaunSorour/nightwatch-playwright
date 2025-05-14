from playwright.sync_api import sync_playwright
from datetime import datetime
from pathlib import Path
from companies.companies_local import company_urls
from jobs.jobs import job_keywords

# clear file and write timestamp
timestamp = datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
header = f"📅 Job Scan Run - {timestamp}\n{'='*30}\n\n"
Path("results/jobs_found.txt").write_text(header, encoding="utf-8")
output_file = Path("results/jobs_found.txt")


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
            for job in page.query_selector_all("a"):
                job_title = job.inner_text().strip()
                for keyword in job_keywords:
                    keyword_parts = keyword.split(",")
                    if match_keywords(job_title, keyword_parts):
                        job_titles.append(job_title)

            if job_titles:
                print(f"✅ Matching job titles on {url}:")
                formatted_titles = "\n".join([f"- {title}" for title in job_titles])
                print(formatted_titles)

                # Write to file
                with output_file.open("a", encoding="utf-8") as f:
                    f.write("\n==============================\n")
                    f.write(f"📍 {url}\n")
                    for idx, title in enumerate(job_titles, start=1):
                        f.write(f"  {idx}. {title}\n")
                    f.write("==============================\n")

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
