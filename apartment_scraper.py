import requests
from bs4 import BeautifulSoup


class RentScraper:

    def __init__(self):

        self.apartment_url = "https://www.zillow.com/seattle-wa/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B" \
                             "%22north%22%3A47.80583778225086%2C%22east%22%3A-122.14910203027345%2C%22south%22%3A47" \
                             ".41978724907133%2C%22west%22%3A-122.54048996972658%7D%2C%22mapZoom%22%3A11%2C" \
                             "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A414517" \
                             "%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp" \
                             "%22%3A%7B%22max%22%3A2200%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B" \
                             "%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value" \
                             "%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22" \
                             "%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22usersSearchTerm%22%3A%22Seattle%20WA" \
                             "%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A16037%2C%22regionType%22%3A6%7D%5D" \
                             "%2C%22pagination%22%3A%7B%7D%7D"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"
        self.accent_language = "en-US,en;q=0.9"
        self.header = {
            "User-Agent": self.user_agent,
            "Accept-Language": self.accent_language
        }

        response = requests.get(self.apartment_url, headers=self.header)
        self.soup = BeautifulSoup(response.content, "html.parser")

        self.prices = []
        self.addresses = []
        self.urls = []
        self.rental_data = []

    def get_price(self):
        listings = self.soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 "
                                                          "iMKTKr")
        for apartment in listings:
            price = apartment.text.split("+")[0].split("/")[0]
            self.prices.append(price)
        return self.prices

    def get_address(self):
        listings = self.soup.find_all(name="address")
        for apartment in listings:
            address = apartment.text
            self.addresses.append(address)
        return self.addresses

    def get_url(self):
        listings = self.soup.find_all(name="a", class_="StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW "
                                                       "property-card-link")
        for apartment in listings:
            url_text = apartment['href']
            if "https://www.zillow.com/" not in url_text:
                url = f"https://www.zillow.com{url_text}"
            else:
                url = url_text
            self.urls.append(url)
        return self.urls

    def get_data(self):
        prices = self.get_price()
        addresses = self.get_address()
        urls = self.get_url()

        for num in range(0, len(prices) - 1):
            apartment = {
                "Price": prices[num],
                "Address": addresses[num],
                "URL": urls[num]
            }
            self.rental_data.append(apartment)
        return self.rental_data
