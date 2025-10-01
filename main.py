from datetime import datetime, timedelta
from api_fetch import fetch_events
from scoring import get_seriousness
from time_filter import filter_recent_events, format_datetime, get_time_only
from search import search_events, search_input

# ----------------------------
# Funktioner
# ----------------------------

# Hämta alla Polisens Events, sätt betyg på dem från funkion i scoring modulen:


def get_most_serious_events(events, min_score=7, max_score=10):
    for event in events:
        event['seriousness'] = get_seriousness(event['type'])
    serious_events = [e for e in events if min_score <= e['seriousness'] <= max_score]
    serious_events_sorted = sorted(serious_events, key=lambda e: (e['datetime'], e['seriousness']), reverse=True)
    return serious_events_sorted


# Sortera ALLA händelser, nu med betyg, men efter tid också, från time_filter modulen.

def get_filtered_recent_events(events, hours):
    serious_events_sorted = get_most_serious_events(events)
    recent_serious_events = filter_recent_events(serious_events_sorted, hours)
    return recent_serious_events

def print_serious_all(events):
    for e in events:
        loc = e.get("location", {})
        loc_name = loc.get("name", "Unknown")
        print(f"{format_datetime(e['datetime'])}, {loc_name} | {e['type']} | {e['summary']}")

def print_serious_time(events):
    for e in events:
        loc = e.get("location", {})
        loc_name = loc.get("name", "Unknown")
        print(f"{get_time_only(e['datetime'])}, {loc_name} | {e['type']} - {e['summary']}")

# ----------------------------
# Hämta events och sortera
# ----------------------------
events = fetch_events()
serious_events_sorted = get_most_serious_events(events)

# ----------------------------
# Input
# ----------------------------
print("Välj tidsperiod att visa händelser från:")
print("1 - Senaste 3 timmar")
print("2 - Senaste 6 timmar")
print("3 - Senaste 12 timmar")
print("4 - Senaste 24 timmar")
print("5 - Alla")
print("6 - Sök efter händelse (ex mord, explosion)")

val = input("Ange nummer: ")

if val == "1":
    hours = 3
elif val == "2":
    hours = 6
elif val == "3":
    hours = 12
elif val == "4":
    hours = 24
elif val == "5":
    print_serious_all(serious_events_sorted)
    hours = None
elif val == "6":
    search_input(events)
    hours = None
else:
    hours = 24

# ----------------------------
# Filtrera och printa efter input
# ----------------------------
if hours is not None:
    recent_serious_events = get_filtered_recent_events(events, hours)
    print_serious_time(recent_serious_events)
