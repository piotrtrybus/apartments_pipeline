import altair as alt
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv(dotenv_path="../prague_apartments/.env")

prod_conn_info = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PROD_PORT"),
    "dbname": os.getenv("PROD_DATABASE"),
    "user": os.getenv("PROD_USER"),
    "password": os.getenv("PROD_PASSWORD"),
    "sslmode": "require"  
}

with psycopg2.connect(**prod_conn_info) as conn:
    with conn.cursor() as cur:
        st.header("Prague Apartment Rentals")
        st.subheader("Rent per District (Top 15)")
        df = pd.read_sql_query("select * from gold_rental_avg_per_district order by avg_rent_czk desc limit 15", conn)                 
        bar = alt.Chart(df).mark_bar(size=15).encode(
            y=alt.Y('property_district:N', sort='-x', title="District", scale=alt.Scale(paddingInner=0.4)),
            x=alt.X('avg_rent_czk:Q', title="Average Rent (CZK)")
        ).properties(
            width=1000,
            height=500
        )

        labels = bar.mark_text(
            align='left',
            baseline='middle',
            dx=3,
            fontSize=10
        ).encode(
            text='avg_rent_czk:Q'
        )

        st.altair_chart(bar + labels, use_container_width=True)


        st.subheader("Rent per Layout")
        df = pd.read_sql_query("select * from gold_rental_avg_per_layout order by avg_rent_czk desc", conn)
        bar = alt.Chart(df).mark_bar(size=25).encode(
            y=alt.Y('property_layout:N', sort='-x', title="Layout", scale=alt.Scale(paddingInner=0.1)),
            x=alt.X('avg_rent_czk:Q', title="Average Rent (CZK)")
        ).properties(
            width=1000,
            height=700
        )

        labels = bar.mark_text(
            align='left',
            baseline='middle',
            dx=3,
            fontSize=10
        ).encode(
            text='avg_rent_czk:Q'
        )

        st.altair_chart(bar + labels, use_container_width=True)

        st.header("Prague Apartment Sales")
        st.subheader("Price per District (Top 15)")
        df = pd.read_sql_query("select * from gold_sale_avg_per_district order by avg_price_czk desc limit 15", conn)
        bar = alt.Chart(df).mark_bar(size=15).encode(
            y=alt.Y('property_district:N', sort='-x', title="District", scale=alt.Scale(paddingInner=0.4)),
            x=alt.X('avg_price_czk:Q', title="Average Price (CZK)")
        ).properties(
            width=1000,
            height=700
        )

        labels = bar.mark_text(
            align='left',
            baseline='middle',
            dx=3,
            fontSize=10
        ).encode(
            text='avg_price_czk:Q'
        )

        st.altair_chart(bar + labels, use_container_width=True)


        st.subheader("Price per Layout")
        df = pd.read_sql_query("select * from gold_sale_avg_per_layout order by avg_price_czk desc", conn)               
        bar = alt.Chart(df).mark_bar(size=30).encode(
            y=alt.Y('property_layout:N', sort='-x', title="Layout", scale=alt.Scale(paddingInner=0.1)),
            x=alt.X('avg_price_czk:Q', title="Average Price (CZK)")
        ).properties(
            width=1000,
            height=700
        )

        labels = bar.mark_text(
            align='left',
            baseline='middle',
            dx=3,
            fontSize=10
        ).encode(
            text='avg_price_czk:Q'
        )

        st.altair_chart(bar + labels, use_container_width=True)
