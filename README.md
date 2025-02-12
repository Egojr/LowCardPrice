# LowCardPrice webscraper

This script scrapes [Wisdom Guild](http://whisper.wisdom-guild.net/), a card price aggregator for Magic: The Gathering card shops in Japan.

## Dependencies

There is no makefile or fancy installer for this project.  You will have to install dependencies manually.

* [beautifulsoup 4](https://pypi.org/project/beautifulsoup4/) 
* [selenium](https://pypi.org/project/selenium/) 

### Tested versions

* python 3.12
* bs4 v4.12.3
* selenium v4.16.0

## What does it do

Takes a shopping list (``cardlist.txt``) and a list of shops to gather prices from (``shoplist.txt``) and gets 
the lowest price listed for English and Japanese language (language is hardcoded).  The script goes to a hardcoded URL
with the card name inserted, set to filter out stores with no stock.  It only searches the first page so may miss.

## How does it work

1. Write or paste card names in ``cardlist.txt``, one card per line.
1. Write or paste shop names in ``shoplist.txt``, one shop per line.
    * *For now you will also need to check that it is in the dic in ``lowcardprice.py`` as well*
1. Run ``lowcardprice.py``
1. Open the output ``pricelist<date>.csv``, for example by Importing into Google Sheets
   * Recommended conditional formatting to highlight the lowest price per line (adjust range to actual range): ``=A2=MIN($A2:$D2)``

## FAQ

* Q: Why isn't a card listed in the output *.csv?
  * A: There was likely an error scraping that page.  Check the python terminal for total errors and each card that threw an error.
* Q: Why isn't there a price for a card for a certain shop in the *.csv?
  * A: That shop's price was not low enough to be displayed on the first page of in-stock listings.
* Q: Why isn't there a price for any shops for a card?
  * A: See above.  This usually happens when the card is very cheap and many shops have the same low price.
* Q: Why does the same card always throw an error?
  * A: If the card name isn't mispelled, it likely means the card is not listed on Wisdom Guild.  This happens with special print cards, such as Universes Beyond or the Clue precon set.
* Q: Why can't I find the listed price on the shop webpage?
  * A: This is a Wisdom Guild issue.  They only scrape periodically and a card may be sold out by the time you see the listing.
* Q: Can I participate in this project?
  * A: If you want to help, sure.  Make a PR or fork the project. 
