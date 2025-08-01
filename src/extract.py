from dataclasses import dataclass
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import re
import time

@dataclass
class CarBrand:
    logo: str
    name: str
    
load_dotenv()
url = os.getenv("SITE_URL")

params = {
    "page": 0,
    "search_text": "",
    "order": "owner_count",
    "view": "list_cards"
}

headers = {
    "Content-Type": "application/json"
}

car_brands = []

while True:
    print(f"Fetching page {params['page']}")
    response = requests.get(url, params = params, headers = headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    data = response.json()

    if not data.get("brand_recs_html"):
        print("End of data fetching.")
        break

    soup = BeautifulSoup(data.get("brand_recs_html"), "html.parser")
    car_brands_html = soup.select('div.brand_item')

    for brand_html in car_brands_html:
        def extract_logo_url(html_link):
            style = html_link.get('style')
            if not style:
                return None
            
            match = re.search(r"background-image:\s*url\(['\"]?(.*?)['\"]?\)", style)
            if match:
                return match.group(1)
            else:
                return None
    
        contents = brand_html.find_all("a")

        if len(contents) == 2:
            logo = extract_logo_url(contents[0])
            name = contents[1].string
        else:
            logo = None
            name = contents[0].string
        
        print(logo, name)
        car_brands.append(CarBrand(logo=logo, name=name))
    
    params["page"] += 1
    time.sleep(2)