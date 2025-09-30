from src.playstation_store_scrapper import scrapper
from urllib.request import HTTPError
import pytest


# @pytest.fixture(scope="module")
# def successful_list_response():
#     return """
#     <html>
#         <head></head>
#         <body>


#         </body>
#     </html>
#     """


class TestList:

    def test_list(self):
        assert scrapper.list_games() is not None, "list games returns None"

    def test_invalid_region(self):
        with pytest.raises(HTTPError):
            scrapper.list_games(region="xyz")
