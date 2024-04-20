import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_yellowpages(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1'
    }
    businesses = []
    with requests.Session() as session:  # Use session for persistent connection
        session.headers.update(headers)  # Update session headers

        for page_num in range(1, 67):  # Scraping pages from 2 to 66
            url = f"{base_url}-{page_num}.html"
            print(f"Scraping page {page_num}...")
            response = session.get(url)  # Use session for making requests
            print(response.status_code)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all listings directly
            listings = soup.select('.row.box.foc')

            for listing in listings:
                try:
                    business = {}
                    business['Name'] = listing.find(
                        'h2', class_='cmp_name').text.strip()

                    # Combine parsing of address elements
                    address_elem = listing.find(itemprop='address')
                    if address_elem:
                        business['Location'] = f"{address_elem.find(itemprop='streetAddress').text.strip()}, {address_elem.find(itemprop='addressLocality').text.strip()}"
                        business['City'] = address_elem.find(
                            itemprop='addressLocality').text.strip()
                        business['P.O Box'] = address_elem.find(
                            class_='pobox').text.strip() if address_elem.find(class_='pobox') else ''

                    business['Phone'] = listing.find(
                        class_='phone').text.strip()
                    business['Company Page Link'] = 'https://www.yellowpages-uae.com' + \
                        listing.find('a')['href']
                    business['Logo URL'] = 'https://media.yellowpages-uae.com' + \
                        listing.find('img')['src']
                    print(business)
                    businesses.append(business)
                except Exception as e:
                    print(f"Error: {e}")
                # time.sleep(1)

    return businesses


def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


if __name__ == "__main__":
    start = time.time()
    base_url = "https://www.yellowpages-uae.com/uae/restaurant"
    data = scrape_yellowpages(base_url)
    save_to_csv(data, "yellowpages_data.csv")
    end = time.time()
    print(
        f"Scraping completed. Data saved to yellowpages_data.csv in {end-start}")
