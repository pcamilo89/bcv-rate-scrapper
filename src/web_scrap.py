"""
A script that scrapes USD and EUR values from the BCV website (Banco Central de Venezuela)
and saves them to a file.

Authors:
    Camilo Perez <camilop15.cp@gmail.com>

Usage: 
    python web_scrap.py

Requirements:
    pip install beautifulsoup4  (For Python 3.7+)
"""

import os
import sys


from datetime import datetime

from urllib.request import urlopen
from urllib.error import URLError

from ssl import create_default_context, CERT_NONE
from typing import Optional, Tuple

from bs4 import BeautifulSoup

from config import BCV_URL, LOG_FILE, HISTORY_FILE, NOTIFICATION_ENABLED

# from constants import BCV_URL, LOG_FILE, HISTORY_FILE


def show_notification(title: str, subtitle: str, message: str, time: int = 10000):
    """
    Show a notification in the desktop tray

    Args:
        title (str): The title of the notification.
        subtitle (str): The subtitle of the notification.
        message (str): The message of the notification.
    """
    os.system(f'notify-send -a "{title}" -t {time} "{subtitle}" "{message}"')


def scrap_url(url: str) -> Optional[BeautifulSoup]:
    """
    Scrap the HTML code from the provided URL.

    Args:
        url (str): The URL of the website.

    Returns:
        Optional[BeautifulSoup]: The scraped HTML code or None if there was an error.
    """
    try:
        ssl_context = create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = CERT_NONE
        with urlopen(url, timeout=10, context=ssl_context) as response:
            html_code = response.read().decode("utf-8")
    except URLError as e:
        print(e.reason)
        return None
    return BeautifulSoup(html_code, "html.parser")


def get_currency_from_url(url: str) -> Optional[Tuple[datetime, str, str]]:
    """
    Scrap the USD and EUR values from the provided URL

    Args:
        url (str): The URL of the website.

    Returns:
        Optional[Tuple[datetime, str, str]]: A tuple with the date, USD value and EUR value.
    """
    parsed_html = scrap_url(url)
    if parsed_html is None:
        return None
    euro_amount: str = (
        parsed_html.find("div", {"id": "euro"}).find("strong").get_text().strip()
    )
    dolar_amount: str = (
        parsed_html.find("div", {"id": "dolar"}).find("strong").get_text().strip()
    )
    fecha = parsed_html.find("span", {"class": "date-display-single"})
    fecha = fecha["content"].split("T")
    datetime_scrap = datetime.strptime(fecha[0], "%Y-%m-%d")
    return datetime_scrap, euro_amount, dolar_amount


def get_last_line(file_path: str) -> Optional[str]:
    """
    Returns the last non-empty line in a file, or None if the file doesn't exist or is empty.

    Args:
        file_path (str): The path to the file.

    Returns:
        Optional[str]: The last line in the file, or None if the file is empty or doesn't exist.
    """
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            pass
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            return last_line
    return None


def append_to_file(file_path: str, data: str):
    """
    Appends a line to the end of the file, and if the file doesn't exist, it creates it.

    Args:
        file_path (str): The path to the file.
        data (str): The data to append to the file.
    """
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"{data}\n")
    else:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{data}\n")


def main():
    """
    This function is the main entry point of the program. It scrapes the BCV website
    for the USD and EUR values and saves them to a file. It also logs the scraping
    operations to a log file.
    """
    datetime_now = datetime.now()
    date_now = datetime_now.strftime("%Y-%m-%d %H:%M:%S")

    last_line = get_last_line(HISTORY_FILE)
    if last_line is not None:
        line = last_line.split(" ")
        datetime_line = datetime.strptime(line[0], "%Y-%m-%d")
    else:
        datetime_line = datetime(2000, 1, 1)

    if datetime_now > datetime_line:
        response = get_currency_from_url(BCV_URL)
        if response is not None:
            datetime_scrap, euro, dolar = response
            if datetime_scrap > datetime_line:
                string_to_write = date_now
                if len(sys.argv) >= 2:
                    string_to_write = f"{string_to_write} {sys.argv[1]}"
                append_to_file(LOG_FILE, string_to_write)

                date_scrap = datetime_scrap.strftime("%Y-%m-%d")
                string_to_write = f"{date_scrap} EUR {euro} USD {dolar}"
                append_to_file(HISTORY_FILE, string_to_write)
                if NOTIFICATION_ENABLED:
                    show_notification("BCV Dolar", date_scrap, f"USD {dolar}")


if __name__ == "__main__":
    main()
