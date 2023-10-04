import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# TODO needs to use Selenium to find_element(). bs4 can't find == $0 elements.


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

        options = webdriver.EdgeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--guest")

        self.driver = webdriver.Edge(options=options)
        self.driver.set_window_size(1700, 1000)

        self.fruit_prices = {}
        self.veg_prices = {}
        self.dairy_prices = {}
        self.meat_prices = {}
        self.grain_prices = {}
        self.bread_prices = {}
        self.prices = [
            self.fruit_prices, self.veg_prices, self.dairy_prices, self.meat_prices,
            self.grain_prices, self.bread_prices
        ]

    def get_prices(self):
        for url in self.urls:
            self.driver.get(url)
            time.sleep(8)

            names = self.driver.find_elements(By.CLASS_NAME, 'e-8zabzc')
            prices = self.driver.find_elements(By.CLASS_NAME, 'screen-reader-only')

            for item in names:
                pos = names.index(item)
                name = item.text
                price = prices[pos].text

                self.fruit_prices[f"{name}"] = price

        self.prices = [
            self.fruit_prices, self.veg_prices, self.dairy_prices, self.meat_prices,
            self.grain_prices, self.bread_prices
        ]
        return self.prices
