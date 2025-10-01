from src.playstation_store_scrapper import scrapper
from .fixture import successful_list_response
from urllib.request import HTTPError
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
        assert scrapper.list_games() is not None, "list games returns None"

    def test_invalid_region(self):
        with pytest.raises(HTTPError):
            scrapper.list_games(region="xyz")

    def test_scrapping(self, monkeypatch):
        monkeypatch.setattr(scrapper, "_request", successful_list_response)
        assert scrapper.list_games() is not None
