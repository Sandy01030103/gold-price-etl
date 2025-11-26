import requests
from bs4 import BeautifulSoup

def get_bot_gold_price(url: str) -> dict:
    """
    Fetches the Bank of Taiwan Gold Passbook rates (Selling and Buying).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to connect to {url}: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

        
    # 1. Find the specific table. 
    # In your HTML, the table has the title "新臺幣黃金牌價"
    table = soup.find('table', attrs={'title': '新臺幣黃金牌價'})

    if not table: # 確認table是不是空的
        raise ValueError("Could not find the Gold Rate table with title '新臺幣黃金牌價'.")

    # Initialize results
    prices = {
        "bank_selling": None, # The price you pay to buy gold (本行賣出)
        "bank_buying": None   # The price the bank pays to buy back gold (本行買進)
    }

    # 2. Iterate through the table rows (tr)
    rows = table.find_all('tr') # rows=[第一行, 第二行, 第三行, 第四行]
    
    for row in rows:
        # Clean the text of the row to find identifying keywords
        row_text = row.get_text(strip=True) # row_text=品名規格單位：新臺幣元

        # 3. Logic for "Bank Selling" (本行賣出) - The price listed is 4200 in your file
        if "本行賣出" in row_text:
            # The price is in a 'td' with class 'text-right'
            # Note: The cell contains "4200" AND a button text "買進". 
            # We need to extract just the number.
            price_td = row.find('td', class_='text-right') # price_td=4224
            # stripped_strings returns a generator of text parts. 
            # [0] is the price (4200), [1] is the button text (買進)
            prices["bank_selling"] = list(price_td.stripped_strings)[0]

        # 4. Logic for "Bank Buying" (本行買進) - The price listed is 4150 in your file
        if "本行買進" in row_text:
            price_td = row.find('td', class_='text-right')
            prices["bank_buying"] = list(price_td.stripped_strings)[0]

    return prices


# The URL matches the content of your HTML file (Bank of Taiwan Gold Rate)
URL = "https://rate.bot.com.tw/gold/"
if __name__ == "__main__":
    try:
        data = get_bot_gold_price(URL)
        print("-" * 30)
        print("Bank of Taiwan - Gold Passbook (1 Gram)")
        print("-" * 30)
        print(f"Bank Selling (Price to Buy): {data['bank_selling']} TWD")
        print(f"Bank Buying  (Price to Sell): {data['bank_buying']} TWD")
        print("-" * 30)
    except Exception as e:
        print(f"Error: {e}")