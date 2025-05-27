import altair as alt
import streamlit as st
import pandas as pd
import duckdb
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'prod_prague_apartments.db')

with duckdb.connect(db_path) as con:
    st.header("Prague Apartment Rentals")
    st.subheader("Rent per District")
    df = con.execute('''
                     select * 
                     
                     from gold_rental_avg_per_district 
                     
                     order by avg_rent_czk desc
                     
                     ''').df()
    
    bar = alt.Chart(df).mark_bar(size=15).encode(
        y=alt.Y('property_district:N', sort='-x', title="District", scale=alt.Scale(paddingInner=0.4)),
        x=alt.X('avg_rent_czk:Q', title="Average Rent (CZK)")
    ).properties(
        width=700,
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
    df = con.execute('''
                     select * 
                     
                     from gold_rental_avg_per_layout
                     
                     order by avg_rent_czk desc
                     
                     ''').df()
    
    bar = alt.Chart(df).mark_bar(size=25).encode(
        y=alt.Y('property_layout:N', sort='-x', title="Layout", scale=alt.Scale(paddingInner=0.1)),
        x=alt.X('avg_rent_czk:Q', title="Average Rent (CZK)")
    ).properties(
        width=800,
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

    st.header("Prague Apartment Sales")
    st.subheader("Price per District")
    df = con.execute('''
                     select * 
                     
                     from gold_sale_avg_per_district 
                     
                     order by avg_price_czk desc
                     
                     ''').df()
    
    bar = alt.Chart(df).mark_bar(size=15).encode(
        y=alt.Y('property_district:N', sort='-x', title="District", scale=alt.Scale(paddingInner=0.4)),
        x=alt.X('avg_price_czk:Q', title="Average Price (CZK)")
    ).properties(
        width=700,
        height=500
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
    df = con.execute('''
                     select * 
                     
                     from gold_sale_avg_per_layout
                     
                     order by avg_price_czk desc
                     
                     ''').df()
    
    bar = alt.Chart(df).mark_bar(size=30).encode(
        y=alt.Y('property_layout:N', sort='-x', title="Layout", scale=alt.Scale(paddingInner=0.1)),
        x=alt.X('avg_price_czk:Q', title="Average Price (CZK)")
    ).properties(
        width=800,
        height=500
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
