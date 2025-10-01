from datetime import datetime, timedelta

def filter_recent_events(events, hours):
    """
    Returnerar endast events som skett de senaste `hours` timmarna.
    Tar bort tidszon och hanterar både 'T' och mellanslag mellan datum och tid.
    
    events: lista med event-dictionaries
    hours: antal timmar att inkludera
    """
    cutoff = datetime.now() - timedelta(hours=hours)
    filtered_events = []

    for e in events:
        dt_str = e['datetime'].strip()  # ta bort extra mellanslag

        # Ta bort tidszon (+02:00 eller -02:00)
        if "+" in dt_str:
            dt_str_clean = dt_str.split(" +")[0]
        elif "-" in dt_str[11:]:
            dt_str_clean = dt_str.split(" -")[0]
        else:
            dt_str_clean = dt_str

        # Byt 'T' mot space om det finns
        dt_str_clean = dt_str_clean.replace("T", " ")

        try:
            # Parsar datumet utan tidszon
            event_time = datetime.strptime(dt_str_clean, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Hoppa över event som inte går att parsa
            continue

        # Filtrera senaste X timmar
        if event_time >= cutoff:
            filtered_events.append(e)

    return filtered_events

def format_datetime(dt_str):
    # ersätt T med mellanslag
    dt_str = dt_str.replace("T", " ")
    # ta bort allt efter + eller - (tidszon)
    dt_str = dt_str.split(" +")[0].split(" -")[0]
    return dt_str


#Fatta denna lite bättre:

def get_time_only(dt_str):
    # ersätt T med mellanslag så det blir lättare
    dt_str = dt_str.replace("T", " ")
    # dela upp datum och tid
    parts = dt_str.split(" ")
    if len(parts) > 1:
        return parts[1]  # andra delen är tiden (HH:MM:SS)
    return dt_str  # fallback om något går fel
