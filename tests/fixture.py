import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope="module")
def successful_list_response():
    return BeautifulSoup(
        """
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
        """,
        "html.parser",
    )
