from typing import Tuple, Optional, Dict

def clean_and_validate_prices(raw_prices: Dict[str, Optional[str]]) -> Tuple[Optional[Dict[str, float]], str]:
    """
    Cleans the raw price dictionary and validates it.

    Args:
        raw_prices (dict): The raw prices dictionary from the scraper,
                           e.g., {'bank_selling': '4200', 'bank_buying': '4150'}.

    Returns:
        Tuple[Optional[Dict[str, float]], str]: A tuple containing a dictionary of cleaned prices
                                               and a status ('OK' or 'Warning').
                                               Returns (None, 'Warning') if any price is invalid.
    """
    try:
        selling_price_str = raw_prices.get("bank_selling")
        buying_price_str = raw_prices.get("bank_buying")

        if not selling_price_str or not buying_price_str:
            return None, 'Warning'

        selling_price = float(selling_price_str.replace(',', ''))
        buying_price = float(buying_price_str.replace(',', ''))

        if selling_price > 0 and buying_price > 0:
            cleaned_prices = {
                "bank_selling_price": selling_price,
                "bank_buying_price": buying_price
            }
            return cleaned_prices, 'OK'
        else:
            return None, 'Warning'  # Prices are zero or negative

    except (ValueError, TypeError, AttributeError):
        # AttributeError will be raised if raw_prices is not a dict and .get() is called
        return None, 'Warning'  # Conversion to float failed or input was invalid