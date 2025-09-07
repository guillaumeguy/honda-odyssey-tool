# Honda Odyssey Inventory Tool

A Python tool to fetch Honda Odyssey inventory data from the Honda API for a given zip code and maximum number of dealers.

## Features

- Fetch Honda Odyssey inventory data by zip code
- Configurable maximum number of dealers
- Detailed dealer information including address, phone, and coordinates
- Vehicle details including VIN, trim, color, and price

## Installation

1. Clone this repository
2. Install required dependencies:

```bash
pip install requests pandas
```

## Getting the Required Cookie

To use this tool, you need to obtain a valid cookie string from the Honda website and store it in a `.cookie` file. Here's how:

1. Open Chrome and navigate to [Honda's inventory search page](https://automobiles.honda.com/platform/api/v3/inventoryAndDealers?productDivisionCode=A&modelYear=2025&modelGroup=odyssey&zipCode=78723&maxDealers=50&preferredDealerId=&showOnlineRetailingURL=true)

2. Open Developer Tools:
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux) / `Cmd+Option+I` (Mac)
   - Or right-click and select "Inspect"

3. Go to the **Network** tab

4. Search for a Honda Odyssey in your area (this will make the API call)

5. Look for a request to `inventoryAndDealers` in the network requests

6. Click on that request and look at the **Headers** section (you may need to disable the cache at the top to see all the headers)

7. Find the **Cookie** header and copy the entire value. You may need the other headers (if so, paste the whole thing to GPT-5 and ask it to format it properly )

### Creating the .cookie File

Once you have your cookie string, create a `.cookie` file in the project directory:

```bash
# Create the .cookie file
echo "your_cookie_string_here" > .cookie
```

Or manually create a file named `.cookie` and paste your cookie string into it (without quotes).

**Important**: Make sure the `.cookie` file contains only the cookie string, no additional text or formatting.

### Sample Cookie Header

Here's what a cookie header typically looks like (this is just an example - you need your own):

```
hpf_id=1d6139bd-892a-4f21-bde9-df77a8b526af; cleared-onetrust-cookies=; siteReferer=https://www.google.com/; vehiclename=ODYSSEY; vehicleyear=2026; siteSessionCount=2; OptanonAlertBoxClosed=2025-08-25T18:39:00.655Z; geocalled=true; zipVault=78704; countryCode=US; state=TX; shell#lang=en; AKA_A2=A; ak_bmsc=EC12D261D2152641961505D3F25F2B1A~000000000000000000000000000000~YBAQcGDsF4YdFvaYLQDAtVeCJR2q9RQbsgJTumoDev1s6scp4dMHHzvhsMuumiAOm/...; zipcode=78723; RT="z=1&dm=automobiles.honda.com&si=82692934-cd28-45e2-9916-497104b81340&ss=mfa1qhju&sl=7&tt=1ms&bcn=%2F%2F17de4c20.akstat.io%2F&obo=6&rl=1&nu=delwv79y&cl=ya5w&ld=1403d&r=delwv79y&hd=1403d"; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Sep+07+2025+14%3A19%3A49+GMT-0500+(Central+Daylight+Time)&version=202501.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=26b6b6d2-f57c-44ee-b53b-14d6f2adca87&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&AwaitingReconsent=false&intType=6&geolocation=%3B
```

### Sample Complete Headers

Here's what the complete headers section typically looks like:

```
accept: */*
accept-encoding: gzip, deflate, br, zstd
accept-language: en-US,en;q=0.9,fr;q=0.8
cache-control: no-cache
pragma: no-cache
referer: https://automobiles.honda.com/tools/search-inventory?modelseries=odyssey&modelyear=2025&trimname=Sport-L
sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
cookie: [YOUR_COOKIE_STRING_HERE]
```

## Usage

### Basic Usage

```python
from main import get_honda_odyssey_inventory

# Get inventory for zip code 78723 with max 50 dealers
# The function will automatically load the cookie from .cookie file
df = get_honda_odyssey_inventory("78723", 50)

print(f"Found {len(df)} vehicles")
print(df.head())
```

### Running the Script

1. Create a `.cookie` file with your cookie string (see instructions above)
2. Run the script:

```bash
python main.py
```

### Using in Jupyter Notebook

```python
import pandas as pd
from main import get_honda_odyssey_inventory

# Fetch data (cookie is automatically loaded from .cookie file)
df = get_honda_odyssey_inventory("78723", 50)

# Display results
df
```

## Output

The tool returns a pandas DataFrame with the following columns:

- `dealer`: Dealer name
- `address1`: Street address
- `city`: City
- `state`: State
- `postal`: Postal code
- `phone`: Phone number
- `lat`: Latitude
- `lon`: Longitude
- `retail_url`: Online retailing URL
- `trim`: Vehicle trim level
- `inv_type`: Inventory type
- `color`: Exterior color
- `vin`: Vehicle Identification Number
- `price`: MSRP price

## Important Notes

1. **Cookie Expiration**: Cookies expire after some time. If you get authentication errors, you'll need to get a fresh cookie from the browser.

2. **Rate Limiting**: Be respectful of Honda's servers. Don't make too many requests in a short time period.

3. **Data Accuracy**: This tool fetches data directly from Honda's API. The accuracy depends on Honda's data.

4. **Legal Use**: This tool is for personal use only. Make sure you comply with Honda's terms of service.

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Your cookie has expired. Get a fresh one from the browser.

2. **403 Forbidden**: The request is being blocked. Try getting a fresh cookie or check if you're using the correct headers.

3. **Empty Results**: The zip code might not have any Honda dealers nearby, or the max_dealers parameter might be too low.

### Getting Fresh Cookies

If you encounter authentication issues:

1. Clear your browser cookies for honda.com
2. Visit the Honda inventory page again
3. Perform a search
4. Get the fresh cookie from DevTools
5. Update your `.cookie` file with the new cookie string

## Security Note

The `.cookie` file contains sensitive authentication information. Make sure to:

- Add `.cookie` to your `.gitignore` file to avoid committing it to version control
- Keep your cookie file secure and don't share it with others
- Regenerate your cookie periodically for security

## License

This tool is for educational and personal use only. Please respect Honda's terms of service and use responsibly.
