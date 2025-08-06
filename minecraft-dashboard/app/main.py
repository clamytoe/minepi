import json
from datetime import timedelta

from flask import Flask, jsonify, render_template

app = Flask(__name__)

with open("static/logs/player_sessions.json") as f:
    players = json.load(f)


@app.route("/")
def index():
    return render_template("index.html", players=players)


def parse_duration(duration_str):
    h, m, s = map(int, duration_str.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)


@app.route("/player/<name>")
def player_detail(name):
    data = players.get(name)
    return render_template("player.html", name=name, data=data)


@app.route("/api/player/<name>")
def player_api(name):
    return jsonify(players.get(name, {}))


@app.template_filter("total_achievements")
def total_achievements(sessions):
    return sum(len(s.get("achievements", [])) for s in sessions)


@app.template_filter("total_playtime")
def total_playtime(sessions):
    total = sum((parse_duration(s["session_duration"]) for s in sessions), timedelta())
    return str(total)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
