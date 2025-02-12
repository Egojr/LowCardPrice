from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import csv

# Convert Japanese shop names to English
romaji = {
    "シングルスター": "SS",
    "テーブルトップ": "TT",
    "晴れる屋": "Hare",
    "トレトク": "Tore",
    "ENNDAL GAMES": "ENND",
    "Cardshop Serra": "Serra",
    "カードラッシュ": "Rush",
    "toyaju shop": "toya",
    "ドラゴンスター": "DStar",
    "カーナベル": "Carn",
    "Nageya": "Nag",
    "まんぞく屋": "Manz",
    "MTG専門店しかのつの": "Shika",
    "ショップあきあき": "Aki",
    "HOBBY SHOPファミコンくん": "Fami",
    "カードショップBIGRED": "BigRed",
    "MTG専門店しかのつの": "shika",
    "BLACK FROG": "BF",
    "Nageya": "Nage",
    "MTG Guild": "Guild",
    "まんぞく屋": "Manz",
    "MINT MALL": "MINT",
    "アドバンテージ": "Adv",
    "カードショップ抜忍": "Nuke",
    "MTG Guild": "Guild",
    "カードショップはま屋": "Hamaya",
    "BIGWEB": "BIG",
    "Gemutlich": "Gemu"
}

# Set input and output filenames
cardfile = "cardlist.txt"
shopfile = "shoplist.txt"
outputfile = "pricelist" + datetime.today().strftime('%Y-%m-%d') + ".csv"

def lowCardPrice():
    # Read input files
    with open(cardfile) as f:
        cards = f.read().splitlines()

    with open(shopfile, 'r', encoding='utf-8') as f:                                                                    # Ensure shop name is also in romaji dict
        shops = f.read().splitlines()

    # Set target website to scrape
    urlHeader = "http://wonder.wisdom-guild.net/price/"
    urlFooter = "/?stock_gt=1"                                                                                          # Filters set to "in stock"
    driver = webdriver.Chrome()

    # Set target columns for HTML table (0: shop, 1: price, 2: set, 3: lang, 4: stock, 5: condition)
    shopname = 0
    price = 1
    lang = 3

    # Error counter
    errCount = 0

    with open(outputfile, 'w', newline='') as csvfile:
        # Write shop names (EN and JP) as header of CSV files
        fieldnames = ["Card Name"]                                                                                      # Column A is "Card Name", B~ are shop names
        for shop in shops:
            fieldnames.append(romaji[shop] + "_ENG")                                                                    # Language footer matches input from HTML table
            fieldnames.append(romaji[shop] + "_JPN")                                                                    # Language footer matches input from HTML table
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Scan for each card in HTML table
        for card in cards:
            card_dict = {"Card Name": card}

            url = urlHeader + str(card) + urlFooter
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            table = soup.find("table", class_="table-main")

            if not table:
                print("Error scraping {}".format(card))
                errCount+=1
                continue

            for row in table.find_all('tr'):
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]

                if len(cols) > 0:
                    try:
                        if cols[shopname] in shops:
                            key = romaji[cols[shopname]] + "_" + cols[lang]
                            if key not in card_dict:                                                                    # Do not add duplicates (only add lowest price)
                                p = int(cols[price].split()[0].replace(',', ''))                                        # Remove yen sign and commas
                                card_dict[key] = p
                    except:
                        print("Error scraping {}".format(card))

            try:
                writer.writerow(card_dict)
                print("Successfully wrote {}".format(card_dict["Card Name"]))
            except:
                print("card_dict: {}".format(card_dict))
                print("Error writing {} to csv".format(card))
                errCount += 1

        print("Finished with {} errors.".format(errCount))

if __name__  == "__main__":
    lowCardPrice()