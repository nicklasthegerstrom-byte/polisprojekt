from time_filter import get_time_only, format_datetime


def search_events(events, keyword):
    keyword_lower = keyword.lower()  # gör sökningen case-insensitive
    results = []

    for e in events:
        if keyword_lower in e['type'].lower() or keyword_lower in e['summary'].lower():
            results.append(e)
    
    return results

# Användning
def search_input(events):    
    search_word = input("Skriv ett ord att söka efter i händelser: ")
    matches = search_events(events, search_word)

    if matches:
        for e in matches:
            loc = e.get("location", {})
            loc_name = loc.get("name", "Unknown")
            print(f"{format_datetime(e['datetime'])}, {loc_name} | {e['type']} - {e['summary']}")
    else:
        print("Inga händelser matchade din sökning.")
