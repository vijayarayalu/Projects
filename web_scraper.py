import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import json
import logging
import time


# Logging Setup 
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Static Scraper (BeautifulSoup + Requests)
def scrape_static_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Example: Extract all headlines (edit based on your target site)
        headlines = [h.get_text(strip=True) for h in soup.find_all("h2")]

        logging.info(f"Scraped {len(headlines)} headlines from {url}")
        return headlines

    except Exception as e:
        logging.error(f"Error scraping static page {url}: {e}")
        return []


#  Dynamic Scraper (Selenium) 
def scrape_dynamic_page(url):
    try:
        # Adjust path to your ChromeDriver
        service = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        driver.get(url)
        time.sleep(3)  # wait for JS to load

        # Example: Extract job titles (edit based on your target site)
        elements = driver.find_elements(By.TAG_NAME, "h2")
        jobs = [el.text for el in elements if el.text.strip()]

        logging.info(f"Scraped {len(jobs)} items from {url} using Selenium")
        driver.quit()
        return jobs

    except Exception as e:
        logging.error(f"Error scraping dynamic page {url}: {e}")
        return []


#  Save Data
def save_to_csv(data, filename="output.csv"):
    df = pd.DataFrame(data, columns=["Data"])
    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")


def save_to_json(data, filename="output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f"Data saved to {filename}")



if __name__ == "__main__":
    print("Choose mode:")
    print("1. Scrape Static Page (BeautifulSoup)")
    print("2. Scrape Dynamic Page (Selenium)")
    choice = input("Enter choice (1 or 2): ")

    url = input("Enter URL to scrape: ")

    if choice == "1":
        data = scrape_static_page(url)
    elif choice == "2":
        data = scrape_dynamic_page(url)
    else:
        print("Invalid choice!")
        exit()

    if data:
        print(f"[INFO] Extracted {len(data)} items.")
        save_to_csv(data, "scraped_data.csv")
        save_to_json(data, "scraped_data.json")
    else:
        print("[INFO] No data found.")

