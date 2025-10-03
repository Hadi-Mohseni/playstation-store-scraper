from playstation_store_scraper import scraper
from bs4 import BeautifulSoup
import pytest


def successful_request(url: str):
    page = """
    <html>
        <head></head>
        <body>
            <ul>
                <li class="psw-l-w-1/2@mobile-s">
                    <a href="/concept/10014148" >
                        <img src="https://game-one.png"/>
                        <span id="product-name">
                            Game One
                        </span>
                    </a>
                </li>
                <li class="psw-l-w-1/2@mobile-s">
                    <a href="/concept/10014149" >
                        <img src="https://game-two.png"/>
                        <span id="product-name">
                            Game Two
                        </span>
                    </a>
                </li>
            </ul>
            <ol>
                <li><span>1</span></li>
                <li><span>2</span></li>
                <li><span>3</span></li>
                <li><span>4</span></li>
            </ol>
        </body>
    </html>
    """
    return BeautifulSoup(page, "html.parser")


class TestList:

    def test_list(self):
        assert scraper.list_games() is not None, "list games returns None"

    def test_list_with_other_region(self):
        assert scraper.list_games(scraper.REGION.TURKEY_ENGLISH) is not None

    def test_invalid_region(self):
        with pytest.raises(scraper.RegionInvalidError):
            scraper.list_games(region="xyz")

    def test_scrapping(self, monkeypatch):
        monkeypatch.setattr(scraper, "_request", successful_request)
        assert scraper.list_games() is not None
