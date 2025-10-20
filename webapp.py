# app.py
from flask import Flask, render_template, request
from datetime import datetime, timedelta
import sys
import os

# If your main.py is in the parent folder and you're running from another cwd, adjust path:
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import the logic functions from your main module
from main import (
    load_events,
    get_serious_events,
    search_events_by_word,
    search_events_by_location,
)
from data.scoring import user_seriousness


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the main page. Handle form POSTs (filter by hours, seriousness, keyword, location).
    """
    # default form values
    selected_hours = "all"
    min_seriousness = 7
    keyword = ""
    location = ""

    # On POST, read the form values
    if request.method == "POST":
        selected_hours = request.form.get("hours", "all")
        keyword = request.form.get("keyword", "").strip()
        location = request.form.get("location", "").strip()
        try:
            min_seriousness = int(request.form.get("min_seriousness", 7))
        except (ValueError, TypeError):
            min_seriousness = 7

    # Start from all events (load once)
    events = load_events()

    # 1) Apply seriousness threshold first (use get_serious_events to reuse logic)
    # If hours is chosen we pass it, otherwise None
    hours_param = None if selected_hours == "all" else int(selected_hours)
    filtered = get_serious_events(hours=hours_param, min_score=min_seriousness)

    # 2) If a keyword is provided, search by word (type or summary)
    if keyword:
        # Using the search helper ensures we only search within seriousness threshold:
        filtered = [e for e in search_events_by_word(keyword, min_score=min_seriousness)]

    # 3) If a location is provided, filter by location as well
    if location:
        # intersect previous results with location filter
        loc_matches = search_events_by_location(location, min_score=min_seriousness)
        # keep only events present in both lists (by id if your Event has .id, otherwise compare object identity)
        loc_ids = {getattr(e, "id", None) for e in loc_matches}
        filtered = [e for e in filtered if getattr(e, "id", None) in loc_ids]

    # 4) Final sort: newest first (events without time at the end)
    filtered = sorted(filtered, key=lambda e: e.time or datetime.min, reverse=True)

    return render_template(
        "index.html",
        events=filtered,
        selected_hours=selected_hours,
        min_seriousness=min_seriousness,
        keyword=keyword,
        location=location,
        count=len(filtered),
    )

@app.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        # Update seriousness values from the form
        for key in list(user_seriousness.keys()):
            field_name = f"seriousness_{key}"
            if field_name in request.form:
                try:
                    new_val = int(request.form[field_name])
                    user_seriousness[key] = max(0, min(10, new_val))  # clamp 1–10
                except ValueError:
                    continue

    return render_template("manage.html", seriousness=user_seriousness)


if __name__ == "__main__":
    # For local network access, use host="0.0.0.0". For dev on your machine use default.
    app.run(debug=True)
