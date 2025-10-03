[![Test](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/test.yaml/badge.svg)](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/test.yaml)
[![Publish](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/publish.yaml/badge.svg)](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/publish.yaml)

<hr>

# PLaystation Store Scrapper 
A web scraper for the PlayStation Store that retrieves and lists all available games with details such as title, price, platform, and more.

# Installation using pip
To install the PlayStation Store Scraper package, open your terminal or command prompt and run the following command:

` $ pip install playstation-store-scraper `

# Usage

For pulling a group/page of games, use ``scraper.list_games`` function.

```
>>> from playstation_store_scraper import scraper
>>> from playstation_store_scraper.scraper import region
>>>
>>> scraper.list_games(page_number = 2, region = region.TURKEY_ENGLISH)`
```



For full detail of a game with given `concept ID`, use ``scraper.retrieve_game`` function. Concept ID` is an identifier for a game available on the PlayStation Store. Note that this ID can be gathered using ``scraper.list_games``

```
>>> from playstation_store_scraper import scraper
>>> from playstation_store_scraper.scraper import region
>>>
>>> scraper.retrieve_game(concept_id = "10011898", region = region.TURKEY_ENGLISH)
```