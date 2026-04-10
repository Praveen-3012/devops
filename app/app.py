from flask import Flask, render_template
import os

app = Flask(__name__)

# Mood-based music data
MOODS = {
    "Happy": {
        "emoji": "😊",
        "songs": [
            {"name": "Walking on Sunshine", "artist": "Katrina & The Waves", "youtube": "https://www.youtube.com/results?search_query=Walking+on+Sunshine"},
            {"name": "Good as Hell", "artist": "Lizzo", "youtube": "https://www.youtube.com/results?search_query=Good+as+Hell+Lizzo"},
            {"name": "Don't Stop Me Now", "artist": "Queen", "youtube": "https://www.youtube.com/results?search_query=Dont+Stop+Me+Now+Queen"},
            {"name": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "youtube": "https://www.youtube.com/results?search_query=Uptown+Funk"},
            {"name": "Here Comes the Sun", "artist": "The Beatles", "youtube": "https://www.youtube.com/results?search_query=Here+Comes+the+Sun+Beatles"},
            {"name": "Walking on Sunshine", "artist": "Kat Kramer", "youtube": "https://www.youtube.com/results?search_query=Walking+on+Sunshine"}
        ]
    },
    "Sad": {
        "emoji": "😢",
        "songs": [
            {"name": "Someone Like You", "artist": "Adele", "youtube": "https://www.youtube.com/results?search_query=Someone+Like+You+Adele"},
            {"name": "Black", "artist": "Pearl Jam", "youtube": "https://www.youtube.com/results?search_query=Black+Pearl+Jam"},
            {"name": "Skinny Love", "artist": "Bon Iver", "youtube": "https://www.youtube.com/results?search_query=Skinny+Love+Bon+Iver"},
            {"name": "The Night We Met", "artist": "Lord Huron", "youtube": "https://www.youtube.com/results?search_query=The+Night+We+Met"},
            {"name": "Creep", "artist": "Radiohead", "youtube": "https://www.youtube.com/results?search_query=Creep+Radiohead"},
            {"name": "Yesterday", "artist": "The Beatles", "youtube": "https://www.youtube.com/results?search_query=Yesterday+Beatles"}
        ]
    },
    "Chill": {
        "emoji": "😎",
        "songs": [
            {"name": "Sunset Lover", "artist": "Petit Biscuit", "youtube": "https://www.youtube.com/results?search_query=Sunset+Lover+Petit+Biscuit"},
            {"name": "Weightless", "artist": "Marconi Union", "youtube": "https://www.youtube.com/results?search_query=Weightless+Marconi+Union"},
            {"name": "Electric Feel", "artist": "MGMT", "youtube": "https://www.youtube.com/results?search_query=Electric+Feel+MGMT"},
            {"name": "Home", "artist": "Edward Sharpe & The Magnetic Zeros", "youtube": "https://www.youtube.com/results?search_query=Home+Edward+Sharpe"},
            {"name": "Youth", "artist": "The Night Game", "youtube": "https://www.youtube.com/results?search_query=Youth+The+Night+Game"},
            {"name": "Dreams", "artist": "Fleetwood Mac", "youtube": "https://www.youtube.com/results?search_query=Dreams+Fleetwood+Mac"}
        ]
    },
    "Energetic": {
        "emoji": "⚡",
        "songs": [
            {"name": "Blinding Lights", "artist": "The Weeknd", "youtube": "https://www.youtube.com/results?search_query=Blinding+Lights+The+Weeknd"},
            {"name": "Eye of the Tiger", "artist": "Survivor", "youtube": "https://www.youtube.com/results?search_query=Eye+of+the+Tiger+Survivor"},
            {"name": "Pump It Up", "artist": "Endor", "youtube": "https://www.youtube.com/results?search_query=Pump+It+Up+Endor"},
            {"name": "Remember the Name", "artist": "Fort Minor", "youtube": "https://www.youtube.com/results?search_query=Remember+the+Name+Fort+Minor"},
            {"name": "Royals", "artist": "Lorde", "youtube": "https://www.youtube.com/results?search_query=Royals+Lorde"},
            {"name": "Mr. Brightside", "artist": "The Killers", "youtube": "https://www.youtube.com/results?search_query=Mr+Brightside+The+Killers"}
        ]
    }
}

@app.route("/")
def index():
    return render_template("index.html", moods=MOODS)

@app.route("/mood/<mood_name>")
def mood_result(mood_name):
    if mood_name not in MOODS:
        return "Mood not found!", 404
    
    mood_data = MOODS[mood_name]
    return render_template("result.html", mood_name=mood_name, mood_data=mood_data)

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
