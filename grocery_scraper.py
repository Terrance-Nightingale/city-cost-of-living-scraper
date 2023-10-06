import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class GroceryScraper:

    def __init__(self):

        self.fruit_url = "https://delivery.metropolitan-market.com/store/metropolitan-market" \
                                 "/collections/fresh-fruits"
        self.veg_url = "https://delivery.metropolitan-market.com/store/metropolitan-market" \
                               "/collections/fresh-vegetables"
        self.dairy_url = "https://delivery.metropolitan-market.com/store/metropolitan-market" \
                                 "/collections/dairy"
        self.meat_url = "https://delivery.metropolitan-market.com/store/metropolitan-market" \
                                "/collections/meat-and-seafood"
        self.grains_url = "https://delivery.metropolitan-market.com/store/metropolitan-market" \
                                  "/collections/dry-goods-pasta"
        self.bread_url = "https://delivery.metropolitan-market.com/store/metropolitan-market" \
                                 "/collections/baked-goods"

        self.urls = [
            self.fruit_url, self.veg_url, self.dairy_url,
            self.meat_url, self.grains_url, self.bread_url
        ]
        self.categories = [
            "Fruits", "Vegetables", "Dairy", "Meat", "Grain", "Bread"
        ]

        options = webdriver.EdgeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--guest")

        self.driver = webdriver.Edge(options=options)
        self.driver.set_window_size(1700, 1000)

        self.fruit_prices = []
        self.veg_prices = []
        self.dairy_prices = []
        self.meat_prices = []
        self.grain_prices = []
        self.bread_prices = []
        self.prices = [
            self.fruit_prices, self.veg_prices, self.dairy_prices,
            self.meat_prices, self.grain_prices, self.bread_prices
        ]

        self.category_pos = 0

    def get_prices(self):
        for url in self.urls:
            self.driver.get(url)
            time.sleep(10)
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(2)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            names = self.driver.find_elements(By.CLASS_NAME, 'e-8zabzc')
            prices = self.driver.find_elements(By.CLASS_NAME, 'screen-reader-only')

            for item in names:
                pos = names.index(item)
                name = item.text
                price = prices[pos].text
                category = self.categories[self.category_pos]

                item_price = {
                    "Category": category,
                    "Item": name,
                    "Price": price
                }
                self.prices[self.category_pos].append(item_price)
            self.category_pos += 1

        self.prices = [
            self.fruit_prices, self.veg_prices, self.dairy_prices, self.meat_prices,
            self.grain_prices, self.bread_prices
        ]

        return self.prices
