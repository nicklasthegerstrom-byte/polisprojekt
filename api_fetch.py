import requests

def fetch_events():
    """Fetch events from the Swedish Police API and return as a list."""
    url = "https://polisen.se/api/events"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch events:", response.status_code)
        return []
