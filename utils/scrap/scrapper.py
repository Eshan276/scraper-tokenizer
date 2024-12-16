import requests
from bs4 import BeautifulSoup
import json


def scrape_food_items(url):
    try:
        # Send a GET request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product cards
        food_items = []

        # Adjust this selector based on the actual website
        cards = soup.select('.card')

        for card in cards:
            print(card)
            # Extract food item details
            # Modify these selectors based on the actual website's HTML structure
            name_tag = card.find('h5')
            description_tag = card.find(
                'span', style=lambda value: value and 'text-align: center;' in value)
            price_tag = card.find('div', class_='text-muted')

            if name_tag and description_tag and price_tag:
                name = name_tag.get_text(strip=True)
                description = description_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)

                food_item = {
                    'name': name,
                    'description': description,
                    'price': price
                }

                food_items.append(food_item)
            else:
                print(f"Skipping card due to missing information: {card}")

        return food_items

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []


# URL of the website
url = 'https://www.villagesoulofindia.com/app/order/menu'

# Scrape food items
scraped_items = scrape_food_items(url)

# Print or save the results
print(json.dumps(scraped_items, indent=2))

# Optionally, save to a JSON file
with open('food_items.json', 'w') as outfile:
    json.dump(scraped_items, outfile, indent=2)
