import csv
import pandas as pd
import matplotlib.pyplot as plt
from jobspy import scrape_jobs


# JOBSPY MODULE - GITHUB
# ----------------------
def spy():
    print("🔍 Scanning SPY...")

    # jobs = scrape_jobs(
    #     site_name=["indeed", "linkedin", "google"],
    #     search_term="QA Engineer",
    #     google_search_term="QA Engineer jobs near Cape Town, South Africa since yesterday",
    #     location="Cape Town, South Africa",
    #     results_wanted=100,
    #     hours_old=72,
    #     country_indeed='south africa',
    # )

    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "google"],
        search_term="Managing Editor",
        google_search_term="Managing Editor jobs near Cape Town, South Africa since yesterday",
        location="Cape Town, South Africa",
        results_wanted=100,
        hours_old=72,
        country_indeed='south africa',
    )
    print(f"Found {len(jobs)} jobs")
    print(jobs.head())
    jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

    # swap before conversion
    df = pd.read_csv("jobs.csv")
    df = df[["title", "job_url", "company"]]
    # contents 
    df[["job_url", "company"]] = df[["company", "job_url"]]
    # column headers
    df = df.rename(columns={"job_url": "company_tmp", "company": "job_url"})
    df = df.rename(columns={"company_tmp": "company"})
    # save
    df.to_csv("jobs_swapped.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)

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