import requests
from bs4 import BeautifulSoup
import time
import random
from googletrans import Translator
import asyncio
import re
from currency_converter import CurrencyConverter

import price_charting_card
import pokemon_card
import website_link
import card_market_stats
import psycopg2

c = CurrencyConverter()

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

cardrushArray = []
cardrushLinks = [
    website_link.WebsiteLink("sv2a", "https://www.cardrush-pokemon.jp/product-list/0/0/photo?keyword=sv2a&num=100&img=120&available=1&order=desc&main_category=&group=&Submit=Narrow+your+search", 165),
    website_link.WebsiteLink("sv7a", "https://www.cardrush-pokemon.jp/product-group/409?num=100&available=1&img=120&order=desc", 64),
    website_link.WebsiteLink("sv8", "https://www.cardrush-pokemon.jp/product-group/411?num=100&available=1&img=120&order=desc", 106),
    website_link.WebsiteLink("sv8a", "https://www.cardrush-pokemon.jp/product-group/416?num=100&available=1&img=120&order=desc", 187),
    website_link.WebsiteLink("sv9", "https://www.cardrush-pokemon.jp/product-group/427?num=100&available=1&img=120&order=desc", 100),
    website_link.WebsiteLink("sv9a", "https://www.cardrush-pokemon.jp/product-group/449?num=100&available=1&img=120&order=desc", 63),
    website_link.WebsiteLink("sv10", "https://www.cardrush-pokemon.jp/product-group/457?num=100&available=1&img=120&order=desc", 98),
    website_link.WebsiteLink("sv11b", "https://www.cardrush-pokemon.jp/product-list?num=100&available=1&img=120&order=price-desc&keyword=sv11b&Submit=search", 86),
    website_link.WebsiteLink("sv11w", "https://www.cardrush-pokemon.jp/product-list?num=100&available=1&img=120&order=price-desc&keyword=sv11w&Submit=search", 86),
    website_link.WebsiteLink("m1l", "https://www.cardrush-pokemon.jp/product-list/0/0/photo?keyword=m1l&num=100&img=160&available=1&order=desc&main_category=&group=&Submit=Narrow+your+search", 63),
    website_link.WebsiteLink("m1s", "https://www.cardrush-pokemon.jp/product-list?num=100&img=160&available=1&order=price-desc&keyword=m1s&Submit=search", 63),
]

torecaCampArray = []
torecaCampLinks = [
    website_link.WebsiteLink("sv2a", "https://torecacamp-pokemon.com/collections/sv2a-%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E3%82%AB%E3%83%BC%E3%83%89151?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 165),
    website_link.WebsiteLink("sv7a", "https://torecacamp-pokemon.com/collections/sv7a-%E6%A5%BD%E5%9C%92%E3%83%89%E3%83%A9%E3%82%B4%E3%83%BC%E3%83%8A?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 64),
    website_link.WebsiteLink("sv8", "https://torecacamp-pokemon.com/collections/sv8-%E8%B6%85%E9%9B%BB%E3%83%96%E3%83%AC%E3%82%A4%E3%82%AB%E3%83%BC?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 106),
    website_link.WebsiteLink("sv8a", "https://torecacamp-pokemon.com/collections/sv8a-%E3%83%86%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%AB%E3%83%95%E3%82%A7%E3%82%B9ex?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 187),
    website_link.WebsiteLink("sv9", "https://torecacamp-pokemon.com/collections/sv9?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 100),
    website_link.WebsiteLink("sv9a", "https://torecacamp-pokemon.com/collections/sv9a?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 63),
    website_link.WebsiteLink("sv10", "https://torecacamp-pokemon.com/collections/sv10?filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=&sort_by=price-descending", 98),
    website_link.WebsiteLink("sv11b", "https://torecacamp-pokemon.com/collections/sv11b?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 86),
    website_link.WebsiteLink("sv11w", "https://torecacamp-pokemon.com/collections/sv11w?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 86),
    website_link.WebsiteLink("m1l", "https://torecacamp-pokemon.com/collections/m1l?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 63),
    website_link.WebsiteLink("m1s", "https://torecacamp-pokemon.com/collections/m1s?sort_by=price-descending&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=", 63),
]

priceChartingArray = []
priceChartingLinks = [
    website_link.WebsiteLink("sv2a", "https://www.pricecharting.com/console/pokemon-japanese-scarlet-&-violet-151?exclude-hardware=true&exclude-variants=true&in-collection=&model-number=&show-images=true&sort=highest-price&view=grid", 165),
    website_link.WebsiteLink("sv7a", "https://www.pricecharting.com/console/pokemon-japanese-paradise-dragona?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 64),
    website_link.WebsiteLink("sv8", "https://www.pricecharting.com/console/pokemon-japanese-super-electric-breaker?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 106),
    website_link.WebsiteLink("sv8a", "https://www.pricecharting.com/console/pokemon-japanese-terastal-festival?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 187),
    website_link.WebsiteLink("sv9", "https://www.pricecharting.com/console/pokemon-japanese-battle-partners?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 100),
    website_link.WebsiteLink("sv9a", "https://www.pricecharting.com/console/pokemon-japanese-heat-wave-arena?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 63),
    website_link.WebsiteLink("sv10", "https://www.pricecharting.com/console/pokemon-japanese-glory-of-team-rocket?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 98),
    website_link.WebsiteLink("sv11b", "https://www.pricecharting.com/console/pokemon-japanese-black-bolt?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 86),
    website_link.WebsiteLink("sv11w", "https://www.pricecharting.com/console/pokemon-japanese-white-flare?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 86),
    website_link.WebsiteLink("m1l", "https://www.pricecharting.com/console/pokemon-japanese-mega-brave?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 63),
    website_link.WebsiteLink("m1s", "https://www.pricecharting.com/console/pokemon-japanese-mega-symphonia?sort=highest-price&model-number=&exclude-hardware=true&exclude-variants=true&show-images=true&in-collection=&view=grid", 63),
]


hareruyaArray = []
hareruyaLinks = [
    website_link.WebsiteLink("sv2a", "https://www.hareruya2.com/collections/612?filter.v.availability=1&sort_by=price-descending", 165),
    website_link.WebsiteLink("sv7a", "https://www.hareruya2.com/collections/sv7a?filter.v.availability=1&sort_by=price-descending", 64),
    website_link.WebsiteLink("sv8", "https://www.hareruya2.com/collections/sv8?filter.v.availability=1&sort_by=price-descending", 106),
    website_link.WebsiteLink("sv8a", "https://www.hareruya2.com/collections/sv8a?filter.v.availability=1&sort_by=price-descending", 187),
    website_link.WebsiteLink("sv9", "https://www.hareruya2.com/collections/sv9?filter.v.availability=1&sort_by=price-descending", 100),
    website_link.WebsiteLink("sv9a", "https://www.hareruya2.com/collections/sv9a?filter.v.availability=1&sort_by=price-descending", 63),
    website_link.WebsiteLink("sv10", "https://www.hareruya2.com/collections/sv10?filter.v.availability=1&sort_by=price-descending", 98),
    website_link.WebsiteLink("sv11b", "https://www.hareruya2.com/collections/sv11b?filter.v.availability=1&sort_by=price-descending", 86),
    website_link.WebsiteLink("sv11w", "https://www.hareruya2.com/collections/sv11w?filter.v.availability=1&sort_by=price-descending", 86),
    website_link.WebsiteLink("m1l", "https://www.hareruya2.com/collections/701?filter.v.availability=1&sort_by=price-descending", 63),
    website_link.WebsiteLink("m1s", "https://www.hareruya2.com/collections/702?filter.v.availability=1&sort_by=price-descending", 63),
]

cardMarketArray = []


def priceCharting(num):
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






async def cardrush(num):

    translator = Translator()

    # cardrushListingURL = "https://www.cardrush-pokemon.jp/product-list/0/0/photo?keyword=sv10&num=100&img=120&order=desc&main_category=&group=448&Submit=Narrow+your+search"
    cardrushListingURL = cardrushLinks[num].link

    for page in range(1, 6):
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

                # # Product URL
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
                ):
                    print(
                          # translator.translate(name, src='ja', dest='en'),
                          # translator.translate(price, src='ja', dest='en'),
                          # translator.translate(stock, src='ja', dest='en'),
                          # translator.translate(link, src='ja', dest='en')
                        name.text,
                        re.sub(r"\D", "", price),
                        re.search(r"\d+", stock).group(),
                        link,
                        re.search(r"\{(\d+)/\d+\}", name.text).group(1)
                    )

                    cardrushArray.append(
                        pokemon_card.PokemonCard(
                            name.text,
                            re.sub(r"\D", "", price),
                            re.search(r"\d+", stock).group(),
                            link,
                            re.search(r"\{(\d+)/\d+\}", name.text).group(1)
                        )
                    )
            except:
                print("Out of stock occurred")
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
                    "quantity": re.search(r"\d+", quantity).group(),
                    "link": "https://torecacamp-pokemon.com" + link,
                    "card_number": re.search(r"(\d+)/\d+", name.text).group(1)
                })

                torecaCampArray.append(
                    pokemon_card.PokemonCard(
                        name.text,
                        re.search(r"[\d,]+", price).group().replace(",", ""),
                        re.search(r"\d+", quantity).group(),
                        "https://torecacamp-pokemon.com" + link,
                        re.search(r"(\d+)/\d+", name.text).group(1)
                    )
                )

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

                quantity_raw = card.select_one("div.product__inventory").get_text(strip=True)
                quantity = int(re.search(r"\d+", quantity_raw).group())

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
                        quantity,
                        "https://www.hareruya2.com" + link,
                        re.search(r"(\d+)/\d+", name.text).group(1),
                    )

                    hareruyaArray.append(
                        pokemon_card.PokemonCard(
                            name.text,
                            price,
                            quantity,
                            "https://www.hareruya2.com" + link,
                            re.search(r"(\d+)/\d+", name.text).group(1),
                        )
                    )

            except:
                print("Out of stock occurred")

        if next_button:
            time.sleep(random.uniform(2, 5))
            print("Next Page")
        else:
            print("No more pages")
            finalExit = True
            break




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




setnum = 1

asyncio.run(cardrush(setnum))
print("Cardrush cards:", len(cardrushArray), cardrushArray[0].__dict__, cardrushArray[0].name)

asyncio.run(torecacamp(setnum))
print("Torecacamp cards:", len(torecaCampArray), torecaCampArray[0].__dict__, torecaCampArray[0].name)

asyncio.run(hareruya(setnum))
print("Hareruya cards:", len(hareruyaArray), hareruyaArray[0].__dict__, hareruyaArray[0].name)

print("CR Array:", cardrushArray)
print("TC Array:", torecaCampArray)

priceCharting(setnum)
print(priceChartingArray[setnum].name)

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