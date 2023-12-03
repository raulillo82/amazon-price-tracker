import requests
from bs4 import BeautifulSoup
from auth import TELEGRAM_BOT_CHATID, TELEGRAM_BOT_TOKEN

url_amazon = "https://www.amazon.es/Instant-Pot-IP-DUO60-el%C3%A9ctrica-programable/dp/B08Z4HCGDH/"
headers_amazon = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        }

amazon_page = requests.get(url=url_amazon, headers=headers_amazon).text

soup = BeautifulSoup(amazon_page, "lxml")
#print(soup.prettify())

price_whole = soup.find(class_="a-price-whole").getText().split(",")[0]
price_fraction = soup.find(class_="a-price-fraction").getText()
price = float(f"{price_whole}.{price_fraction}")

desired_price = float(input("Please introduce the desired price (€) for "
                            "the item you hardcoded in this program: €"))

if price <= desired_price:
    bot_message = "Amazon price alert!\n"
else:
    bot_message = "Item still too expensive!\n"

bot_message += f"Price as of now is {price}€\n"
bot_message += f"Check {url_amazon}"

params = {
        "chat_id": TELEGRAM_BOT_CHATID,
        "text": bot_message,
        "parse_mode": "MARKDOWN",
        }
url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
response = requests.get(url, params=params)
response.raise_for_status()
#print(response.json())
