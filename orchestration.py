from prague_apartments_scraper.scraper import scrape_apartments
from prague_apartments_ingestion.loader import load_data
from prefect import flow, task
import subprocess
import logging
import os

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
def load_env_from_dotenv():
    command = '''
    Get-Content .env | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.+)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim('"').Trim()
            [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    '''
    subprocess.run(["powershell", "-Command", command], check=True)


@task
def transform():
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
    load_env_from_dotenv()
    load()
    transform()
    #remove_csv()

if __name__ == "__main__":
    run_elt.serve(name="prague-apartments-pipeline", cron="0 6 * * *")