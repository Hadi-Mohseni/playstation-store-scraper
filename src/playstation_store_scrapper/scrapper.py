from typing import Literal
from urllib.request import urlopen
from bs4 import BeautifulSoup

REGIONS = ["en", "en-tr"]
REGION = Literal["en", "en-tr"]
BASE_URL = "https://store.playstation.com"


class RegionInvalidError(Exception): ...


def _get_url(region: REGION, page: int) -> str:
    """
    _get_url Generate the URL for the PlayStation Store based on the region and page number.

    Parameters
    ----------
    region : REGION
        The region code ("en" or "en-tr").
    page : int
        The page number.

    Returns
    -------
    str
        The generated URL.
    """
    if region == "en":
        return f"{BASE_URL}/pages/browse/{page}"
    else:
        return f"{BASE_URL}/{region}/pages/browse/{page}"


def _request(url: str) -> BeautifulSoup:
    """
    _request Make a request to the provided URL and return the BeautifulSoup object.

    Parameters
    ----------
    url : str
        The URL to request.

    Returns
    -------
    BeautifulSoup
        The parsed HTML content.
    """
    return BeautifulSoup(urlopen(url).read().decode("utf-8"), "html.parser")


def list_games(region: REGION = "en", page: int = 1) -> tuple:
    """
    list_games List games available on the PlayStation Store for the specified region and page.

    Parameters
    ----------
    region : REGION, optional
        The region code ("en" or "en-tr"), by default "en"
    page : int, optional
        The page number, by default 1

    Returns
    -------
    tuple
        A tuple containing:
            list: A list of dictionaries containing game information.
            int: The current page number.
            int: The last page number.

    Raises
    ------
    RegionInvalidError
        If an invalid region is provided.
    """
    if region not in REGIONS:
        raise RegionInvalidError

    url = _get_url(region, page)
    soup = _request(url)
    last_page = int(soup.find("ol").find_all("span")[-1].text)
    cards = soup.find_all("li", class_="psw-l-w-1/2@mobile-s")
    games = [
        {
            "id": (BASE_URL + c.find("a")["href"]).split("/")[-1],
            "title": c.find(id="product-name").text,
            "image": c.find("img")["src"].split("?")[0],
            "url": BASE_URL + c.find("a")["href"],
        }
        for c in cards
    ]
    return games, page, last_page
