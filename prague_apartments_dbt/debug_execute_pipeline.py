import subprocess
import time
import logging

#Logger setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execute_pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

dbt_model = [
    'bronze_prague_apartments',
    'silver_prague_apartments_for_rent',
    'silver_prague_apartments_for_sale',
    'gold_rental_avg_per_district',
    'gold_sale_avg_per_district',
    'gold_rental_avg_per_layout',
    'gold_sale_avg_per_layout'
]


dbt_project_directory = 'prague_apartments'
sleep_s = 120

def execute_dbt_model(model):
    logger.info("Execution initiated")
    result = subprocess.run(
        ["dbt", "run", "--select", model],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        logger.info(f"Successful execution of {model}")
    else:
        logger.error(f"Unsuccessful execution {model}")

for model in dbt_model:
    execute_dbt_model(model)
    time.sleep(sleep_s)