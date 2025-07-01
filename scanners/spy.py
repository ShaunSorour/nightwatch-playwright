import csv
import pandas as pd
import matplotlib.pyplot as plt
from jobspy import scrape_jobs


# JOBSPY MODULE - GITHUB
# ############
def spy():
    print("🔍 Scanning SPY...")

    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "google"],
        search_term="QA Engineer",
        google_search_term="QA Engineer jobs near Cape Town, South Africa since yesterday",
        location="Cape Town, South Africa",
        results_wanted=100,
        hours_old=72,
        country_indeed='south africa',
    )
    print(f"Found {len(jobs)} jobs")
    print(jobs.head())
    jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

    # --- Swap columns and contents before PDF conversion ---
    df = pd.read_csv("jobs.csv")
    df = df[["title", "company", "url"]]
    # Swap the contents of 'job_url' and 'company'
    df[["job_url", "company"]] = df[["company", "job_url"]]
    # Save the swapped DataFrame back to CSV (optional, for verification)
    df.to_csv("jobs_swapped.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

    # Use the swapped DataFrame for PDF conversion
    fig, ax = plt.subplots(figsize=(12, min(0.5 * len(df), 50)))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.axis('off')
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='left'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.tight_layout()
    plt.savefig("results/spy.pdf", bbox_inches='tight')
    plt.close()