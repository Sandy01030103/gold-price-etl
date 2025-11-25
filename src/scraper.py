import requests
from bs4 import BeautifulSoup

URL = "https://rate.bot.com.tw/gold"

def fetch_gold_price() -> str:
    """
    Fetches the selling price of gold from the Bank of Taiwan website.

    Returns:
        str: The raw price string scraped from the page.

    Raises:
        Exception: If the request fails or the HTML structure is not as expected.
    """
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Explicitly set the encoding to UTF-8 to prevent garbled characters (mojibake)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table cell ('td') that contains the text "黃金條塊".
        # We use a lambda function to search for the text within the cell, ignoring whitespace.
        gold_bar_cell = soup.find('td', string=lambda text: text and '黃金條塊' in text.strip())

        if not gold_bar_cell:
            raise ValueError("Could not find the '黃金條塊' row in the price table.")

        # The cell we found is the first cell of the row. The price is in the same row ('tr').
        gold_bar_row = gold_bar_cell.find_parent('tr')

        # Find all cells with the class 'text-right' in that row, as these contain the prices.
        price_cells = gold_bar_row.find_all('td', class_='text-right')

        # The last price cell in the "本行賣出" (selling) row is for "100 公克" (100g).
        price_td = price_cells[-1]
        return price_td.text.strip().replace(',', '')

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to retrieve data from {URL}: {e}") from e
    except (AttributeError, IndexError, ValueError) as e:
        raise ValueError(f"Failed to parse HTML structure. The website layout may have changed. Details: {e}") from e