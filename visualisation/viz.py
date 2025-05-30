import altair as alt
import streamlit as st
import pandas as pd
import os
import psycopg2

conn_dict = dict(st.secrets["prod_conn_info"])

with psycopg2.connect(**conn_dict) as conn:

    tab2, tab1 = st.tabs([ "Explore Listings","Real Estate Analytics"])

    with tab1:
        with conn.cursor() as cur:
            st.header("Prague Apartment Rentals")
            st.subheader("Rent per District (Top 15)")
            with st.spinner("Loading data..."):
                df_rent_district = pd.read_sql_query("select * from gold_rental_avg_per_district order by avg_rent_czk desc limit 15", conn)                 
            bar = alt.Chart(df_rent_district).mark_bar(size=15).encode(
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
            with st.spinner("Loading data..."):
                df_rent_layout = pd.read_sql_query("select * from gold_rental_avg_per_layout order by avg_rent_czk desc", conn)
            bar = alt.Chart(df_rent_layout).mark_bar(size=25).encode(
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
            with st.spinner("Loading data..."):
                df_apartment_sale = pd.read_sql_query("select * from gold_sale_avg_per_district order by avg_price_czk desc limit 15", conn)
            bar = alt.Chart(df_apartment_sale).mark_bar(size=15).encode(
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
            with st.spinner("Loading data..."):
                df_price_layout = pd.read_sql_query("select * from gold_sale_avg_per_layout order by avg_price_czk desc", conn)               
                bar = alt.Chart(df_price_layout).mark_bar(size=30).encode(
                    y=alt.Y('property_layout:N', sort='-x', title="Layout", scale=alt.Scale(paddingInner=0.1)),
                    x=alt.X('avg_price_czk:Q', title="Average Price (CZK)")
                ).properties(
                    width=1000,
                    height=30 * len(df_rent_district)
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

        with tab2:
            st.header("Explore Prague Apartment Listings")
            st.markdown("Use the sidebar to filter results. Visit Analytics tab for a market overview.")

            with st.spinner("Loading detailed listings..."):
                df_full = pd.read_sql_query("SELECT * FROM gold_full_listings", conn)

                with st.sidebar:
                    st.header("🧭 Filter Listings")

                    districts = ["All"] + sorted(df_full["property_district"].dropna().unique())
                    layouts = ["All"] + sorted(df_full["property_layout"].dropna().unique())
                    listing_types = ["All"] + sorted(df_full["listing_type"].dropna().unique())

                    selected_district = st.selectbox("District", districts)
                    selected_layout = st.selectbox("Layout", layouts)
                    selected_listing = st.selectbox("Listing Type",listing_types)

                    price_min, price_max = int(df_full["price_czk"].min()), int(df_full["price_czk"].max())
                    price_range = st.slider("Price Range (CZK)", price_min, price_max, (25000, 1000000), step=1000)

                    min_area = st.number_input("Min Area (m²)", value=20)

                df_filtered = df_full.copy()

                if selected_district != "All":
                    df_filtered = df_filtered[df_filtered["property_district"] == selected_district]

                if selected_layout != "All":
                    df_filtered = df_filtered[df_filtered["property_layout"] == selected_layout]

                if selected_listing != "All":
                    df_filtered = df_filtered[df_filtered["listing_type"] == selected_listing]

                df_filtered = df_filtered[
                    (df_filtered["price_czk"] >= price_range[0]) &
                    (df_filtered["price_czk"] <= price_range[1]) &
                    (df_filtered["area_m2"] >= min_area)
                ]

                df_filtered["Listing"] = df_filtered.apply(
                    lambda row: f"[{row['property_title']}]({row['listing_link']})", axis=1
                )

                display_cols = {
                    "Listing": "Listing",
                    "price_czk": "Price (CZK)",
                    "area_m2": "Area (m²)",
                    "property_layout": "Layout",
                    "property_district": "District",
                    "listing_type": "Type"
                }

                df_display = df_filtered[list(display_cols.keys())].rename(columns=display_cols)

                st.write(f"Showing {len(df_display)} matching listings.")
                st.write(df_display.to_markdown(index=False), unsafe_allow_html=True)

