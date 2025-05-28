import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn_info = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "dbname": os.getenv("DATABASE"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "sslmode": "require"  
}

prod_conn_info = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PROD_PORT"),
    "dbname": os.getenv("PROD_DATABASE"),
    "user": os.getenv("PROD_USER"),
    "password": os.getenv("PROD_PASSWORD"),
    "sslmode": "require"  
}

#csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "prague_apartments.csv")

#df = pd.read_csv(csv_path)


sql_create_postgres = '''

drop table prague_apartments cascade;

create table if not exists prague_apartments(
    eventid VARCHAR,
    title VARCHAR,
    link VARCHAR,
    location VARCHAR,
    district VARCHAR,
    property_type VARCHAR,
    price_czk VARCHAR,
    layout VARCHAR,
    area_m2 NUMERIC,
    timestamp TIMESTAMP
);

'''

sql_insert_postgres = '''

insert into prague_apartments (
    eventid, 
    title,
    location, 
    district, 
    property_type, 
    price_czk,
    layout,
    area_m2,
    timestamp
) values (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
    );

'''

sql_check_postgres = '''

select * from prague_apartments
'''

#Postgres con
with psycopg2.connect(**conn_info) as conn:
    with conn.cursor() as cur:
        df = cur.execute(sql_check_postgres)
        df = cur.fetchall()
        print(df)
    