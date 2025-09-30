from typing import Literal
from urllib.request import urlopen
from bs4 import BeautifulSoup


REGION = Literal["en", "en-tr"]
BASE_URL = "https://store.playstation.com"


def _get_url(region: REGION, page: int):
    if region == "en":
        return f"{BASE_URL}/pages/browse/{page}"
    else:
        return f"{BASE_URL}/{region}/pages/browse/{page}"


def _request(url: str) -> BeautifulSoup:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, "html.parser")


def _scrap_cards(cards):
    games = []
    for c in cards:
        url = "https://store.playstation.com" + c.find("a")["href"]
        games.append(
            {
                "id": url.split("/")[-1],
                "title": c.find(id="product-name").text,
                "image": c.find("img")["src"].split("?")[0],
                "url": url,
            }
        )
    return games


def list_games(region: REGION = "en", page: int = 1):
    games = []
    url = _get_url(region, page)
    soup = _request(url)
    last_page = int(soup.find("ol").find_all("span")[-1].text)
    cards = soup.find_all("li", class_="psw-l-w-1/2@mobile-s")
    games = _scrap_cards(cards)
    return games, page, last_page
