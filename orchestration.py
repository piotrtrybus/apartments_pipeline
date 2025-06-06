from prague_apartments_scraper.scraper import scrape_apartments
from prague_apartments_ingestion.loader import load_data
from dagster import op, job, RetryPolicy
from dotenv import load_dotenv
import subprocess
import os

@op(retry_policy=RetryPolicy(max_retries=5, delay=10))
def extract(context):
    try:
        context.log.info("Initiating the web scraper")
        scrape_apartments()
        context.log.info("Web scraping completed")
    except Exception as e:
        context.log.error(f"Scraping failed: {e}")
        raise

@op
def load(context):
    try:
        context.log.info("Initiating the Postgres load")
        load_data()
        context.log.info("Postgres load completed")
    except Exception as e:
        context.log.error(f"Unable to load data: {e}")
        raise


import dotenv
import os

@op
def transform(context):
    dotenv.load_dotenv(dotenv_path="../prague_apartments_dbt/.env", override=True)
    context.log.info("Initiating the DBT execution")

    try:
        context.log.info("Running DBT via PowerShell with .env loading")

        ps_command = (
                "& { "
                "Get-Content ../prague_apartments_dbt/.env | "
                "Where-Object { $_ -and ($_ -notmatch '^#') } | "
                "ForEach-Object { "
                "$name, $value = $_ -split '=', 2; "
                "if ($name) { Set-Item -Path Env:\\$name -Value $value } "
                "}; "
                "dbt run --target prod "
                "}"
            )


        result = subprocess.run(
                ["powershell", "-Command", ps_command],
                check=True,
                capture_output=True,
                text=True,
                cwd="prague_apartments_dbt",
                encoding="utf-8",
                errors="replace"
            )

        context.log.info("DBT execution completed")

    except subprocess.CalledProcessError as e:
        context.log.error(f"DBT failed with return code {e.returncode}")
        context.log.error(f"stdout: {e.stdout}") 
        context.log.error(f"stderr: {e.stderr}")
        raise
    except Exception as e:
        context.log.error(f"Unexpected error: {e}")
        raise



@op
def remove_csv(context):
    try:
        context.log.info("Removing file")
        os.remove("data/prague_apartments.csv")
    except Exception as e:
        context.log.info("Unable to remove CSV file")
        raise

@job
def run_elt():
    extract()
    load()
    transform()
    remove_csv()

if __name__ == "__main__":
    result = run_elt.execute_in_process()
