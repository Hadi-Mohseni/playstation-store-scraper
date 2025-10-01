from typing import Literal
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ast

REGIONS = ["en", "en-tr"]
REGION = Literal["en", "en-tr"]
BASE_URL = "https://store.playstation.com"


class RegionInvalidError(Exception): ...


def _get_list_url(region: REGION, page: int) -> str:
    """
    _get_list_url Generate the URL for the PlayStation Store based on the region and page number.

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


def _get_retrieve_url(concept_id: str, region: REGION) -> str:
    """
    Generate the URL for retrieving a specific game concept on the PlayStation Store.

    This function constructs the URL for fetching detailed information about a game
    concept based on the provided game ID and region.

    Parameters
    ----------
    region : REGION
        The region code ("en" or "en-tr").
    concept_id : str
        he unique identifier for the game.

    Returns
    -------
    str
        The generated URL.
    """
    if region == "en":
        return f"{BASE_URL}/en-tr/concept/{concept_id}"
    else:
        return f"{BASE_URL}/{region}/en-tr/concept/{concept_id}"


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


def _get_editions(soup: BeautifulSoup):
    articles = soup.find_all("article")
    editions = []
    for a in articles:
        meta = a.find("button").get("data-telemetry-meta")
        meta = meta.replace("false", "False")
        meta = meta.replace("true", "True")
        meta = meta.replace("null", "None")
        meta = ast.literal_eval(meta)
        if meta["ctaSubType"] != "add_to_cart":
            continue

        title = a.find("h3").text
        price_detail = meta["productDetail"][0]["productPriceDetail"][0]
        original_price = price_detail["originalPriceValue"]
        discount_price = price_detail["discountPriceValue"]
        currency = price_detail["priceCurrencyCode"]
        editions.append(
            {
                "title": title,
                "original_price": original_price,
                "discount_price": discount_price,
                "currency": currency,
            }
        )

    return editions


def _scrap_retrieve(soup: BeautifulSoup):
    title = soup.find("h1").text
    pltfrm = soup.find("dd", {"data-qa": "gameInfo#releaseInformation#platform-value"})
    rd = soup.find("dd", {"data-qa": "gameInfo#releaseInformation#releaseDate-value"})
    pblshr = soup.find("dd", {"data-qa": "gameInfo#releaseInformation#publisher-value"})
    genres = soup.find("dd", {"data-qa": "gameInfo#releaseInformation#genre-value"})
    editions = _get_editions(soup)
    return {
        "title": title,
        "platforms": pltfrm,
        "release_data": rd,
        "publisher": pblshr,
        "genres": genres,
        "editions": editions,
    }


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

    url = _get_list_url(region, page)
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


def retrieve_game(concept_id: str, region: REGION = "en"):
    if region not in REGIONS:
        raise RegionInvalidError
    url = _get_retrieve_url(concept_id, region)
    soup = _request(url)
    return _scrap_retrieve(soup)
