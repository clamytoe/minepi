import json
from datetime import datetime


def load_json(path):
    return json.load(open(path))


def render_dashboard(players, motds):
    html = "<html><head><link rel='stylesheet' href='magic.css'></head><body>"
    html += "<h1>🎮 Playtime & Lore Dashboard</h1>"

    html += "<section><h2>🧑 Players</h2><ul>"
    for p in players:
        html += f"<li>{p['name']}: {p['minutes']} min</li>"
    html += "</ul></section>"

    html += "<section><h2>📜 Lore Archive</h2><ul>"
    for m in motds:
        state = "✅" if m.get("unlocked") else "🔒"
        html += f"<li>{state} {m['text']}</li>"
    html += "</ul></section>"

    pi_status = load_json("../logs/pi_status.json")

    html += "<section><h2>🧠 Raspberry Pi Status</h2><ul>"
    html += f"<li>🌡️ CPU Temp: {pi_status['cpu_temp']}</li>"
    html += f"<li>📉 Load Average: {pi_status['load_avg']}</li>"
    html += f"<li>⏱️ Uptime: {pi_status['uptime']}</li>"
    html += "</ul></section>"

    html += "</body></html>"
    with open("../public/dashboard.html", "w") as f:
        f.write(html)


players = load_json("../logs/player_logins.json")
motds = load_json("../logs/motd_archive.json")
render_dashboard(players, motds)
