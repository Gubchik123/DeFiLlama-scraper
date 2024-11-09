import os
import csv
from time import sleep
from datetime import datetime

from loguru import logger
from dotenv import load_dotenv
from user_agent import generate_user_agent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
)


load_dotenv()

logger.add("scraping.log", rotation="1 MB")

DELAY_MINS = int(os.getenv("DELAY_MINS", "5"))


class DefiLlamaScraper:
    """A web scraper for DeFi Llama's website."""

    def __init__(self):
        """Initializes the web driver and data structures."""
        options = webdriver.ChromeOptions()
        user_agent = generate_user_agent()
        logger.info(f"Using user agent: {user_agent}")
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--disable-blink-features=AutomationControlled")

        if proxy := os.getenv("PROXY_SERVER"):
            logger.info(f"Using proxy server: {proxy}")
            options.add_argument(f"--proxy-server={proxy}")

        self.driver = webdriver.Chrome(options)
        self.processed_rows = set()
        self.data = []

    def load_page(self, url: str):
        """Loads the given URL in the web driver."""
        try:
            self.driver.get(url)
            sleep(5)
        except WebDriverException as e:
            logger.error(f"Error loading page: {e}")
            self.close()
            raise

    def extract_data(self):
        """Extracts the data from the page and stores it in the data structure."""
        try:
            last_height = self.driver.execute_script(
                "return window.innerHeight + window.scrollY"
            )
            while True:
                columns = [
                    element.text
                    for element in self.driver.find_elements(
                        By.CSS_SELECTOR, "div.sc-af4250f5-0.fYBVwr"
                    )
                ]
                for index in range(14, len(columns), 14):
                    row_data = (
                        columns[index].split("\n")[-1],
                        columns[index + 1],
                        columns[index + 6],
                    )
                    if row_data not in self.processed_rows:
                        self.processed_rows.add(row_data)
                        self.data.append(
                            {
                                "Name": row_data[0],
                                "Protocols": row_data[1],
                                "TVL": row_data[2],
                            }
                        )
                self.scroll_page()
                new_height = self.driver.execute_script(
                    "return window.innerHeight + window.scrollY"
                )
                if new_height == last_height:
                    break
                last_height = new_height
        except NoSuchElementException as e:
            logger.error(f"Error extracting data: {e}")
            self.close()
            raise
        except WebDriverException as e:
            logger.error(f"WebDriver error: {e}")
            self.close()
            raise

    def scroll_page(self):
        """Scrolls the page to load more data."""
        try:
            self.driver.execute_script(
                "window.scrollBy(0, window.innerHeight);"
            )
        except WebDriverException as e:
            logger.error(f"Error scrolling page: {e}")
            self.close()
            raise

    def save_to_csv(self, filename: str):
        """Saves the data to a CSV file with the given filename."""
        try:
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["Name", "Protocols", "TVL"]
                )
                writer.writeheader()
                writer.writerows(self.data)
            logger.info(f"Data successfully saved to {filename}")
        except IOError as e:
            logger.error(f"Error saving to CSV: {e}")
            raise

    def close(self):
        """Closes the web driver."""
        try:
            self.driver.quit()
        except WebDriverException as e:
            logger.error(f"Error closing WebDriver: {e}")

    def clear_data(self):
        """Clears the processed rows and data structures."""
        self.processed_rows.clear()
        self.data.clear()


if __name__ == "__main__":
    scraper = DefiLlamaScraper()
    try:
        while True:
            logger.info("Starting new scraping cycle")
            scraper.load_page("https://defillama.com/chains")
            scraper.extract_data()
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
            logger.info(f"Saving data to CSV: {timestamp}.csv")
            scraper.save_to_csv(f"{timestamp}.csv")
            scraper.clear_data()
            logger.info("Scraping cycle completed successfully")
            logger.info(f"Waiting {DELAY_MINS} minutes before next cycle")
            sleep(DELAY_MINS * 60)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        scraper.close()
