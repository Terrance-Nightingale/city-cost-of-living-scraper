import pandas as pd
from apartment_scraper import RentScraper
from grocery_scraper import GroceryScraper
from transport_scraper import TransportScraper
# TODO 2. Gas prices in the city (average)
# TODO 3. Utility prices (average)

print("Loading...")

# Grab apartment data
rent_scraper = RentScraper()
rental_data = rent_scraper.get_data()

# Grab grocery data
food_scraper = GroceryScraper()
grocery_prices = food_scraper.get_prices()

# Grab transport data
t_scraper = TransportScraper()
transport_prices = t_scraper.get_pubtrans_prices()
gas_prices = t_scraper.get_gas_prices()

# Save apartment price data as a xlsx file
with pd.ExcelWriter("rental_data.xlsx") as writer:
    df = pd.DataFrame(rental_data)
    df = df.drop_duplicates()
    df.to_excel(writer, sheet_name="Data", index=False)

# Save grocery price data as a xlsx file
category_position = 0
with pd.ExcelWriter("grocery_prices.xlsx") as writer:
    for category in grocery_prices:
        category_name = category[category_position]["Category"]
        df = pd.DataFrame(category)
        category_position += 1
        df = df.drop_duplicates()
        df.to_excel(writer, sheet_name=f"{category_name}", index=False)

# Save transport price data as a xlsx file
with pd.ExcelWriter("transport_data.xlsx") as writer:
    df = pd.DataFrame(transport_prices)
    df.to_excel(writer, sheet_name="Public_Transport", index=False)

    df = pd.DataFrame(gas_prices)
    df.to_excel(writer, sheet_name="Gas", index=False)

print("Done")
