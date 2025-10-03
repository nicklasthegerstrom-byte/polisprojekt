# Hämta unika orter från dagens events




#ELLER

# location_filter.py


def filter_by_city(events, city_name):
    """
    Returnerar en lista med events som matchar den valda orten.
    """
    return [e for e in events if e.get('location', {}).get('name') == city_name]

def get_unique_cities(events):
    """
    Returnerar en sorterad lista med unika orter från events.
    """
    return sorted({e.get('location', {}).get('name', "Unknown") for e in events})
