import json
import logging
import os
import re
import email
import requests
import smtplib

from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime


def setup_logging():
    app_name = {"app_name": "PriceChecker"}
    logger = logging.getLogger(__name__)
    syslog = logging.StreamHandler()
    formatter = logging.Formatter("[%(app_name)s]: %(message)s")
    syslog.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("./logs.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(syslog)
    logger.addHandler(file_handler)
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
        return None


def calculate_diff(card_name, current_price):
    current_date = datetime.today()
    # ABSTRACT THIS?
    all_reports_dates = [datetime.strptime(file[:8], "%d%m%Y") for file in os.listdir("./reports")]
    last_report_date = min(all_reports_dates, key=lambda x: abs(x - current_date))

    if current_price:
        try:
            with open(f"reports/{last_report_date.strftime('%d%m%Y')}.json", "r") as file:
                last_report = json.load(file)
                last_price = last_report["prices"][card_name]
                diff = round(current_price - last_price, ndigits=2)
                return diff, last_report_date.strftime("%d-%m-%Y")
        except FileNotFoundError:
            print("FILE NOT FOUND")
            return None
    else:
        return None

calculate_diff("As Foretold", 10)
    
def email_report():
    pass
