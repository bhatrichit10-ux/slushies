from flask import Flask, render_template
import requests

app = Flask(__name__)

API = "https://clubapi.hackclub.com/club"

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

@app.route('/   club/<clubname>')
def club_stats(clubname):
    try:
        response = requests.get(API, params={"name": clubname})
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return render_template("error.html", message="API error")

    if not data:
        return render_template("error.html", message="Club not found")

        if len(data) == 0:
            return render_template("error.html", message="Club not found")
        data = data[0]  

    fields = data.get("fields", {})

    return render_template(
        'club.html',
        club_name=fields.get("club_name"),
        status=fields.get("club_status"),
        level=fields.get("level"),
        attendees=fields.get("Est. # of Attendees"),
        meeting_days=fields.get("call_meeting_days", []),
        meeting_length=fields.get("call_meeting_length"),
        country=fields.get("venue_address_country"),
        created_time=data.get("createdTime")
    )

if __name__ == "__main__":
    app.run(debug=True)