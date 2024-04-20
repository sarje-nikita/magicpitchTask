# YellowPages UAE Restaurant Scraper

## Introduction

This project is an assignment to scrape business listings from the YellowPages UAE website. The script collects information such as business name, location, contact details, and logo URLs for restaurants listed on the website. It automates the process of data collection and saves the results to a CSV file for further analysis. The script is available in both normal and multithreading versions.

## Table of Contents
- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Output](#output)


## Dependencies

- Python 3.x
- BeautifulSoup4
- Requests

## Usage

### Normal Version
1. Clone the repository:
    ```
    git clone https://github.com/sarje-nikita/magicpitchTask.git
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the script:
    ```
    python scrape_yellowpages.py
    ```

4. The scraped data will be saved to a file named `yellowpages_data.csv`.

### Multithreading Version
1. Clone the repository:
    ```
    git clone https://github.com/sarje-nikita/magicpitchTask.git
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the script:
    ```
    python scrape_yellowpages_multithreading.py
    ```

4. The scraped data will be saved to a file named `yellowpages_data.csv`.

## Output

The script generates a CSV file containing the following fields for each business listing:

- Name
- Location
- City
- P.O Box
- Phone
- Company Page Link
- Logo URL

