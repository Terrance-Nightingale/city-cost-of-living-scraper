import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class TransportScraper:

    def __init__(self):

        self.public_url = "https://kingcounty.gov/en/dept/metro/fares-and-payment/prices"
        self.gas_url = "https://gasprices.aaa.com/?state=WA"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"
        self.accent_language = "en-US,en;q=0.9"
        self.header = {
            "User-Agent": self.user_agent,
            "Accept-Language": self.accent_language
        }

        r = requests.get(self.public_url, headers=self.header)
        self.soup = BeautifulSoup(r.content, "html.parser")

        options = webdriver.EdgeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--guest")

        self.driver = webdriver.Edge(options=options)
        self.driver.set_window_size(1700, 1000)

        self.public_prices = []
        self.gas_prices = []

    def get_pubtrans_prices(self):
        price_tiers = self.soup.find_all(class_="pricing-toggle-head pricing-block-title pricing-with-description")
        ride_type = self.soup.find_all(class_="pricing-block-item")
        prices = self.soup.find_all(class_="pricing-block-price")

        current_tier = 0
        for tier in price_tiers:
            tier_to_add = {
                "Tier": tier.text,
                "Ride": ride_type[current_tier].text.split("$")[0].strip(),
                "Price": prices[current_tier].text
            }
            self.public_prices.append(tier_to_add)
            current_tier += 1
        return self.public_prices

    def get_gas_prices(self):
        self.driver.get(self.gas_url)
        time.sleep(5)
        price_button = self.driver.find_element(By.XPATH, '//*[@id="ui-id-15"]')

        price_button.click()
        time.sleep(2)
        prices = self.driver.find_elements(By.XPATH, '//*[@id="ui-id-16"]/div[1]/table/tbody')
        clean_prices = prices[0].text.split("\n")
        for line in clean_prices:
            split_line = line.split(".", 1)
            timeframe = split_line[0]
            prices = split_line[1].strip().split(" ")
            print(line)
            print(timeframe)
            print(prices)
            line_to_add = {
                "Timeframe": timeframe,
                "Regular": prices[0],
                "Mid": prices[1],
                "Premium": prices[2],
                "Diesel": prices[3]
            }
            self.gas_prices.append(line_to_add)
        return self.gas_prices



