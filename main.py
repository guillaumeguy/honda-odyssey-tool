#!/usr/bin/env python3
"""
Honda Odyssey Inventory Tool

This tool fetches Honda Odyssey inventory data from the Honda API
for a given zip code and maximum number of dealers.
"""

import json
import requests
import pandas as pd
from typing import Dict, List, Generator, Any
from pathlib import Path


def load_cookie() -> str:
    """
    Load cookie string from .cookie file.

    Returns:
        Cookie string from the .cookie file

    Raises:
        FileNotFoundError: If .cookie file doesn't exist
        IOError: If there's an error reading the file
    """
    cookie_file = Path(".cookie")
    if not cookie_file.exists():
        raise FileNotFoundError(
            ".cookie file not found. Please create a .cookie file with your cookie string. "
            "See README.md for instructions on how to get the cookie."
        )

    try:
        with open(cookie_file, "r") as f:
            cookie = f.read().strip()
            if not cookie:
                raise ValueError("Cookie file is empty")
            return cookie
    except Exception as e:
        raise IOError(f"Error reading .cookie file: {e}")


def get_headers(cookie_string: str) -> Dict[str, str]:
    """
    Build headers for Honda API requests.

    Args:
        cookie_string: The cookie string from browser dev tools

    Returns:
        Dictionary of headers for the API request
    """
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,fr;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://automobiles.honda.com/tools/search-inventory?modelseries=odyssey&modelyear=2025&trimname=Sport-L",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "cookie": cookie_string,
    }


def build_url(zip_code: str, max_dealers: int = 50, year: int = 2025) -> str:
    """
    Build the Honda API URL with the given parameters.

    Args:
        zip_code: The zip code to search for dealers
        max_dealers: Maximum number of dealers to include

    Returns:
        The complete API URL
    """
    return (
        "https://automobiles.honda.com/platform/api/v3/inventoryAndDealers"
        f"?productDivisionCode=A&modelYear={year}&modelGroup=odyssey"
        f"&zipCode={zip_code}&maxDealers={max_dealers}&preferredDealerId=&showOnlineRetailingURL=true"
    )


def fetch_inventory_data(
    zip_code: str, max_dealers: int, cookie_string: str, year: int = 2025
) -> Dict[str, Any]:
    """
    Fetch inventory data from Honda API.

    Args:
        zip_code: The zip code to search for dealers
        max_dealers: Maximum number of dealers to include
        cookie_string: The cookie string from browser dev tools

    Returns:
        JSON response from the API

    Raises:
        requests.RequestException: If the API request fails
    """
    url = build_url(zip_code, max_dealers, year)
    headers = get_headers(cookie_string)

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def build_dealer_map(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Build a mapping of dealer numbers to dealer information.

    Args:
        data: The API response data

    Returns:
        Dictionary mapping dealer numbers to dealer info
    """
    dealer_map = {}
    for dealer in data.get("dealers", []):
        dealer_num = str(dealer.get("DealerNumber"))
        dealer_map[dealer_num] = {
            "name": dealer.get("Name", ""),
            "address1": dealer.get("Address1", ""),
            "city": dealer.get("City", ""),
            "state": dealer.get("State", ""),
            "postal": dealer.get("ZipCode", ""),
            "phone": dealer.get("Phone", ""),
            "lat": dealer.get("Latitude"),
            "lon": dealer.get("Longitude"),
            "retail_url": dealer.get("OnlineRetailingURL", ""),
        }
    return dealer_map


def format_price(price: Any) -> str:
    """
    Format price as currency string.

    Args:
        price: Price value (string, int, or float)

    Returns:
        Formatted price string
    """
    if price is None:
        return "N/A"

    if isinstance(price, str) and price.replace(".", "", 1).isdigit():
        return f"${float(price):,.0f}"
    elif isinstance(price, (int, float)):
        return f"${price:,.0f}"
    else:
        return str(price)


def iter_inventory_rows(data: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    """
    Iterate through inventory data and yield formatted rows.

    Args:
        data: The API response data

    Yields:
        Dictionary containing inventory item information
    """
    dealer_map = build_dealer_map(data)

    for item in data.get("inventory", []):
        dealer_num = str(item.get("DealerNumber"))
        dealer_info = dealer_map.get(dealer_num, {})

        dealer = dealer_info.get("name", "Unknown dealer")
        color = (
            item.get("ExteriorColor") or item.get("ModelBaseColor") or "(Unknown color)"
        )
        price = format_price(item.get("ModelMSRP"))

        trim = item.get("ModelTrim", "")
        inv_type = item.get("InventoryType", "")
        interior_color = item.get("InteriorColor", "")

        for vin_entry in item.get("VINs", []):
            vin = vin_entry.get("VIN")
            if not vin:
                continue

            yield {
                "dealer": dealer,
                "address1": dealer_info.get("address1", ""),
                "city": dealer_info.get("city", ""),
                "state": dealer_info.get("state", ""),
                "postal": dealer_info.get("postal", ""),
                "phone": dealer_info.get("phone", ""),
                "lat": dealer_info.get("lat", ""),
                "lon": dealer_info.get("lon", ""),
                "retail_url": dealer_info.get("retail_url", ""),
                "trim": trim,
                "inv_type": inv_type,
                "color": color,
                "vin": vin,
                "price": price,
                "interior_color": interior_color,
            }


def get_honda_odyssey_inventory(
    zip_code: str, max_dealers: int = 50, cookie_string: str = None, year: int = 2025
) -> pd.DataFrame:
    """
    Main function to fetch Honda Odyssey inventory data.

    Args:
        zip_code: The zip code to search for dealers (e.g., "78723")
        max_dealers: Maximum number of dealers to include (default: 50)
        cookie_string: The cookie string from browser dev tools (optional, will load from .cookie file if not provided)

    Returns:
        pandas DataFrame containing inventory data

    Example:
        >>> df = get_honda_odyssey_inventory("78723", 50)  # Uses .cookie file
        >>> print(df.head())

        >>> # Or provide cookie directly
        >>> cookie = "hpf_id=1d6149ad-892a-4f21-bde9-df77a8b526af; ..."
        >>> df = get_honda_odyssey_inventory("78723", 50, cookie)
    """
    if cookie_string is None:
        cookie_string = load_cookie()

    data = fetch_inventory_data(zip_code, max_dealers, cookie_string, year)

    df = pd.DataFrame([row for row in iter_inventory_rows(data)])
    df["year"] = year

    return df


def main(zip_code: str, max_dealers: int = 50, year: int = 2025):
    """
    Example usage of the Honda Odyssey inventory tool.
    """

    try:
        # The function will automatically load the cookie from .cookie file
        df = get_honda_odyssey_inventory(zip_code, max_dealers, year=year)
        print(f"Found {len(df)} Honda Odyssey vehicles")
        print("\nFirst 5 results:")
        print(df.head())

        # Save to CSV
        df.to_csv("honda_odyssey_inventory.csv", index=False)
        print(f"\nData saved to honda_odyssey_inventory.csv")

    except FileNotFoundError as e:
        print(f"Cookie file error: {e}")
        print("Please create a .cookie file with your cookie string.")
        print("See README.md for instructions on how to get the cookie.")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
