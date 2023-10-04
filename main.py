from apartment_scraper import RentScraper
from grocery_scraper import GroceryScraper
# TODO 1. Rent price website (average, min and max)
# TODO 2. Gas prices in the city (average)
# TODO 3. Utility prices (average)
# TODO 4. Write this info to a CSV file

rent_scraper = RentScraper()
scraper = GroceryScraper()

rent = rent_scraper.get_price()
prices = scraper.get_prices()
print(rent)
print(prices)
