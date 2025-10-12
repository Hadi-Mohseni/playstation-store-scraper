[![Test](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/test.yaml/badge.svg)](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/test.yaml)
[![Publish](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/publish.yaml/badge.svg)](https://github.com/Hadi-Mohseni/playstation-store-scrapper/actions/workflows/publish.yaml)

<hr>
<div align='center'>
# Playstation Store Scrapper 
A web scraper for the PlayStation Store that retrieves and lists all available games with details such as title, price, platform, and more.
</div>

---

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

---

## About the Project
Playstation Store Scraper is a Python package designed to make it easy to extract and list PlayStation Store game information directly from the official website.  
You can retrieve:
- Game titles  
- Prices  
- Platforms  
- Genres  

This package is ideal for developers, data analysts, or hobbyists interested in building apps, bots, or dashboards that use PlayStation Store data.

---

## Getting Started
Follow the steps below to install and start using the scraper.


###  Prerequisites
Before installing, make sure you have:
- **Python 3.8+**
- **pip** (Python package manager)

To verify:
```
python --version
pip --version
```
### Installation
Install the package directly from PyPI using:
```
pip install playstation-store-scraper
```
If you’d like to use the latest development version:
```
git clone https://github.com/Hadi-Mohseni/playstation-store-scrapper.git
cd playstation-store-scrapper
pip install .
```

---

## Usage

List Games
Use `scraper.list_games()` to retrieve a group/page of games for a specific region.

```
from playstation_store_scraper import scraper
from playstation_store_scraper.scraper import region

scraper.list_games(page_number=2, region=region.TURKEY_ENGLISH)
```
This returns a list of available games with metadata such as:

1. Game title
2. Price
3. Platform
4. Concept ID

Retrieve Game Details
Use scraper.retrieve_game() to fetch complete details about a specific game using its Concept ID.
```
from playstation_store_scraper import scraper
from playstation_store_scraper.scraper import region

scraper.retrieve_game(concept_id="10011898", region=region.TURKEY_ENGLISH)
```
          Note : You can get a game's concept_id from the results of scraper.list_games().
---

## Contributing

We love contributions from the community!
If you’d like to improve this project, fix a bug, or add new features, please check out the [Contributing Guidelines](CONTRIBUTING.md).
Your contributions make this project better for everyone.

---

## Code of Conduct

Please note that this project follows a [Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you agree to uphold these values to ensure a positive, respectful community for all contributors and users.

---

## License

This project is licensed under the MIT License — see the [MIT License](LICENSE) file for details.
---
