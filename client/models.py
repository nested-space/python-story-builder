from typing import Optional
import requests
import re

def generate_flash_fiction(base_url: str, silliness: float = 0.0, timeout: Optional[float] = 5.0) -> str:
    """
    Call the Flash‐Fiction Generator API and return the generated text.

    Args:
        base_url:    The root URL where the FastAPI app is served (e.g. "http://localhost:8000").
        silliness:   Float between 0.0 (all serious) and 1.0 (all comical).
        timeout:     How many seconds to wait for the server response.

    Returns:
        The 'text' field from the JSON response.

    Raises:
        requests.HTTPError: If the API returns a 4xx/5xx status.
        ValueError:         If the response JSON doesn't contain 'text'.
    """
    params = {"silliness": silliness}
    response = requests.get(f"{base_url.rstrip('/')}/generate", params=params, timeout=timeout)
    response.raise_for_status()

    payload = response.json()
    try:
        return payload["text"]
    except (TypeError, KeyError):
        raise ValueError(f"Unexpected response format: {payload!r}")

def replace_markers(text):
    # Pattern to match {"key"="value"}
    pattern = r'\{\s*"([^"]+)"\s*=\s*"([^"]+)"\s*\}'

    # Replace each match with <mark marker-type="key">value</mark>
    def replacer(match):
        key = match.group(1)
        value = match.group(2)
        return f' <mark marker-type="{key}">{value}</mark> '

    return re.sub(pattern, replacer, text)
