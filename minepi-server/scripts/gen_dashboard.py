import json

# Paths
BASE_DIR = "/home/clamytoe/minecraft-server"
DATA_DIR = f"{BASE_DIR}/data"


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

    pi_status = load_json(f"{BASE_DIR}/logs/pi_status.json")

    html += "<section><h2>🧠 Raspberry Pi Status</h2><ul>"
    html += f"<li>🌡️ CPU Temp: {pi_status['cpu_temp']}</li>"
    html += f"<li>📉 Load Average: {pi_status['load_avg']}</li>"
    html += f"<li>⏱️ Uptime: {pi_status['uptime']}</li>"
    html += "</ul></section>"

    html += "</body></html>"
    with open(f"{BASE_DIR}/public/dashboard.html", "w") as f:
        f.write(html)


def main():
    players = load_json(f"{BASE_DIR}/logs/player_logins.json")
    motds = load_json(f"{BASE_DIR}/logs/motd_archive.json")
    render_dashboard(players, motds)


if __name__ == "__main__":
    main()
