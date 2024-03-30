import json
import logging
import re
import email
import requests
import smtplib

from bs4 import BeautifulSoup
from datetime import date, timedelta

def setup_logging():
    app_name = {"app_name": "PriceChecker"}
    logger = logging.getLogger(__name__)
    syslog = logging.StreamHandler()
    formatter = logging.Formatter("[%(app_name)s]: %(message)s")
    syslog.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(syslog)
    logger = logging.LoggerAdapter(logger, app_name)

    return logger

def get_price_from_site(url):
    try:
        class_name = ".price-box-price"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, features="html.parser")

        price_div = soup.select(class_name)[0]
        price_pattern = re.compile(r'[^\d.]+')
        price = float(price_pattern.sub("", price_div.text))
        return price
    except IndexError: 
        print("Couldn't get price (typo in name?)! Setting to $0")
        return 0


def calculate_diff(card_name, current_price):
    current_date = date.today()
    last_report_date = (current_date - timedelta(days = 7)).strftime("%d%m%Y")
    try:
        with open(f"reports/{last_report_date}.json", "r") as file:
            last_report = json.load(file)
            last_price = last_report["prices"][card_name]
            delta = round(((current_price - last_price) / last_price) * 100, ndigits=2)
    except FileNotFoundError:
        return None

    return delta

def email_report():
    pass
