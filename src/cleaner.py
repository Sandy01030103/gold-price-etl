from typing import Tuple, Optional

def clean_and_validate_price(raw_price: str) -> Tuple[Optional[float], str]:
    """
    Cleans the raw price string and validates it.

    Args:
        raw_price (str): The raw price string from the scraper.

    Returns:
        Tuple[Optional[float], str]: A tuple containing the cleaned price (as a float)
                                     and a status ('OK' or 'Warning').
                                     Returns (None, 'Warning') if cleaning fails.
    """
    try:
        # Attempt to convert the string to a float
        price = float(raw_price)
        if price > 0:
            return price, 'OK'
        return None, 'Warning' # Price is zero or negative
    except (ValueError, TypeError):
        return None, 'Warning' # Conversion to float failed