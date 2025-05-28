from prague_apartments_scraper.scraper import save_data,scrape_data
from prague_apartments_ingestion.loader import load_data
from prefect import flow, task
import subprocess
import logging

#Logger setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("elt.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@task
def retrieve_data():
    logger.info("Initiating the web scraper")
    scrape_data()
    logger.info("Web scraping completed")
    save_data()
    logger.info("Web scraping results saved to CSV")


@task
def load_postgres():
    logger.info("Initiating the Postgres load")
    load_data()
    logger.info("Postgres load completed")


@task
def execute_dbt():
    logger.info("Initiating the DBT execution")
    try:
        result = subprocess.run(
            ["dbt", "run"],
            check=True,
            capture_output=True,
            text=True,
            cwd="prague_apartments_dbt"
        )
        logger.info("DBT execution completed")
        logger.debug(f"stdout:\n{result.stdout}")
        logger.debug(f"stderr:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"DBT failed with return code {e.returncode}")
        logger.error(f"stdout:\n{e.stdout}")
        logger.error(f"stderr:\n{e.stderr}")
        raise

@flow
def run_elt():
    retrieve_data()
    load_postgres()
    execute_dbt()

if __name__ == "__main__":
    run_elt()
