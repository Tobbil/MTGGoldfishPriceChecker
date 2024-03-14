import json
import re
import requests

from bs4 import BeautifulSoup

url_base = "https://www.mtggoldfish.com/price/"

with open("cards.json") as file:
    cards = json.load(file)["cards"]

prices = {}

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

    prices.update({card["name"]: price})
      

    