import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL with page number
BASE_URL = "https://www.phishtank.com/phish_search.php?page="

# CSV file to save results
csv_file = 'phish_urls.csv'

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

# List to hold all URLs
phish_urls = []

# Number of pages to scrape (change as needed)
NUM_PAGES = 5

for page in range(NUM_PAGES):
    url = f"{BASE_URL}{page}"
    print(f"Scraping page {page + 1}: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all table rows with phishing URLs
    table_rows = soup.select("table tr")[1:]  # Skip header row

    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            link_tag = cols[1].find('a')
            if link_tag and 'href' in link_tag.attrs:
                phish_url = link_tag.get_text(strip=True)
                phish_urls.append([phish_url])

    time.sleep(1)  # Be nice to the server

# Save to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Phish URL'])
    writer.writerows(phish_urls)

print(f"\n Scraped {len(phish_urls)} phishing URLs into '{csv_file}'")
