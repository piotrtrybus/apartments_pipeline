**Prague Apartments Analytics**

This project consists a lightweight data pipeline for collecting, transforming, and visualizing apartment listings in Prague from sreality.cz.

**1. Data Ingestion (Scraping)**
Apartment data is scraped using Playwright and saved to a raw CSV file.
Scheduled and orchestrated using GitHub Actions.

**2. Data Transformation (ELT)**
CSV is ingested into DuckDB using dbt.
Follows the medallion architecture:
- Bronze: raw → cleaned + deduplicated
- Silver: enriched + split by listing type
- Gold: analytics-ready tables (4 models)
  
Includes schema management, Jinja templating, and tests via dbt.

**3.Visualization**
Final datasets are visualized with Streamlit and Altair.

Tech Stack:
- **Scraping:** Playwright
- **Orchestration:** GitHub Actions
- **Transformation:** dbt + DuckDB
- **Logging**: Python logging module
- **Metadata**: dbt docs
- **Visualisation:** Streamlit & Altair

DBT Lineage:
![Lineage](lineage.png)
