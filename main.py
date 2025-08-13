import requests
from bs4 import BeautifulSoup
import time
import random
from googletrans import Translator
import asyncio
import re
from currency_converter import CurrencyConverter
from datetime import datetime, date, timezone
import time
from zoneinfo import ZoneInfo
import pytz
from psycopg2 import DATETIME

import price_charting_card
import pokemon_card
import website_link
import card_market_stats
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
c = CurrencyConverter()

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

cardrushArray = []
cardrushLinks = [
    # website_link.WebsiteLink("sv2a", "https://www.cardrush-pokemon.jp/product-list/0/0/photo?keyword=sv2a&num=100&img=120&order=desc&main_category=&group=&Submit=Narrow+your+search", 165, date(2023, 6, 16)),
    # website_link.WebsiteLink("sv7a", "https://www.cardrush-pokemon.jp/product-group/409?num=100&img=120&order=desc", 64, date(2024, 9, 13)),
    # website_link.WebsiteLink("sv8", "https://www.cardrush-pokemon.jp/product-group/411?num=100&img=120&order=desc", 106, date(2024, 10, 18)),
    # website_link.WebsiteLink("sv8a", "https://www.cardrush-pokemon.jp/product-group/416?num=100&img=120&order=desc", 187, date(2024, 12, 6)),
    # website_link.WebsiteLink("sv9", "https://www.cardrush-pokemon.jp/product-group/427?num=100&img=120&order=desc", 100, date(2025, 1, 24)),
    # website_link.WebsiteLink("sv9a", "https://www.cardrush-pokemon.jp/product-group/449?num=100&img=120&order=desc", 63, date(2025, 3, 14)),
    # website_link.WebsiteLink("sv10", "https://www.cardrush-pokemon.jp/product-group/457?num=100&img=120&order=desc", 98, date(2025, 4, 18)),
    # website_link.WebsiteLink("sv11b", "https://www.cardrush-pokemon.jp/product-list?num=100&img=120&order=price-desc&keyword=sv11b&Submit=search", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("sv11w", "https://www.cardrush-pokemon.jp/product-list?num=100&img=120&order=price-desc&keyword=sv11w&Submit=search", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("m1l", "https://www.cardrush-pokemon.jp/product-list/0/0/photo?keyword=m1l&num=100&img=160&order=desc&main_category=&group=&Submit=Narrow+your+search", 63, date(2025, 8, 1)),
    # website_link.WebsiteLink("m1s", "https://www.cardrush-pokemon.jp/product-list?num=100&img=160&order=price-desc&keyword=m1s&Submit=search", 63, date(2025, 8, 1)),
]

torecaCampArray = []
torecaCampLinks = [
    # website_link.WebsiteLink("sv2a", "https://torecacamp-pokemon.com/collections/sv2a-%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E3%82%AB%E3%83%BC%E3%83%89151?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 165, date(2023, 6, 16)),
    # website_link.WebsiteLink("sv7a", "https://torecacamp-pokemon.com/collections/sv7a-%E6%A5%BD%E5%9C%92%E3%83%89%E3%83%A9%E3%82%B4%E3%83%BC%E3%83%8A?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 64, date(2024, 9, 13)),
    # website_link.WebsiteLink("sv8", "https://torecacamp-pokemon.com/collections/sv8-%E8%B6%85%E9%9B%BB%E3%83%96%E3%83%AC%E3%82%A4%E3%82%AB%E3%83%BC?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 106, date(2024, 10, 18)),
    # website_link.WebsiteLink("sv8a", "https://torecacamp-pokemon.com/collections/sv8a-%E3%83%86%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%AB%E3%83%95%E3%82%A7%E3%82%B9ex?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 187, date(2024, 12, 6)),
    # website_link.WebsiteLink("sv9", "https://torecacamp-pokemon.com/collections/sv9?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 100, date(2025, 1, 24)),
    # website_link.WebsiteLink("sv9a", "https://torecacamp-pokemon.com/collections/sv9a?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 63, date(2025, 3, 14)),
    # website_link.WebsiteLink("sv10", "https://torecacamp-pokemon.com/collections/sv10?filter.v.price.gte=&filter.v.price.lte=&sort_by=price-descending", 98, date(2025, 4, 18)),
    # website_link.WebsiteLink("sv11b", "https://torecacamp-pokemon.com/collections/sv11b?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("sv11w", "https://torecacamp-pokemon.com/collections/sv11w?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("m1l", "https://torecacamp-pokemon.com/collections/m1l?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 63, date(2025, 8, 1)),
    # website_link.WebsiteLink("m1s", "https://torecacamp-pokemon.com/collections/m1s?sort_by=price-descending&filter.v.price.gte=&filter.v.price.lte=", 63, date(2025, 8, 1)),
]

priceChartingArray = []
priceChartingLinks = [
    # website_link.WebsiteLink("sv2a", "https://www.pricecharting.com/console/pokemon-japanese-scarlet-&-violet-151?exclude-hardware=true&exclude-variants=true&in-collection=&model-number=&show-images=true&sort=highest-price&view=grid", 165, date(2023, 6, 16)),
    # website_link.WebsiteLink("sv7a", "https://www.pricecharting.com/console/pokemon-japanese-paradise-dragona?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 64, date(2024, 9, 13)),
    # website_link.WebsiteLink("sv8", "https://www.pricecharting.com/console/pokemon-japanese-super-electric-breaker?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 106, date(2024, 10, 18)),
    # website_link.WebsiteLink("sv8a", "https://www.pricecharting.com/console/pokemon-japanese-terastal-festival?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 187, date(2024, 12, 6)),
    # website_link.WebsiteLink("sv9", "https://www.pricecharting.com/console/pokemon-japanese-battle-partners?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 100, date(2025, 1, 24)),
    # website_link.WebsiteLink("sv9a", "https://www.pricecharting.com/console/pokemon-japanese-heat-wave-arena?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 63, date(2025, 3, 14)),
    # website_link.WebsiteLink("sv10", "https://www.pricecharting.com/console/pokemon-japanese-glory-of-team-rocket?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 98, date(2025, 4, 18)),
    # website_link.WebsiteLink("sv11b", "https://www.pricecharting.com/console/pokemon-japanese-black-bolt?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("sv11w", "https://www.pricecharting.com/console/pokemon-japanese-white-flare?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("m1l", "https://www.pricecharting.com/console/pokemon-japanese-mega-brave?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 63, date(2025, 8, 1)),
    # website_link.WebsiteLink("m1s", "https://www.pricecharting.com/console/pokemon-japanese-mega-symphonia?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 63, date(2025, 8, 1)),
]


hareruyaArray = []
hareruyaLinks = [
    # website_link.WebsiteLink("sv2a", "https://www.hareruya2.com/collections/612?sort_by=price-descending", 165, date(2023, 6, 16)),
    # website_link.WebsiteLink("sv7a", "https://www.hareruya2.com/collections/sv7a?sort_by=price-descending", 64, date(2024, 9, 13)),
    # website_link.WebsiteLink("sv8", "https://www.hareruya2.com/collections/sv8?sort_by=price-descending", 106, date(2024, 10, 18)),
    # website_link.WebsiteLink("sv8a", "https://www.hareruya2.com/collections/sv8a?sort_by=price-descending", 187, date(2024, 12, 6)),
    # website_link.WebsiteLink("sv9", "https://www.hareruya2.com/collections/sv9?sort_by=price-descending", 100, date(2025, 1, 24)),
    # website_link.WebsiteLink("sv9a", "https://www.hareruya2.com/collections/sv9a?sort_by=price-descending", 63, date(2025, 3, 14)),
    # website_link.WebsiteLink("sv10", "https://www.hareruya2.com/collections/sv10?sort_by=price-descending", 98, date(2025, 4, 18)),
    # website_link.WebsiteLink("sv11b", "https://www.hareruya2.com/collections/sv11b?sort_by=price-descending", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("sv11w", "https://www.hareruya2.com/collections/sv11w?sort_by=price-descending", 86, date(2025, 6, 6)),
    # website_link.WebsiteLink("m1l", "https://www.hareruya2.com/collections/701?sort_by=price-descending", 63, date(2025, 8, 1)),
    # website_link.WebsiteLink("m1s", "https://www.hareruya2.com/collections/702?sort_by=price-descending", 63, date(2025, 8, 1)),
]

cardMarketArray = []

connection = psycopg2.connect(
    database = str(os.getenv("DATABASE")),
    user = str(os.getenv("USER")),
    password = str(os.getenv("PASSWORD")),
    host = str(os.getenv("HOST")),
    port = str(os.getenv("PORT")),
)
print("Database Connection Established")

cursor = connection.cursor()


def priceCharting(num):

    query = """
        INSERT INTO price_charting_cards (card_name, price, link, image_link, card_number, card_set, set_amount, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (card_set, card_number)
        DO UPDATE SET 
            card_name = EXCLUDED.card_name,
            price = EXCLUDED.price,
            link = EXCLUDED.link,
            image_link = EXCLUDED.image_link,
            set_amount = EXCLUDED.set_amount,
            last_updated = EXCLUDED.last_updated
    """

    priceChartingSet = priceChartingLinks[num].set
    priceChartingSetAmount = priceChartingLinks[num].setAmount

    priceChartingCurrUrl = priceChartingLinks[num].link
    priceChartingResponse = requests.get(priceChartingCurrUrl, headers=HEADERS)
    priceChartingResponse.encoding = 'utf-8'

    soup = BeautifulSoup(priceChartingResponse.text, 'html.parser')

    cards = soup.find_all('div', attrs={'class': 'item'})

    for card in cards:
        name = card.select_one("div.title a").get_text(strip=True)

        if '#' not in name.lower():
            card_number = "N/A"
        else:
            card_number = re.search(r"(\d+)", name).group(1)

        price = card.select_one('span', attrs={'class': 'price'}).text
        price = re.search(r"\d+.\d+", price).group()

        link = "https://www.pricecharting.com" + card.select_one("div.title a").get("href")

        image = card.select_one("img.photo").get("src")

        if card_number != "N/A" and int(card_number) > int(priceChartingLinks[num].setAmount):
            priceChartingArray.append(
                price_charting_card.PriceChartingCard(
                    name,
                    price,
                    link,
                    image,
                    card_number
                )
            )

            print(name, price, link, image, card_number)

            now_utc = pytz.timezone('US/Eastern')
            print(datetime.now(now_utc))

            params = (
                name,
                price,
                link,
                image,
                card_number,
                priceChartingSet,
                priceChartingSetAmount,
                datetime.now(now_utc)
            )

            # try:
            print(cursor.mogrify(query, params).decode("utf8"))
            cursor.execute(query, params)
            connection.commit()

            # except:
            #     print("Error occured when inserting/updating data in price_charting table")






async def cardrush(num):

    print("Beginning of Cardrush")

    translator = Translator()

    # cardrushListingURL = "https://www.cardrush-pokemon.jp/product-list/0/0/photo?keyword=sv10&num=100&img=120&order=desc&main_category=&group=448&Submit=Narrow+your+search"
    cardrushListingURL = cardrushLinks[num].link
    cardrushSet = cardrushLinks[num].set

    cardrushSetAmount = cardrushLinks[num].setAmount

    query = """
        INSERT INTO cardrush_cards (card_name, price, stock, link, card_number, card_set, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (card_set, card_number)
        DO UPDATE SET 
            card_name = EXCLUDED.card_name,
            price = EXCLUDED.price,
            stock = EXCLUDED.stock,
            link = EXCLUDED.link,
            last_updated = EXCLUDED.last_updated
    """

    for page in range(1, 20):
        print("Page:", page)

        cardrushListingCurrURL = cardrushListingURL + "&page=" + str(page)
        cardrushResponse = requests.get(cardrushListingCurrURL, headers=HEADERS)
        cardrushResponse.encoding = "utf-8"

        soup = BeautifulSoup(cardrushResponse.text, "html.parser")

        cards = soup.select("li.list_item_cell")

        nextButton = soup.select_one("a.to_next_page")

        for card in cards:
            try:
                # Name
                name = await translator.translate(
                    card.select_one("span.goods_name").get_text(strip=True),
                    src='ja', dest='en'
                )

                # Price
                price = card.select_one("span.figure").get_text(strip=True)


                # Stock
                stock = card.select_one("p.stock").get_text(strip=True)

                if stock:
                    stock = re.search(r"\d+", stock).group()
                else:
                    stock = "0"


                # Product URL
                link = card.select_one("a.item_data_link")["href"]

                if ("[Status" not in name.text
                        and "[State" not in name.text
                        and "[Condition" not in name.text
                        and "[C]" not in name.text
                        and "[U]" not in name.text
                        and "[R]" not in name.text
                        and "[RR]" not in name.text
                        and "[ACE]" not in name.text
                        and "PSA10" not in name.text
                        and "PSA9" not in name.text
                        and "Expansion Pack" not in name.text
                        and "Booster Pack" not in name.text
                        and "Deck Shield" not in name.text
                        # and int(re.search(r"\{(\d+)/\d+\}", name.text).group(1) > int(cardrushSetAmount))
                ):
                    print(
                          # translator.translate(name, src='ja', dest='en'),
                          # translator.translate(price, src='ja', dest='en'),
                          # translator.translate(stock, src='ja', dest='en'),
                          # translator.translate(link, src='ja', dest='en')
                        name.text,
                        re.sub(r"\D", "", price),
                        stock,
                        link,
                        re.search(r"\{(\d+)/\d+\}", name.text).group(1),

                    )

                    now_utc = pytz.timezone('US/Eastern')
                    print(datetime.now(now_utc))

                    cardrushArray.append(
                        pokemon_card.PokemonCard(
                            name.text,
                            re.sub(r"\D", "", price),
                            stock,
                            link,
                            re.search(r"\{(\d+)/\d+\}", name.text).group(1)
                        )
                    )

                    params = (
                            name.text,
                            re.sub(r"\D", "", price),
                            stock,
                            link,
                            re.search(r"\{(\d+)/\d+\}", name.text).group(1),
                            cardrushSet,
                            datetime.now(now_utc)
                        )

                    try:
                        print(cursor.mogrify(query, params).decode("utf8"))
                        cursor.execute(query, params)
                        connection.commit()

                    except psycopg2._psycopg.OperationalError:
                        print("An error occurred while inserting/updating the cardrush table")


            except:
                print("Non-Card detected")
                # break


        if not nextButton:
            break

        time.sleep(random.uniform(2, 5))
        print("Next Page")

            # if exit_loops:
            #     break






async def torecacamp(num):

    translator = Translator()

    torecaCampListingURL = torecaCampLinks[num].link
    setAmount = torecaCampLinks[num].setAmount

    torecaCampSet = torecaCampLinks[num].set

    query = """
        INSERT INTO toreca_camp_cards (card_name, price, stock, link, card_number, card_set, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (card_set, card_number)
        DO UPDATE SET 
            card_name = EXCLUDED.card_name,
            price = EXCLUDED.price,
            stock = EXCLUDED.stock,
            link = EXCLUDED.link,
            last_updated = EXCLUDED.last_updated
    """

    print("Start of Toreca")
    for page in range(1, 20):
        finalExit = False

        torecaCampListingCurrURL = torecaCampListingURL + "&page=" + str(page)
        torecaCampResponse = requests.get(torecaCampListingCurrURL, headers=HEADERS)
        torecaCampResponse.encoding = "utf-8"

        soup = BeautifulSoup(torecaCampResponse.text, "html.parser")
        cards = soup.select("li.list_item_cell")

        product_list = soup.find("div", class_="product-list product-list--collection product-list--with-sidebar")
        product_items = product_list.find_all("div", class_="product-item")

        next_link_tag = soup.select_one("a.pagination__next")

        print("Curr Page: " + str(page))
        for item in product_items:

            # Product name
            name_tag = item.select_one("a.product-item__title")
            name = await translator.translate(
                name_tag.get_text(strip=True), src='ja', dest='en'
            )

            # Price
            price_tag = item.select_one("span.price")
            price = price_tag.get_text(strip=True) if price_tag else None

            # Quantity / Inventory
            qty_tag = item.select_one("span.product-item__inventory")
            quantity = qty_tag.get_text(strip=True) if qty_tag else "0"
            match = re.search(r"\d+", quantity)
            stock = match.group() if match else "0"

            # Product link (relative URL)
            link_tag = item.select_one("a.product-item__image-wrapper")
            link = link_tag["href"] if link_tag else None

            if ("[Status" not in name.text
                    and "[State" not in name.text
                    and "[Condition" not in name.text
                    and "[C]" not in name.text
                    and "[U]" not in name.text
                    and "[R]" not in name.text
                    and "[RR]" not in name.text
                    and "[ACE]" not in name.text
                    and "PSA10" not in name.text
                    and "PSA9" not in name.text
                    and int(setAmount) < int(re.search(r"(\d+)/\d+", name.text).group(1))
            ):

                print({
                    "name": name.text,
                    "price": re.search(r"[\d,]+", price).group().replace(",", ""),
                    "quantity": stock,
                    "link": "https://torecacamp-pokemon.com" + link,
                    "card_number": re.search(r"(\d+)/\d+", name.text).group(1)
                })

                now_utc = pytz.timezone('US/Eastern')
                print(datetime.now(now_utc))

                torecaCampArray.append(
                    pokemon_card.PokemonCard(
                        name.text,
                        re.search(r"[\d,]+", price).group().replace(",", ""),
                        stock,
                        "https://torecacamp-pokemon.com" + link,
                        re.search(r"(\d+)/\d+", name.text).group(1)
                    )
                )

                params = (
                    name.text,
                    re.sub(r"\D", "", price),
                    stock,
                    "https://torecacamp-pokemon.com" + link,
                    re.search(r"(\d+)/\d+", name.text).group(1),
                    torecaCampSet,
                    datetime.now(now_utc),
                )


                try:
                    print(cursor.mogrify(query, params).decode("utf8"))
                    cursor.execute(query, params)
                    connection.commit()

                except:
                    print("An error occurred while inserting/updating the toreca_camp table")

        if next_link_tag:
            print("Next Page")
        else:
            print("No more pages")
            finalExit = True
            break

        time.sleep(random.uniform(2, 5))



async def hareruya(num):
    translator = Translator()
    hareruyaListingURL = hareruyaLinks[num].link
    setAmount = hareruyaLinks[num].setAmount

    hareruyaSet = hareruyaLinks[num].set

    query = """
        INSERT INTO hareruya_cards (card_name, price, stock, link, card_number, card_set, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (card_set, card_number)
        DO UPDATE SET 
            card_name = EXCLUDED.card_name,
            price = EXCLUDED.price,
            stock = EXCLUDED.stock,
            link = EXCLUDED.link,
            last_updated = EXCLUDED.last_updated
    """

    print("Start of Hareruya")
    for page in range(1, 7):

        print("Page: " + str(page))
        finalExit = False

        hareruyaListingCurrURL = hareruyaLinks[num].link + "&page=" + str(page)
        hareruyaResponse = requests.get(hareruyaListingURL, headers=HEADERS)
        hareruyaResponse.encoding = "utf-8"

        soup = BeautifulSoup(hareruyaResponse.text, "html.parser")
        cards = soup.select("li.grid__item")

        next_button = soup.select_one(
            "a.pager_btn.pagination__item.pagination__item--prev.pagination__item-arrow.link.motion-reduce"
        )

        for card in cards:
            try:
                name = await translator.translate(
                    card.select_one("h3.card__heading.h5").get_text(strip=True), src='ja', dest='en'
                )

                price_tag = card.select_one("span.figure").get_text(strip=True)
                price = int(re.sub(r"\D", "", price_tag))

                stock_raw = card.select_one("div.product__inventory").get_text(strip=True)
                stock = int(re.search(r"\d+", stock_raw).group())

                link = card.select_one("a.full-unstyled-link").get("href")

                if ("*Status" not in name.text
                        and "(State" not in name.text
                        and "(Condition" not in name.text
                        and "(C)" not in name.text
                        and "(U)" not in name.text
                        and "(R)" not in name.text
                        and "(RR)" not in name.text
                        and "(ACE)" not in name.text
                        and "PSA10" not in name.text
                        and "PSA9" not in name.text
                        and int(setAmount) < int(re.search(r"(\d+)/\d+", name.text).group(1))
                ):

                    print(
                        name.text,
                        price,
                        stock,
                        "https://www.hareruya2.com" + link,
                        re.search(r"(\d+)/\d+", name.text).group(1)
                    )

                    now_utc = pytz.timezone('US/Eastern')
                    print(datetime.now(now_utc))

                    hareruyaArray.append(
                        pokemon_card.PokemonCard(
                            name.text,
                            price,
                            stock,
                            "https://www.hareruya2.com" + link,
                            re.search(r"(\d+)/\d+", name.text).group(1),
                        )
                    )

                    params = (
                        name.text,
                        price,
                        stock,
                        "https://www.hareruya2.com" + link,
                        re.search(r"(\d+)/\d+", name.text).group(1),
                        hareruyaSet,
                        datetime.now(now_utc),
                    )

                    try:
                        print(cursor.mogrify(query, params).decode("utf8"))
                        cursor.execute(query, params)
                        connection.commit()


                    except:
                        print("An error occurred while inserting/updating the hareruya table")


            except:
                print("Out of stock occurred")

        if next_button:
            time.sleep(random.uniform(2, 5))
            print("Next Page")
        else:
            print("No more pages")
            finalExit = True
            break


def databaseConnection():
    try:
        connection = psycopg2.connect(
            database = str(os.getenv("DATABASE")),
            user = str(os.getenv("USER")),
            password = str(os.getenv("PASSWORD")),
            host = str(os.getenv("HOST")),
            port = str(os.getenv("PORT")),
        )
        print("Database Connection Established")

        cursor = connection.cursor()

        cardrush_query = "INSERT INTO cardrush_sites (link, set, set_amount, set_release_date) VALUES (%s, %s, %s, %s)"
        torecacamp_query = "INSERT INTO toreca_camp_sites (link, set, set_amount, set_release_date) VALUES (%s, %s, %s, %s)"
        hareruya_query = "INSERT INTO hareruya_sites (link, set, set_amount, set_release_date) VALUES (%s, %s, %s, %s)"
        pricecharting_query = "INSERT INTO price_charting_sites (link, card_set, set_amount, set_release_date) VALUES (%s, %s, %s, %s)"

        for cardrushlink in cardrushLinks:
            try:
                print("Inserting cardrush set:", cardrushlink.set)
                data = (cardrushlink.link, cardrushlink.set, cardrushlink.setAmount, cardrushlink.setReleaseDate)
                cursor.execute(cardrush_query, data)
                connection.commit()
                print("Data inserted:", data)
            except psycopg2 as e:
                print("Insertion failed for cardrush", cardrushlink.set, e)

        for torecacamplink in torecaCampLinks:
            try:
                print("Inserting torecacamp set:", torecacamplink.set)
                data = (torecacamplink.link, torecacamplink.set, torecacamplink.setAmount, torecacamplink.setReleaseDate)
                cursor.execute(torecacamp_query, data)
                connection.commit()
                print("Data inserted:", data)
            except psycopg2 as e:
                print("Insertion failed for torecacamp", torecacamplink.set, e)

        for hareruyaLink in hareruyaLinks:
            try:
                print("Inserting hareruya set:", hareruyaLink.link)
                data = (hareruyaLink.link, hareruyaLink.set, hareruyaLink.setAmount, hareruyaLink.setReleaseDate)
                cursor.execute(hareruya_query, data)
                connection.commit()
            except psycopg2 as e:
                print("Insertion failed for hareruya", hareruyaLink.link, e)

        for priceChartingLink in priceChartingLinks:
            try:
                print("Inserting price charting set:", priceChartingLink.link)
                data = (priceChartingLink.link, priceChartingLink.set, priceChartingLink.setAmount, priceChartingLink.setReleaseDate)
                cursor.execute(pricecharting_query, data)
                connection.commit()
            except psycopg2 as e:
                print("Insertion failed for pricecharting", priceChartingLink.link, e)


    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
#


def marketPrice():
    print("Start of Market Price")
    for marketCard in priceChartingArray:

        cardrushPrice = 0
        cardrushQuantity = 0

        torecaPrice = 0
        torecaQuantity = 0

        hareruyaPrice = 0
        hareruyaQuantity = 0

        # Cardrush price
        try:
            for cardrushCard in cardrushArray:
                if int(marketCard.card_number) == int(cardrushCard.card_number):
                    cardrushPrice = cardrushCard.price
                    cardrushQuantity = cardrushCard.stock
                    break
        except:
            print("Error when getting Cardrush price")

        # Torecacamp price
        try:
            for torecaCard in torecaCampArray:
                if int(marketCard.card_number) == int(torecaCard.card_number):
                    torecaPrice = torecaCard.price
                    torecaQuantity = torecaCard.stock
                    break
        except:
            print("Error when getting Toreca price")

        # Hareruya price
        try:
            for hareruyaCard in hareruyaArray:
                if int(marketCard.card_number) == int(hareruyaCard.card_number):
                    hareruyaPrice = hareruyaCard.price
                    hareruyaQuantity = hareruyaCard.stock
                    break

        except:
            print("Error when getting Hareruya price")

        print(
            # marketCard.image,
            # marketCard.link,
            marketCard.name,
            # marketCard.card_number,

            "$" + str(round(c.convert(marketCard.price, "USD", "CAD"), 2)),

            "$" + str(round(c.convert(cardrushPrice, "JPY", "CAD"), 2)),
            "#" + str(cardrushQuantity),

            "$" + str(round(c.convert(torecaPrice, "JPY", "CAD"), 2)),
            "#" + str(torecaQuantity),

            "$" + str(round(c.convert(hareruyaPrice, "JPY", "CAD"), 2)),
            "#" + str(hareruyaQuantity),

        )
        if int(cardrushPrice) != 0:
            print("CardRush:", str(round(c.convert(marketCard.price, "USD", "CAD") / c.convert(cardrushPrice, "JPY", "CAD"), 2)) + "%",)

        if int(torecaPrice) != 0:
            print("TorecaCamp:", str(round(c.convert(marketCard.price, "USD", "CAD") / c.convert(torecaPrice, "JPY", "CAD"), 2)) + "%")

        if int(hareruyaPrice) != 0:
            print("Hareruya", str(round(c.convert(marketCard.price, "USD", "CAD") / c.convert(hareruyaPrice, "JPY", "CAD"), 2)) + "%")


        cardMarketArray.append(
            card_market_stats.CardMarketStats(
                marketCard.image,
                marketCard.link,
                marketCard.name,
                marketCard.card_number,

                round(c.convert(marketCard.price, "USD", "CAD"), 2),

                cardrushPrice,
                cardrushQuantity,

                torecaPrice,
                torecaQuantity,

                hareruyaPrice,
                hareruyaQuantity
            )
        )

def websiteLinks():
    print("Start of Website Links")
    try:
        cursor.execute("SELECT set, link, set_amount, set_release_date FROM cardrush_sites")
        cardrushRows = cursor.fetchall()
        for cardrushCard in cardrushRows:
            cardrushLinks.append(website_link.WebsiteLink(cardrushCard[0], cardrushCard[1], cardrushCard[2], cardrushCard[3]))



        cursor.execute("SELECT set, link, set_amount, set_release_date FROM toreca_camp_sites")
        torecaRows = cursor.fetchall()
        for torecaCampCard in torecaRows:
            torecaCampLinks.append(website_link.WebsiteLink(torecaCampCard[0], torecaCampCard[1], torecaCampCard[2], torecaCampCard[3]))



        cursor.execute("SELECT set, link, set_amount, set_release_date FROM hareruya_sites")
        hareruyaRows = cursor.fetchall()
        for hareruyaCampCard in hareruyaRows:
            hareruyaLinks.append(website_link.WebsiteLink(hareruyaCampCard[0], hareruyaCampCard[1], hareruyaCampCard[2], hareruyaCampCard[3]))



        cursor.execute("SELECT card_set, link, set_amount, set_release_date FROM price_charting_sites")
        priceChartingRows = cursor.fetchall()
        for priceChartingCard in priceChartingRows:
            priceChartingLinks.append(website_link.WebsiteLink(priceChartingCard[0], priceChartingCard[1], priceChartingCard[2], priceChartingCard[3]))



    except:
        print("Error when getting Website Links")


# setnum = 10

start_time = time.time()

websiteLinks()
print(cardrushLinks[0].set, cardrushLinks[0].link, cardrushLinks[0].setAmount, cardrushLinks[0].setReleaseDate)

for i in range(len(priceChartingLinks)):

    asyncio.run(cardrush(i))
    print("Cardrush cards:", len(cardrushArray), cardrushArray[0].__dict__, cardrushArray[0].name)

    asyncio.run(torecacamp(i))
    print("Torecacamp cards:", len(torecaCampArray), torecaCampArray[0].__dict__, torecaCampArray[0].name)

    asyncio.run(hareruya(i))
    print("Hareruya cards:", len(hareruyaArray), hareruyaArray[0].__dict__, hareruyaArray[0].name)

    print("CR Array:", cardrushArray)
    print("TC Array:", torecaCampArray)

    priceCharting(i)
    print(priceChartingArray[i].name)

    marketPrice()
    print(cardMarketArray[0].imageURL,
          cardMarketArray[0].siteURL,
          cardMarketArray[0].cardName,
          cardMarketArray[0].card_number,

          cardMarketArray[0].marketPrice,

          cardMarketArray[0].cardrushPrice,
          cardMarketArray[0].cardrushQuantity,

          cardMarketArray[0].torecacampPrice,
          cardMarketArray[0].torecacampQuantity,

          cardMarketArray[0].hareruyaPrice,
          cardMarketArray[0].hareruyaQuantity,
    )

# databaseConnection()

end_time = time.time()

elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time)