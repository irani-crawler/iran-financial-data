# PriceScraper

PriceScraper is a Python tool designed to scrape pricing data from [tgju.org](https://www.tgju.org/) at scheduled intervals. The tool collects several market indicators such as stock, gold prices, coin values, dollars, Brent Oil, tether, and Bitcoin. The scraped data is saved into a CSV file for later analysis. The tool uses threading to run the scraping process without blocking the main program.

## Features

- **Scheduled Scraping:**  
  Retrieve data a specified number of times (default 5 iterations) with a 60-second interval between scrapes.

- **Data Processing:**  
  Cleans and parses the scraped HTML using BeautifulSoup.

- **Data Storage:**  
  Collected data is appended to a Pandas DataFrame with English column names and saved to a CSV file (`price.csv`).

- **Threading:**  
  Uses the Python `threading` module to run the scraping process in a separate thread.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/irani-crawler/iran-financial-data.git
   cd PriceScraper
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   **Required Packages:**

   - `requests`
   - `beautifulsoup4`
   - `pandas`
   - `persiantools` (for converting dates)

   If you do not have a `requirements.txt` file, you can install them individually:

   ```bash
   pip install requests beautifulsoup4 pandas persiantools
   ```

## Usage

Run the script directly to start the scheduled scraping:

```bash
python price_scraper.py
```

The script will perform 5 iterations of scraping, each 60 seconds apart by default. You can adjust the number of iterations or the interval by modifying the arguments when calling the `start_thread` method in the `if __name__ == "__main__":` block.

### Code Overview

- **PriceScraper Class:**  
  This class encapsulates all functionality to scrape data, update a DataFrame, and save it to `price.csv`. The major methods include:
  
  - `_scrape_prices`: Scrapes the pricing data from the target URL.
  - `get_prices`: Appends the newly scraped data to the DataFrame and writes to a CSV file.
  - `start_scheduled_scraping`: Runs the scraping in a loop with a delay between each iteration.
  - `start_thread`: Launches the scheduled scraping using threading.

- **Threaded Execution:**  
  The tool uses threading to run the scraping task asynchronously. This ensures that the main thread remains responsive.

## Troubleshooting

- **Scraping Errors:**  
  If you encounter errors such as "Price list container not found on the page," ensure the target website has not changed its page structure. You may need to update the BeautifulSoup selectors accordingly.


## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with improvements.

## License

This project is open source and available under the [MIT License](LICENSE).

