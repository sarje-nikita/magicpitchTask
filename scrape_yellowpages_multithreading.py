import requests
from bs4 import BeautifulSoup
import csv
import threading
import time

def scrape_page(base_url, page_num, businesses):
    url = f"{base_url}-{page_num}.html"
    print(f"Scraping page {page_num}...")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.select('.row.box.foc')
        for listing in listings:
            try:
                business = {}
                name_elem = listing.find('h2', class_='cmp_name')
                if name_elem:
                    business['Name'] = name_elem.text.strip()
                
                address_elem = listing.find(itemprop='address')
                if address_elem:
                    street_elem = address_elem.find(itemprop='streetAddress')
                    locality_elem = address_elem.find(itemprop='addressLocality')
                    if street_elem and locality_elem:
                        business['Location'] = f"{street_elem.text.strip()}, {locality_elem.text.strip()}"
                        business['City'] = locality_elem.text.strip()
                        business['P.O Box'] = address_elem.find(class_='pobox').text.strip() if address_elem.find(class_='pobox') else ''
                
                phone_elem = listing.find(class_='phone')
                if phone_elem:
                    business['Phone'] = phone_elem.text.strip()
                
                link_elem = listing.find('a', href=True)
                if link_elem:
                    business['Company Page Link'] = 'https://www.yellowpages-uae.com' + link_elem['href']
                
                img_elem = listing.find('img', src=True)
                if img_elem:
                    business['Logo URL'] = 'https://media.yellowpages-uae.com' + img_elem['src']
                
                businesses.append(business)
                print(business)
            except Exception as e:
                print(f"Error: {e}")

def scrape_yellowpages(base_url):
    businesses = []
    threads = []
    for page_num in range(1, 67):  # Scraping pages from 2 to 66
        thread = threading.Thread(target=scrape_page, args=(base_url, page_num, businesses))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

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
    print(f"Scraping completed. Data saved to yellowpages_data.csv in {end-start}")
