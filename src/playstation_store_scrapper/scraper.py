from urllib.request import urlopen
from bs4 import BeautifulSoup
from enum import Enum
import ast


BASE_URL = "https://store.playstation.com"


class REGION(Enum):
    ARGENTINA = "es-ar"
    AUSTRALIA = "en-au"
    AUSTRIA = "de-at"
    BAHRAIN_ARABIC = "ar-bh"
    BAHRAIN_ENGLISH = "en-bh"
    BELGIUM_FRENCH = "fr-be"
    BELGIUM_DUTCH = "nl_be"
    BOLIVIA = "es-bo"
    BRASIL = "pt-br"
    BULGARIA = "bg-bg"
    BULGARIA_ENGLISH = "en-bg"
    CANADA_ENGLISH = "en-ca"
    CANADA_FRENCH = "fr-ca"
    CHILE = "es-cl"
    COLOMBIA = "es-co"
    COSTA_RICA = "es-cr"
    CROATIA_ENGLISH = "en-hr"
    CROATIA_HRVATSKA = "hr-hr"
    CYPRUS = "en-cy"
    CZECH_REPUBLIC = "cz-cz"
    CZECH_REPUBLIC_ENGLISH = "en-cz"
    DENMARK = "da-dk"
    DENMARK_ENGLISH = "en-dk"
    ECUADOR = "es-ec"
    EL_SALVADOR = "es-sv"
    FINLAND_ENGLISH = "en-fi"
    FINLAND_SUOMI = "fi-fi"
    FRANCE = "fr-fr"
    GERMANY_DUTCH = "de-de"
    GREECE = "el-gr"
    GREECE_ENGLISH = "en-gr"
    GUATEMALA = "es-gt"
    HONDURAS = "es-hn"
    HONG_KONG = "zs-hans-hk"
    HONG_KONG_ENGLISH = "en-hk"
    HUNGARY = "hu-hu"
    HUNGARY_ENGLISH = "en-hu"
    ICELAND_ENGLISH = "en-is"
    INDIA = "en-in"
    INDONESIA_ENGLISH = "en-id"
    IRELAND = "en-ie"
    ISRAEL_ENGLISH = "en-il"
    ISRAEL = "he-il"
    ITALY = "it-it"
    JAPAN = "ja-jp"
    KOREA = "ko-kr"
    KUWAIT_ARABIC = "ar-kw"
    KUWAIT_ENGLISH = "en-kw"
    LEBANON_ARABIC = "ar-lb"
    LEBANON_ENGLISH = "en-lb"
    LUXEMBOURG_DUTCH = "de-lu"
    LUXEMBOURG_FRENCH = "fr-lu"
    MALAYSIA_ENGLISH = "en-my"
    MALTA = "en-mt"
    MEXICO = "es-mx"
    NEDERLAND = "nl-nl"
    NEW_ZEALAND = "en-nz"
    NICARAGUA = "es-ni"
    NORWAY = "no-no"
    NORWAY_ENGLISH = "en-no"
    OMAN_ARABIC = "ar-om"
    OMAN_ENGLISH = "en-om"
    PANAMA = "es-pa"
    PARAGUAY = "es-py"
    PERU = "es-pe"
    PHILIPPINES_ENGLISH = "en-ph"
    POLAND = "pl-pl"
    POLAND_ENGLISH = "en-pl"
    PORTUGAL = "pt-pt"
    QATAR_ARABIC = "ar-qa"
    QATAR_ENGLISH = "en-qa"
    ROMANIA = "ro-ro"
    ROMANIA_ENGLISH = "en-ro"
    RUSSIA = "ru-ru"
    SAUDI_ARABIA = "ar-sa"
    SAUDI_ARABIA_ENGLISH = "en-sa"
    SERBIA = "sr-sr"
    SINGAPORE_ENGLISH = "en-sg"
    SLOVENIA = "sl-si"
    SLOVENIA_ENGLISH = "en-si"
    SLOVAKIA = "sk-sk"
    SLOVAKIA_ENGLISH = "en-sk"
    SOUTH_AFRICA = "en-za"
    SPAIN = "es-es"
    SWEDEN = "sv-se"
    SWEDEN_ENGLISH = "en-se"
    SWITZERLAND_DUTCH = "de-ch"
    SWITZERLAND_FRENCH = "fr-ch"
    SWITZERLAND_ITALIAN = "it-ch"
    TAIWAN = "zh-hant-tw"
    TAIWAN_ENGLISH = "en-tw"
    THAILAND = "th-th"
    THAILAND_ENGLISH = "en-th"
    TURKEY = "tr-tr"
    TURKEY_ENGLISH = "en-tr"
    UKRAINE = "ru-ua"
    UAE_ARABIC = "ar-ae"
    UAE_ENGLISH = "en-ae"
    USA = "en-us"
    UNITED_KINGDOM = "en-gb"
    URUGUAY = "es-uy"
    VIETNAM_ENGLISH = "en-vn"


class RegionInvalidError(Exception): ...


def _get_list_url(region: REGION = REGION.USA, page: int = 1) -> str:
    """
    _get_list_url Generate the URL for the PlayStation Store based on the region and page number.

    Parameters
    ----------
    region : REGION, optional
    page : int
        The page number.

    Returns
    -------
    str
        The generated URL.
    """
    return f"{BASE_URL}/{region.value}/pages/browse/{page}"


def _get_retrieve_url(concept_id: str, region: REGION = REGION.USA) -> str:
    """
    Generate the URL for retrieving a specific game concept on the PlayStation Store.

    This function constructs the URL for fetching detailed information about a game
    concept based on the provided game ID and region.

    Parameters
    ----------
    region : REGION, optional
    concept_id : str
        he unique identifier for the game.

    Returns
    -------
    str
        The generated URL.
    """
    return f"{BASE_URL}/{region.value}/concept/{concept_id}"


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


def _get_editions(soup: BeautifulSoup) -> list:
    """
    Extract edition information from the BeautifulSoup object.

    Parameters
    ----------
    soup : BeautifulSoup
        The parsed HTML content representing the game page.

    Returns
    -------
    list
        A list of dictionaries, each containing edition-specific information.

    Each dictionary in the list has the following keys:
        - "title" (str): The title of the edition.
        - "original_price" (float): The original price of the edition.
        - "discount_price" (float): The discounted price of the edition.
        - "currency" (str): The currency code for the price.
    """
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
        original_price = price_detail["originalPriceFormatted"]
        discount_price = price_detail["discountPriceFormatted"]
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


def _scrap_retrieve(soup: BeautifulSoup) -> dict:
    """
    Extract detailed information about a game from the BeautifulSoup object.

    Parameters
    ----------
    soup : BeautifulSoup
        The parsed HTML content representing the game page.

    Returns
    -------
    dict
        A dictionary containing detailed information about the game.

    Keys in the returned dictionary:
        - "title" (str): The full title of the game.
        - "platforms" (str): The platforms the game is available on.
        - "release_date" (str): The release date of the game.
        - "publisher" (str): The publisher of the game.
        - "genres" (str): The genres the game belongs to.
        - "editions" (list): A list of dictionaries containing edition-specific information.

    Each edition dictionary contains:
        - "title" (str): The title of the edition.
        - "original_price" (float): The original price of the edition.
        - "discount_price" (float): The discounted price of the edition.
        - "currency" (str): The currency code for the price.

    """
    title = soup.find("h1").text
    pltfrm = soup.find(
        "dd", {"data-qa": "gameInfo#releaseInformation#platform-value"}
    ).text
    rd = soup.find(
        "dd", {"data-qa": "gameInfo#releaseInformation#releaseDate-value"}
    ).text
    pblshr = soup.find(
        "dd", {"data-qa": "gameInfo#releaseInformation#publisher-value"}
    ).text
    genres = soup.find(
        "dd", {"data-qa": "gameInfo#releaseInformation#genre-value"}
    ).text
    editions = _get_editions(soup)
    return {
        "title": title,
        "platforms": pltfrm,
        "release_date": rd,
        "publisher": pblshr,
        "genres": genres,
        "editions": editions,
    }


def list_games(region: REGION = REGION.USA, page: int = 1) -> tuple:
    """
    list_games List games available on the PlayStation Store for the specified region and page.

    Parameters
    ----------
    region : REGION, optional
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
    if region not in REGION:
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


def retrieve_game(concept_id: str, region: REGION = REGION.USA) -> dict:
    """
    Retrieve detailed information about a specific game concept from the PlayStation Store.

    This function fetches and parses the HTML content for a given game concept ID
    and region, extracting various pieces of information such as title, platforms,
    release date, publisher, genres, and available editions.

    Parameters
    ----------
    concept_id : str
        The unique identifier for the game concept.
    region : REGION, optional

    Returns
    -------
    dict
        A dictionary containing detailed information about the game.

    Keys in the returned dictionary:
        - "title" (str): The full title of the game.
        - "platforms" (str): The platforms the game is available on.
        - "release_date" (str): The release date of the game.
        - "publisher" (str): The publisher of the game.
        - "genres" (str): The genres the game belongs to.
        - "editions" (list): A list of dictionaries containing edition-specific information.

    Each edition dictionary contains:
        - "title" (str): The title of the edition.
        - "original_price" (float): The original price of the edition.
        - "discount_price" (float): The discounted price of the edition.
        - "currency" (str): The currency code for the price.

    Raises
    ------
    RegionInvalidError
        If an invalid region is provided.
    """
    if region not in REGION:
        raise RegionInvalidError
    url = _get_retrieve_url(concept_id, region)
    soup = _request(url)
    return _scrap_retrieve(soup)
