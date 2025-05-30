import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
import logging

#Logger setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("loader.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "prague_apartments.csv")

#Retrieve conn info
def get_connection_info(use_prod=False):
    return {
        "host": os.getenv("HOST"),
        "port": os.getenv("PROD_PORT" if use_prod else "PORT"),
        "dbname": os.getenv("PROD_DATABASE" if use_prod else "DATABASE"),
        "user": os.getenv("PROD_USER" if use_prod else "USER"),
        "password": os.getenv("PROD_PASSWORD" if use_prod else "PASSWORD"),
        "sslmode": "require"
    }

#Postgres conn
import pandas as pd  # make sure this is imported

def copy_csv_to_postgres(csv_path, table_name, conn_info):
    try:
        df = pd.read_csv(csv_path)
        row_count = len(df)
        col_count = len(df.columns)

        if row_count == 0:
            logger.warning(f"CSV at {csv_path} is empty. Aborting load.")
            return

        logger.info(f"CSV loaded with {row_count} rows and {col_count} columns.")

        with psycopg2.connect(**conn_info) as conn:
            logger.info("Connection established")
            with conn.cursor() as cursor, open(csv_path, 'r', encoding='utf-8') as f:
                logger.info("Streaming CSV into Postgres")
                cursor.copy_expert(
                    f"COPY {table_name} FROM STDIN WITH CSV HEADER",
                    f
                )
            conn.commit()
            logger.info(f"Data loaded from {csv_path} to {table_name}")

    except Exception as e:
        logger.exception(f"Failed to load data from {csv_path} to {table_name}")


    


def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "prague_apartments.csv")
    conn_info = get_connection_info(use_prod=True)
    copy_csv_to_postgres(csv_path, "prague_apartments", conn_info)

if __name__ == "__main__":
    load_data()