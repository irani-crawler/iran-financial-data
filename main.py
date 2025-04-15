import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from persiantools.jdatetime import JalaliDate
import threading

class PriceScraper:
    def __init__(self, url="https://www.tgju.org/"):
        """
        Initialize the scraper with the target URL and setup DataFrame with English columns.
        """
        self.url = url
        # Mapping of Persian labels to English column names
        self.column_map = {
            "بورس": "Stock",
            "انس طلا": "GoldOunce",
            "مثقال طلا": "GoldMithqal",
            "طلا ۱۸": "Gold18K",
            "سکه": "Coin",
            "دلار": "Dollar",
            "نفت برنت": "BrentOil",
            "تتر": "Tether",
            "بیت کوین": "Bitcoin"
        }
        # DataFrame with additional columns for date and time.
        self.df = pd.DataFrame(columns=list(self.column_map.values()) + ["Date", "Time"])

    def _get_current_time(self):
        """
        Returns the current Jalali date and time in HH:MM:SS format.
        """
        current_time = time.strftime("%H:%M:%S")
        current_date = str(JalaliDate.today())
        return current_date, current_time

    def _clean_text(self, text):
        """
        Clean text by stripping leading and trailing whitespace.
        """
        return text.strip()

    def _scrape_prices(self):
        """
        Scrape price information from the target URL and return a dictionary with the data.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        price_list_container = soup.find('ul', class_='info-bar mobile-hide')
        if not price_list_container:
            raise Exception("Price list container not found on the page.")
        
        # Extract and clean the text elements
        price_text = price_list_container.get_text(separator="\n")
        price_items = [self._clean_text(item) for item in price_text.split("\n")]
        # Filter out blank strings and unwanted elements
        price_items = [item for item in price_items if item and item != ")" and "%" not in item]

        # Build dictionary based on the column map
        data = {}
        for persian_label, english_label in self.column_map.items():
            try:
                index = price_items.index(persian_label)
                data[english_label] = price_items[index + 1]
            except ValueError:
                data[english_label] = None

        # Append current date and time
        current_date, current_time = self._get_current_time()
        data["Date"] = current_date
        data["Time"] = current_time

        return data

    def get_prices(self):
        """
        Retrieve current prices and update the DataFrame with a new row of data.
        """
        try:
            price_data = self._scrape_prices()
            # Create a new DataFrame from the scraped data
            new_row = pd.DataFrame([price_data])
            # Concatenate with the existing DataFrame
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            # Remove rows with missing data
            self.df.dropna(inplace=True)
            # Save updated DataFrame to CSV
            self.df.to_csv("price.csv", index=False)
            print(f"Data scraped at {price_data['Date']} - {price_data['Time']}")
        except Exception as e:
            print(f"Error during scraping: {e}")

    def start_scheduled_scraping(self, iterations=5, interval=60):
        """
        Schedule the scraping to run 'iterations' times, pausing for 'interval' seconds between each scrape.
        This method runs in a separate thread.
        """
        for i in range(iterations):
            print(f"Scraping iteration {i+1} of {iterations}...")
            self.get_prices()
            if i < iterations - 1:
                print(f"Waiting for {interval} seconds before the next scrape...\n")
                time.sleep(interval)
        print("Scheduled scraping complete.")

    def start_thread(self, iterations=5, interval=60):
        """
        Start the scheduled scraping process in a separate thread.
        Returns the Thread object so that the main program can wait on it if desired.
        """
        thread = threading.Thread(target=self.start_scheduled_scraping, args=(iterations, interval))
        thread.start()
        return thread

if __name__ == "__main__":
    # Create an instance of the PriceScraper
    scraper = PriceScraper()
    # Start the scheduled scraping process in a new thread (5 times, every 60 seconds)
    scraping_thread = scraper.start_thread(iterations=5, interval=60)
    # Optionally wait for the thread to finish before exiting the program
    scraping_thread.join()
