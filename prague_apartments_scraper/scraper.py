import re
import os
import sys
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
        logging.FileHandler("elt.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

#Set URL for scraping and target location for CSV
url = "https://www.sreality.cz/hledani/byty/praha"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prague_apartments.csv")

#Unique ID per listing generator
def generate_id(*args):
    raw = "||".join(str(arg).strip().lower() for arg in args if arg)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def append_data_to_csv(row):
    df = pd.DataFrame(row)
    df.to_csv(csv_file_path, mode='a', header=not os.path.isfile(csv_file_path), index=False)


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
            for i in range(5):
                if page.locator("li[id^='estate-list-item']").first.is_visible():
                    break
                else:
                    logger.warning("Listings not visible after multiple attempts.")
                    return
            apartments = page.locator("li[id^='estate-list-item']")
            count = apartments.count()
            logger.info(f"{count} apartments found")

            for i in range(count):
                apartment = apartments.nth(i)
                title = apartment.locator("p").nth(0).text_content()
                location = apartment.locator("p").nth(1).text_content()
                price_locator = apartment.locator("p", has_text="Kč")

                if price_locator.count() > 0:
                    price = price_locator.text_content()
                else:
                    logger.warning("Price not available: skipping listing")
                    continue
                
                link = apartment.locator("a[href*='/detail/']")
                href = link.get_attribute("href")
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


                row = {
                    "eventid": generate_id(title,location,type),
                    "title": title,
                    "link": "https://www.sreality.cz/"+href,
                    "location": location,
                    "district": district,
                    "property_type": type,
                    "price_czk": price,
                    "layout": layout,
                    "area_m2": area,
                    "timestamp": datetime.now()
                }
                
                append_data_to_csv([row])
                logger.info(f"Data appeneded:{title} | {location} | {price}")
        

        page_number = 0

        while True:
            page_number += 1
            logger.info(f"Scraping page {page_number}")
        
            extract_apartments()
            logger.info("Apartments extracted")
            
            try:
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

 


def scrape_apartments():
    scrape_data()

if __name__ == "__main__":
    scrape_apartments()

