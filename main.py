import pandas as pd
from apartment_scraper import RentScraper
from grocery_scraper import GroceryScraper
# TODO 1. Rent price website (average, min and max)
# TODO 2. Gas prices in the city (average)
# TODO 3. Utility prices (average)
# TODO 4. Write this info to a CSV file

rent_scraper = RentScraper()
food_scraper = GroceryScraper()

print("Loading...")
rent_prices = rent_scraper.get_price()
grocery_prices = food_scraper.get_prices()

# Save grocery price data as a CSV file
category_position = 0
with pd.ExcelWriter("grocery_prices.xlsx") as writer:
    for category in grocery_prices:
        category_name = category[category_position]["Category"]
        df = pd.DataFrame(category)
        category_position += 1
        df = df.drop_duplicates()
        df.to_excel(writer, sheet_name=f"{category_name}", index=False)
print("Done")
