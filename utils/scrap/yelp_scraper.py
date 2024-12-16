import requests
from bs4 import BeautifulSoup
import json

# URL of the Yelp menu page
url = "https://www.yelp.com/menu/chennai-dosas-hicksville"

# Fetch the page content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# List to store menu items
menu_items = []

# Find all sections with menu items
menu_sections = soup.find_all("div", class_="menu-item")

for section in menu_sections:
    # Extract the name of the menu item
    name_tag = section.find('h4')
    name = name_tag.get_text(strip=True) if name_tag else None

    # Extract the price
    price_tag = section.find('li', class_='menu-item-price-amount')
    price = float(price_tag.get_text(strip=True).replace(
        '$', '')) if price_tag else None

    # Extract the item link (if available)
    link_tag = section.find('a')
    link = link_tag['href'] if link_tag else None

    # Append to the list if name and price are available
    if name and price:
        menu_items.append({
            "name": name,
            "price": price,
            "link": f"https://www.yelp.com{link}" if link else None
        })

# Convert to JSON
menu_json = json.dumps({"menu": menu_items}, indent=4)

# Output the JSON
print(menu_json)
with open('chennai-dosas-hicksville.json', 'w') as outfile:
    json.dump({"menu": menu_items}, outfile, indent=4)
