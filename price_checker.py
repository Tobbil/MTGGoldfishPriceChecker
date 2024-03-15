import json
import logging

from datetime import date

from helpers import calculate_diff, get_price_from_site

#TODO: SETUP LOGGING
app_name = {"app_name": "PriceChecker"}
LOGGER = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter("[%(app_name)s]: %(message)s")
syslog.setFormatter(formatter)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(syslog)
LOGGER = logging.LoggerAdapter(LOGGER, app_name)

current_date = date.today()
url_base = "https://www.mtggoldfish.com/price/"

with open("cards.json") as file:
    cards = json.load(file)["cards"]

prices = {"date": current_date.strftime("%d-%m-%Y"), "prices": {}, "diff": {}}

for card in cards:
    card_name = card["name"].replace("_", "+")
    url = url_base + card["expansion"] + (":Foil/" if card["foil"] else "/") + card_name

    LOGGER.info(f"Checking price for {card['name']}")
    price = get_price_from_site(url)
    LOGGER.info(f"Price: ${price}")
    prices["prices"].update({card["name"]: price})

    LOGGER.info(f"Checking price difference for {card['name']}")
    diff = calculate_diff(card["name"], price)
    LOGGER.info(f"Price difference: {'+' if diff >= 0 else ''}{diff}%")
    prices["diff"].update({card["name"]: diff})

with open(f"reports/{current_date.strftime('%d%m%Y')}.json", "w") as file:
    LOGGER.info(f"Writing report to file: {file.name}")
    json.dump(prices, file)

