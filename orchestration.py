from prague_apartments_scraper.scraper import scrape_apartments
from prague_apartments_ingestion.loader import load_data
from prefect import flow, task, get_run_logger
from dotenv import load_dotenv
import subprocess
import os

@task(retries=3, retry_delay_seconds=5)
def extract():
    logger = get_run_logger()
    try:
        logger.info("Initiating the web scraper")
        scrape_apartments()
        logger.info("Web scraping completed")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise

@task
def load():
    logger = get_run_logger()
    try:
        logger.info("Initiating the Postgres load")
        load_data()
        logger.info("Postgres load completed")
    except Exception as e:
        logger.error(f"Unable to load data: {e}")
        raise


@task
def transform():
    logger = get_run_logger()
    load_dotenv(dotenv_path="../prague_apartments_dbt/.env", override=True)
    logger.info("Initiating the DBT execution")
    try:
        result = subprocess.run(
            ["dbt", "run","--target","prod"],
            check=True,
            capture_output=True,
            text=True,
            cwd="prague_apartments_dbt",
            encoding="utf-8",
            errors="replace"  
        )
        logger.info("DBT execution completed")
        logger.debug(f"DBT stdout:\n{result.stdout}")
        logger.debug(f"DBT stderr:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"DBT failed with return code {e.returncode}")
        logger.error(f"stderr: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


@task
def remove_csv():
    logger = get_run_logger()
    try:
        logger.info("Removing file")
        os.remove("data/prague_apartments.csv")
    except Exception as e:
        logger.error("Unable to remove CSV file")
        raise

@flow
def run_elt():
    extract()
    load()
    transform()
    remove_csv()