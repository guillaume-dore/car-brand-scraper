from dataclasses import dataclass
import os
from typing import cast
from bs4.element import Tag
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import re
import time

@dataclass
class CarBrand:
    logo: str | None
    name: str

def extract_logo_url(html_link: Tag) -> str | None:
    style = html_link.get('style')
    if not style:
        return None
    
    match = re.search(r"background-image:\s*url\(['\"]?(.*?)['\"]?\)", str(style))
    if match:
        return match.group(1)
    else:
        return None
    
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
    if url is None:
        print("SITE_URL is not set in the environment variables.")
        break
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
        contents = brand_html.find_all("a")

        if len(contents) == 2:
            logo = extract_logo_url(cast(Tag, contents[0]))
            name = contents[1].get_text(strip=True)
        else:
            logo = None
            name = contents[0].get_text(strip=True)

        print(logo, name)
        car_brands.append(CarBrand(logo=logo, name=name))
    
    params["page"] += 1
    time.sleep(2)

print("Exit program.")