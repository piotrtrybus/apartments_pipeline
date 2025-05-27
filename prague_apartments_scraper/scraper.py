import re
import os
from playwright.sync_api import sync_playwright
import pandas as pd
from time import sleep
import queue
import logging
import hashlib
from datetime import datetime


#Logger setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

#Set URL for scraping and target location for CSV
url = "https://www.sreality.cz/hledani/byty/praha"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prague_apartments.csv")

data = []

#Unique ID per listing generator
def generate_id(*args):
    raw = "||".join(str(arg).strip().lower() for arg in args if arg)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def scrape_data():
    logger.info("Scraping initiated")
    with sync_playwright() as p:
        logger.info("Launching new browser Chromium")
        browser = p.chromium.launch() 
        page = browser.new_page()
        logger.info(f"Redirecting to URL: {url}")
        page.goto(url) 

        logger.info("Loading page")
        page.wait_for_load_state() 
        page.wait_for_timeout(1000)
        logger.info("Page loaded")

        consent = page.locator("button", has_text = "Souhlasím")
        page.wait_for_timeout(3000)

        if consent: #Handle consent form upon page load
            consent.click(force=True) #Proceed to listings
            page.wait_for_timeout(2000)
            logger.info("Proceeded through consent page")

        def extract_apartments():
            apartments = page.query_selector_all("div.css-18g5ywv")
            logger.info(f"{len(apartments)} Apartments fetched")

            for apartment in apartments:
                title = apartment.query_selector("p.css-d7upve:nth-child(1)").text_content()
                location = apartment.query_selector("p.css-d7upve:nth-child(2)").text_content()
                price = apartment.query_selector("p.css-ca9wwd").text_content()
                #Initiate variables
                layout = None
                type = None
                area = None
            
                if 'Pronájem' in title:
                    type = 'For Rent'
                    match_price = re.search(r"(\d+\s?\d+)", price)

                    
                    if match_price:
                        price = match_price.group().replace("\xa0", "").replace(" ", "")
                    else:
                        price = None

                    if price and price.isdigit():
                        price = int(price)
                    else:
                        price = 0


                elif 'Prodej' in title:
                    type = 'For Sale'
                    match_price = re.search(r"[\d\s]+",price)
                    
                    if match_price:
                        price = match_price.group().replace("\xa0", "").replace(" ", "")
                    else:
                        price = None

                    if price and price.isdigit():
                        price = int(price)
                    else:
                        price = 0
                
                match_location = re.search("(?<=-\s).*$",location)

                if match_location:
                    district = match_location.group()
                else:
                    district = None

                match_title = re.search(r"(\d+\+\w+)\s+(\d+)\s*m(?:\^?2|²)",title,re.IGNORECASE)

                if match_title:
                    layout = match_title.group(1) 
                    area = match_title.group(2)
                else:
                    match_alt = re.search(r"(\w+)\D*(\d+)\s*m(?:\^?2|²)", title, re.IGNORECASE)
                    if match_alt:
                        layout = match_alt.group(1)
                        area = match_alt.group(2)
                    else:
                        layout = None
                        area = None


                data.append({
                    "eventid": generate_id(title,location,type),
                    "title": title,
                    "location": location,
                    "district": district,
                    "property_type": type,
                    "price_czk": price,
                    "layout": layout,
                    "area_m2": area,
                    "timestamp": datetime.now()
                })
                
                logger.info("Data appeneded.")
                    
        

        page_number = 0

        while True:
            page_number += 1
            logger.info(f"Scraping page {page_number}")

            extract_apartments()
            logger.info("Apartments extracted")
            
            try:
                next_page_button = page.locator("button",has_text="Další stránka")
                next_page_button = page.locator("button",has_text="Další stránka")
                next_page_button.wait_for(state="visible")
                next_page_button.scroll_into_view_if_needed()

                if next_page_button.is_visible():    
                    next_page_button.click(force=True)
                    page.wait_for_timeout(2000)
                else:
                    logger.warning("No more pages to scrape - exiting loop.")
                    break
            except:
                logger.warning("No more pages to scrape. Stopping")
                break

        browser.close()



def save_data():
    # Check if the file exists to determine if the header should be written
    file_exists = os.path.isfile(csv_file_path)
    
    if data:
        df = pd.DataFrame(data)
        df.to_csv(csv_file_path, mode='a', header=not file_exists, index=False)
        logger.info(f"Data saved to CSV. Total rows: {len(df)}")
    else:
        logger.error("No data, save skipped")
 


def main():
    scrape_data()
    save_data()

main()

