import json
import logging
import re
import sys
import requests

from datetime import date
from bs4 import BeautifulSoup

#TODO: SETUP LOGGING

current_date = date.today()
url_base = "https://www.mtggoldfish.com/price/"

with open("cards.json") as file:
    cards = json.load(file)["cards"]

prices = {"date": current_date.strftime("%d-%m-%Y"), "prices": {}, "diff": {}}

for card in cards:
    card_name = card["name"].replace("_", "+")
    if card["foil"] == True:
        url = url_base + card["expansion"] + ":Foil/" + card_name
    else:
        url = url_base + card["expansion"] + "/" + card_name

    req = requests.get(url)
    soup = BeautifulSoup(req.content, features="html.parser")

    price_div = soup.select(".price-box-price")[0]
    price_pattern = re.compile(r'[^\d.]+')
    price = price_pattern.sub("", price_div.text)

    prices["prices"].update({card["name"]: price})
    #TODO: wyliczenie diff z wczoraj i dodanie do dicta
    print(prices)

with open(f"reports/{current_date.strftime('%d%m%Y')}.json", "w") as file:
    json.dump(prices, file)

