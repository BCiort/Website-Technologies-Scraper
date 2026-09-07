import aiohttp
import asyncio
from typing import Dict, Any


async def fetch_domain_data(session: aiohttp.ClientSession, domain: str) -> Dict[str, Any]:

    url = f"https://{domain}" if not domain.startswith("http") else domain

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    result = {
        "domain": domain,
        "url_fetched": url,
        "html": "",
        "headers": {},
        "cookies": {},
        "error": None
    }

    try:
        timeout = aiohttp.ClientTimeout(total=15)

        async with session.get(url, headers=headers, timeout=timeout, allow_redirects=True, ssl=False) as response:
            result["headers"] = dict(response.headers)
            result["cookies"] = {cookie.key: cookie.value for cookie in session.cookie_jar}

            if response.status < 400:
                result["html"] = await response.text()
            else:
                result["error"] = f"HTTP Status: {response.status}"

    except asyncio.TimeoutError:
        result["error"] = "Timeout"
    except aiohttp.ClientError as e:
        result["error"] = f"Client Error: {str(e)}"
    except Exception as e:
        result["error"] = f"Unexpected Error: {str(e)}"

    return result