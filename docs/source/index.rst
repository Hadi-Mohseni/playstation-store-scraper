.. playstation store scraper documentation master file, created by
   sphinx-quickstart on Fri Oct  3 18:27:40 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

playstation store scraper documentation
=======================================
A web scraper for the PlayStation Store that retrieves and lists all available games with details such as title, price, platform, and more.


Installation using pip
----------------------

To install the PlayStation Store Scraper package, open your terminal or command prompt and run the following command:

.. code-block:: bash

    $ pip install playstation-store-scraper


Usage
-----
|
    For pulling a group/page of games, use ``scraper.list_games`` function.

>>> from playstation_store_scraper import scraper
>>> from playstation_store_scraper.scraper import region
>>>
>>> scraper.list_games(page_number = 2, region = region.TURKEY_ENGLISH)




For full detail of a game with given `concept ID`, use ``scraper.retrieve_game`` function. 
`Concept ID` is an identifier for a game available on the PlayStation Store. Note that this ID can be gathered using ``scraper.list_games``

>>> from playstation_store_scraper import scraper
>>> from playstation_store_scraper.scraper import region
>>>
>>> scraper.retrieve_game(concept_id = "10011898", region = region.TURKEY_ENGLISH)


.. toctree::
   :maxdepth: 2
   :caption: Contents: