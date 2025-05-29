from prague_apartments_scraper.scraper import scrape_apartments
from prague_apartments_ingestion.loader import load_data
from prefect import flow, task
from dotenv import load_dotenv
import subprocess
import logging
import os
import sys

#Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@task
def extract():
    logger.info("Initiating the web scraper")
    scrape_apartments()
    logger.info("Web scraping completed")

@task
def load():
    logger.info("Initiating the Postgres load")
    load_data()
    logger.info("Postgres load completed")


@task
def transform():
    load_dotenv(dotenv_path="../prague_apartments_dbt/.env", override=True)
    logger.info("Initiating the DBT execution")
    try:
        result = subprocess.run(
            ["dbt", "run","--target","prod"],
            check=True,
            capture_output=True,
            text=True,
            cwd="prague_apartments_dbt"
        )
        logger.info("DBT execution completed")
    except subprocess.CalledProcessError as e:
        logger.error(f"DBT failed with return code {e.returncode}")
        raise


@task
def remove_csv():
    logger.info("Removing file")
    os.remove("data/prague_apartments.csv")


@flow
def run_elt():
    extract()
    load()
    transform()
    remove_csv()

if __name__ == "__main__":
    run_elt.serve(name="prague-apartments-pipeline-new", cron="0 6 * * *")