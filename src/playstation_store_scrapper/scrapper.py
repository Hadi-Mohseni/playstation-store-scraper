from typing import Literal
from urllib.request import urlopen
from bs4 import BeautifulSoup

REGIONS = ["en", "en-tr"]
REGION = Literal["en", "en-tr"]
BASE_URL = "https://store.playstation.com"


class RegionInvalidError(Exception): ...


def _get_url(region: REGION, page: int):
    if region == "en":
        return f"{BASE_URL}/pages/browse/{page}"
    else:
        return f"{BASE_URL}/{region}/pages/browse/{page}"


def _request(url: str) -> BeautifulSoup:
    return BeautifulSoup(urlopen(url).read().decode("utf-8"), "html.parser")


def _scrap_cards(cards):
    return [
        {
            "id": (BASE_URL + c.find("a")["href"]).split("/")[-1],
            "title": c.find(id="product-name").text,
            "image": c.find("img")["src"].split("?")[0],
            "url": BASE_URL + c.find("a")["href"],
        }
        for c in cards
    ]


def list_games(region: REGION = "en", page: int = 1):
    if region not in REGIONS:
        raise RegionInvalidError

    url = _get_url(region, page)
    soup = _request(url)
    last_page = int(soup.find("ol").find_all("span")[-1].text)
    games = _scrap_cards(soup.find_all("li", class_="psw-l-w-1/2@mobile-s"))
    return games, page, last_page
