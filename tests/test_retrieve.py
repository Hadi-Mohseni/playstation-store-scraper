from playstation_store_scraper import scraper
from bs4 import BeautifulSoup
import os


def successful_request(url: str) -> BeautifulSoup:
    """
    Mock HTTP request function for testing purposes.

    This function simulates a successful HTTP request by reading from the local
    "detail_page.html" file and parsing its content with BeautifulSoup.

    Parameters
    ----------
    url : str
        The URL of the PlayStation Store page to simulate (not used).

    Returns
    -------
    BeautifulSoup
        A BeautifulSoup object containing the parsed HTML content.
    """
    path = os.path.join(os.path.dirname(__file__), "detail_page.html")
    with open(path) as html:
        return BeautifulSoup("".join(html.readlines()), "html.parser")


class TestRetrieve:

    def test_retrieve(self):
        """
        Test a real game retrieval and make sure retrieve_game works flawlessly.
        """
        assert scraper.retrieve_game("10011898") is not None

    def test_monkeypatching(self, monkeypatch):
        """
        Test a fake retrieval and make sure retrieve_game works flawlessly.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        assert scraper.retrieve_game("10011898") is not None

    def test_title(self, monkeypatch):
        """
        Test if title is scrapped correctly.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["title"] == "EA SPORTS FC™ 26 Standard Edition PS4 & PS5"

    def test_platform(self, monkeypatch):
        """
        Test if platform is scrapped correctly.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["platforms"] == "PS4, PS5"

    def test_release_date(self, monkeypatch):
        """
        Test if release date is scrapped correctly.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["release_date"] == "9/26/2025"

    def test_publisher(self, monkeypatch):
        """
        Test if publisher is scrapped correctly.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["publisher"] == "Electronic Arts Inc"

    def test_genres(self, monkeypatch):
        """
        Test if genres is scrapped correctly.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["genres"] == "Sport"

    def test_editions(self, monkeypatch):
        """
        Test if number of editions is correct.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert len(result["editions"]) == 2

    def test_editions_title(self, monkeypatch):
        """
        Test if editions` title is correct.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["editions"][0]["title"] == "Standard Edition"
        assert result["editions"][1]["title"] == "Ultimate Edition"

    def test_editions_title(self, monkeypatch):
        """
        Test if editions` title is correct.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["editions"][0]["title"] == "Standard Edition"
        assert result["editions"][1]["title"] == "Ultimate Edition"

    def test_editions_price(self, monkeypatch):
        """
        Test if editions` price is correct.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["editions"][0]["original_price"] == "$69.99"
        assert result["editions"][0]["discount_price"] == "$69.99"
        assert result["editions"][1]["original_price"] == "$99.99"
        assert result["editions"][1]["discount_price"] == "$99.99"

    def test_editions_price(self, monkeypatch):
        """
        Test if editions` price is correct.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["editions"][0]["original_price"] == "$69.99"
        assert result["editions"][0]["discount_price"] == "$69.99"
        assert result["editions"][1]["original_price"] == "$99.99"
        assert result["editions"][1]["discount_price"] == "$99.99"

    def test_editions_currency(self, monkeypatch):
        """
        Test if editions` price is correct.
        """
        monkeypatch.setattr(scraper, "_request", successful_request)
        result = scraper.retrieve_game("10011898")
        assert result["editions"][0]["currency"] == "USD"
        assert result["editions"][1]["currency"] == "USD"
