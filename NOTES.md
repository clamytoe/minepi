
# Raspberry Pi - MinePi Setup

|**Component**|**Recommendation**|**Why It Works**|
|:--|:--|:--|
|Raspberry Pi |Raspberry Pi 5 (8GB or 16GB RAM) |Strong multi-core performance and USB 3.0 for fast I/O; enough RAM for Java server and plugins |
|Cooling |Active Cooler or Turbo Cooled Aluminum Case |Keeps temps in check during long sessions, especially with kids jumping in and out |
|Power Supply |27W GaN USB-C (5.1V/5A) |Prevents throttling or stability issues; ideal for sustained CPU bursts |
|Storage |128GB–256GB microSD (or SSD via USB 3.0) |Plenty of space for worlds, logs, and datapacks—Cobblemon alone can bloat things |
|OS |Raspberry Pi OS 64-bit |Maximizes performance and compatibility with server software and monitoring tools |
|Starter Kit |CanaKit or iRasptek Starter Kit |Bundles everything: board, cooler, case, power, storage—easy to deploy without guesswork |

## 🧰 Option 1: Format & Install Your Own Minimal OS

If you prefer a leaner, headless setup:

- Flash Raspberry Pi OS Lite or Ubuntu Server using Raspberry Pi Imager.

- Enable SSH and install Docker manually

  ```bash
  curl <https://get.docker.com> | bash
  sudo usermod -aG docker $USER
  sudo curl -L "https://github.com/docker/compose/releases/download/v2.39.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
  docker --version
  docker-compose --version
  ```

- Use Docker Compose or a shell script to launch and manage the Minecraft container.

- Benefit: No GUI overhead, faster boots, tighter control.

This gives you full flexibility and cleaner logs, especially for automated monitoring or uptime tracking.

## 🖥️ Option 2: Use the Preloaded OS with GUI

If you're okay with keeping the desktop environment:

- Boot into the pre-installed OS.

- Open the terminal, install Docker like above.

- You can still set up the container normally—GUI won’t interfere unless you’re short on resources.

- Bonus: The desktop makes it easier for occasional file browsing, drag-n-drop mods, or visual backup scripting.

Perfect if you're planning on collaborating with family or want quick access for tweaking skin assets or datapacks.

## 🚀 docker-compose.yml **(Starter Template for Modded Java Edition)**

```yaml
name: minepi-server
services:
  mc-server:
    container_name: cobblemon-server
    environment:
      ENABLE_AUTOPAUSE: "true"
      ENABLE_ROLLING_LOGS: "true"
      EULA: "TRUE"
      GID: "1000"
      ICON: server-icon.png
      MEMORY: 6G
      MODRINTH_FORCE_SYNCHRONIZE: "true"
      MODRINTH_LOADER: fabric
      MODRINTH_MODPACK: cobblemon-fabric
      MODRINTH_OVERRIDES_EXCLUSIONS: |
        mods/shulkerboxtooltip-*.jar
      OVERRIDE_ICON: "true"
      PROJECT_ID: 5FFgwNNP
      TYPE: MODRINTH
      UID: "1000"
      VERSION: 1.21.1
    image: itzg/minecraft-server:latest
    networks:
      default: null
    ports:
      - mode: ingress
        target: 25565
        published: "25565"
        protocol: tcp
    restart: unless-stopped
    volumes:
      - type: bind
        source: /home/clamytoe/minepi-server/data
        target: /data
        bind:
          create_host_path: true
networks:
  default:
    name: minepi-server_default
```

## 🧩 Enhancements You Can Layer In

- **World Backups**: Use cron with zip -r and timestamping for nightly backups.

- **Login Tracker**: Shell hook to append player logins to a JSON file.

- **Earn-A-Minute Sync**: Integrate with your reward chart using a small Flask API or bash parser to control uptime logic.

- **Themed Dashboard**: Pipe container stats and player activity to a scrolling HTML page. We can matrix-ify this.

## 📁 Folder Structure Suggestion

```bash
~/cobblemon-server/
├── docker-compose.yml
├── data/               # Persistent server data
├── backups/            # Zipped backups
├── logs/               # Rolling container logs
└── scripts/            # Hooks for login, uptime, etc.
```

## 🛠️ scripts/init_server.sh — Server Setup & Extras

```bash
#!/bin/bash
set -e

# Paths
DATA_DIR="../data"
BACKUP_DIR="../backups"
LOG_FILE="../logs/player_logins.json"
PROPERTIES_FILE="$DATA_DIR/server.properties"

# Create backup folder if missing
mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# Write custom server.properties
cat > "$PROPERTIES_FILE" <<EOF
motd=A New Adventure Awaits!
level-name=world_cobble
max-players=10
online-mode=true
allow-nether=true
enable-command-block=true
view-distance=10
simulation-distance=6
spawn-protection=0
EOF
echo "✔️ Custom server.properties written."

# Timestamped backup
TS=$(date +"%Y%m%d_%H%M")
zip -rq "$BACKUP_DIR/world_$TS.zip" "$DATA_DIR/world"
echo "🗃️ World backed up to world_$TS.zip."

# Fake login event for testing
echo "{\"timestamp\": \"$TS\", \"player\": \"Steve\"}" >> "$LOG_FILE"
echo "📋 Logged sample player login."

echo "✅ Server init complete."
```

## 🕰️ Matching Cron Job: Daily World Backup

Add this to your crontab (`crontab -e`), assuming the shell script lives in `~/cobblemon-server/scripts/init_server.sh`:

```cron
0 2 * * * bash ~/minepi-server/scripts/init_server.sh >> ~/minepi-server/logs/cron_backup.log 2>&1
```

🪄 Runs at 2:00 AM daily 📦 Backs up the world, rewrites server.properties, and appends a mock login 📜 Logs output for debugging.

## 💻 What Could a Shell-Based Dashboard Look Like?

A simple, animated terminal dashboard can give a Matrix-style vibe while showing:

- Server status: 🟢/🔴 based on container uptime

- Current players: names parsed from logs or JSON

- Uptime and memory: pulled from docker stats

- Backup count: zip files in backups/ directory

- Theme-aware: green glow, glitch effect, maybe a Pokéball spinner?

Here's a sneak peek of the style:

```bash
#!/bin/bash
clear
echo -e "\e[32m=== Cobblemon Server Dashboard ===\e[0m"
echo "Status: $(docker inspect -f '{{.State.Status}}' cobblemon-server)"
echo "Players Online:"
jq '.' ~/cobblemon-server/logs/player_logins.json | tail -n 3
echo "Backup Count: $(ls ~/cobblemon-server/backups/*.zip | wc -l)"
echo "Uptime: $(uptime -p)"
```

We can wrap that into a refreshable loop with ASCII art headers, glitch-style separators (`echo -e "\e[5m--==*==--\e[0m"`), or even animate it with `watch -n 10 ./dashboard.sh`.

## 🌟 scripts/dashboard.sh — Cobblemon Server Terminal Dashboard

```bash
#!/bin/bash
clear

# Colors and style
green="\e[32m"
bold="\e[1m"
reset="\e[0m"
glitch="\e[5m"
divider="${glitch}${green}--===[*]===--${reset}"

# Paths
DATA_DIR="../data"
LOG_FILE="../logs/player_logins.json"
BACKUP_DIR="../backups"

# Header
echo -e "${green}${bold}🧬 Cobblemon Terminal Dashboard 🧬${reset}"
echo -e "$divider"

# Server Status
status=$(docker inspect -f '{{.State.Status}}' cobblemon-server 2>/dev/null)
echo -e "🖥️ Server Status: ${bold}${status^^}${reset}"

# Uptime
up=$(uptime -p)
echo -e "⏱️ Host Uptime: $up"

# Backups
count=$(ls $BACKUP_DIR/*.zip 2>/dev/null | wc -l)
latest=$(ls -t $BACKUP_DIR/*.zip 2>/dev/null | head -n 1)
echo -e "🗂️ Backups: $count (latest: ${latest##*/})"

echo -e "$divider"

# Recent Players
echo -e "${bold}🧍 Recent Player Logins:${reset}"
jq -c '. | {time: .timestamp, player: .player}' $LOG_FILE | tail -n 3 | while read entry; do
  time=$(echo "$entry" | jq -r '.time')
  player=$(echo "$entry" | jq -r '.player')
  echo -e "🔹 $player @ $time"
done

# Time Earned (example parser)
total_minutes=$(jq -r '. | select(.player=="Steve") | .timestamp' $LOG_FILE | wc -l)
echo -e "\n🎖️ Steve's Earn-A-Minute Count: ${bold}$total_minutes min${reset}"

echo -e "$divider"
echo -e "${green}🔄 Refresh with: watch -n 10 ./dashboard.sh${reset}"
```

## ✨ Magic MOTD Rotator

**Goal**: Rotate through themed messages for Cobblemon lore, family jokes, or time-based prompts—auto-writing them into `server.properties`.

### 🗂️ scripts/motd_rotator.sh

```bash
#!/bin/bash
# List of magical MOTDs
MOTDS=(
  "🌟 Welcome, Trainer! Your journey begins..."
  "⚡ Powered by Raspberry Pi magic and parental wizardry"
  "💡 Tip: Feed your Pixelmon berries, not cookies!"
  "🕒 Play responsibly. Dinner Time: 6PM sharp!"
  "🧬 Cobblemon research lab online—explore mutations!"
)

# Pick one at random
RANDOM_MOTD=${MOTDS[$RANDOM % ${#MOTDS[@]}]}

# Write it to server.properties
sed -i "s/^motd=.*/motd=${RANDOM_MOTD}/" ../data/server.properties
echo "✅ MOTD set to: $RANDOM_MOTD"
```

💡 You can trigger this script via cron at startup, or every few hours for a fresh experience. Want to tie it to player events or weekday themes next?

## 📈 Playtime Charting

**Goal**: Track login timestamps per player and estimate daily session minutes.

🛠️ scripts/chart_playtime.sh:

```bash
#!/bin/bash
LOG_FILE="../logs/player_logins.json"

echo "📊 Playtime Report"
echo "-------------------------"

jq -r '.player' "$LOG_FILE" | sort | uniq | while read player; do
  count=$(jq -r --arg p "$player" '. | select(.player==$p)' "$LOG_FILE" | wc -l)
  minutes=$((count))  # 1 event = 1 Earn-A-Minute token
  echo "🧍 $player: $minutes min earned"
done
```

🧮 This assumes each log event adds one minute. We can upgrade this to track login+logout pairs with smarter session calculation later, or even visualize with gnuplot or an HTML dashboard.

## 🔁 scripts/orchestrate_magic.sh

```bash
#!/bin/bash
# Orchestrator: MOTD rotation + playtime charting
# 🧙 By Martin & Copilot – modular and magical!

# Set paths
BASE_DIR="$(dirname "$0")"
MOTD_SCRIPT="$BASE_DIR/motd_rotator.sh"
CHART_SCRIPT="$BASE_DIR/chart_playtime.sh"
LOG_FILE="$BASE_DIR/../logs/orchestration.log"

# Timestamp
now=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$now] 🌀 Orchestration begins" >> "$LOG_FILE"

# Rotate MOTD
echo "🔄 Running MOTD rotator..."
bash "$MOTD_SCRIPT" >> "$LOG_FILE" 2>&1

# Chart playtime
echo "📈 Running Playtime Chart..."
bash "$CHART_SCRIPT" >> "$LOG_FILE" 2>&1

echo "[$now] ✅ Orchestration complete" >> "$LOG_FILE"
```

## 🔧 Crontab Integration

Let’s schedule this script every few hours, say every 3:

```cron
0 */3 * * * /home/minecraft/scripts/orchestrate_magic.sh
```

## 🌟 **1. Lore Archive Overlay** (`overlay_motd_archive.html`)

**Goal**: Display past MOTDs with unlockable lore entries based on playtime or calendar date.

**Features**:

- 🧾 MOTD history scrolls as a themed ticker (Matrix-style, if desired)

- 🔓 Unlock requirements (e.g. “playtime > 120 minutes” or “weekends only”)

- ✨ Hidden entries with animated reveal on unlock

- 📜 Lore snippets with fun icons or “research notes”

**Suggested HTML Block**:

```html
<div class="archive">
  <h2>📜 MOTD Lore Archive</h2>
  <ul>
    <li class="unlocked">🌟 Welcome, Trainer! Your journey begins...</li>
    <li class="locked">🔒 Tip: Feed your Pixelmon berries, not cookies!</li>
    <li class="locked playtime">🔓 Unlocked at 240 min playtime</li>
  </ul>
</div>
```

We can sync this to `player_logins.json` and add lore entries based on thresholds. Want the frontend to update with `chart_playtime.sh` logic?

## 📈 2. Magical Stats Dashboard (dashboard.html)

**Goal**: Display current playtime stats, MOTD history, and fun Earn-A-Minute achievements.

**Sections**:

- 🧑 Player cards (name + minutes earned + icon)

- ⏳ Daily Graph (minutes over time)

- 🎖️ Badge progress tracker (optional logic add-on)

- 💬 Latest MOTD log entry + timestamp

**Data Sources**:

- `player_logins.json`

- `motd.log` or `orchestration.log` MOTD section

**Optional Flair**:

- Theme-aware styles (e.g. nighttime palette on weekends 🌒)

- Toggle between retro pixel style or magical parchment UI

- Hover tooltips with “Parental Tip of the Day”

## 🌌 **MOTD Lore Archive Overlay: JSON-fed and Unlockable**

We’ll store MOTD entries in a JSON file with metadata like timestamp, theme, and unlock conditions.

### 📁 `logs/motd_archive.json`

```json
[
  {
    "text": "🌟 Welcome, Trainer! Your journey begins...",
    "timestamp": "2025-07-27T18:00:00",
    "unlocked": true
  },
  {
    "text": "💡 Tip: Feed your Pixelmon berries, not cookies!",
    "timestamp": "2025-07-25T17:00:00",
    "unlock_at_minutes": 240,
    "unlocked": false
  }
]
```

Your orchestration script will log each MOTD into this file. We’ll create a Python/JS frontend that checks player minutes and reveals new entries with shimmer animation ✨.

## 📊 **Magical Stats Dashboard Generator: JSON-to-HTML**

This takes `player_logins.json` + `motd_archive.json` and generates a themed dashboard.

🛠️ `scripts/gen_dashboard.py` **(Starter Outline)**

```python
import json
from datetime import datetime

def load_json(path): return json.load(open(path))

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

    html += "</body></html>"
    with open("../public/dashboard.html", "w") as f: f.write(html)

players = load_json("../logs/player_logins.json")
motds = load_json("../logs/motd_archive.json")
render_dashboard(players, motds)
```

You can style with `magic.css` using parchment gradients or pixel glyphs. 🧾 Want me to sketch some CSS ideas for magical parchment, shimmer unlock effects, or Matrix-style ticker?

And shall we link this dashboard to Raspberry Pi status or Earn-A-Minute badge icons next? 🏆🔗

## 🧠 **Step 1: Raspberry Pi Status Probe**

Here’s a lightweight script to collect status info:

🔍 `scripts/pi_status_probe.sh`

```bash
#!/bin/bash
STATUS_FILE="../logs/pi_status.json"

echo "🧪 Gathering Pi stats..."

cpu_temp=$(vcgencmd measure_temp | sed "s/temp=//")
load_avg=$(uptime | awk -F'load average:' '{ print $2 }' | xargs)
uptime_days=$(uptime -p | sed "s/up //")

# Save status to JSON
cat <<EOF > "$STATUS_FILE"
{
  "cpu_temp": "$cpu_temp",
  "load_avg": "$load_avg",
  "uptime": "$uptime_days"
}
EOF

echo "✅ Raspberry Pi status updated"
```

🔄 You can call this probe from `orchestrate_magic.sh` right after the playtime chart!

## 🧾 **Step 2: Extend Dashboard Renderer**

Your Python script gets a friendly update to show Pi vitals:

```python
pi_status = load_json("../logs/pi_status.json")

html += "<section><h2>🧠 Raspberry Pi Status</h2><ul>"
html += f"<li>🌡️ CPU Temp: {pi_status['cpu_temp']}</li>"
html += f"<li>📉 Load Average: {pi_status['load_avg']}</li>"
html += f"<li>⏱️ Uptime: {pi_status['uptime']}</li>"
html += "</ul></section>"
```

You can style this block with digital meter glyphs, glowing borders, or “diagnostic parchment” visuals. Shall I draft CSS for those?

## 🎈 **Bonus Ideas**

- 🔌 Add SD card usage or memory health with df -h and free -m

- 🔋 Animate the status block if temp/load cross thresholds

- 🪄 Display uptime as “X moons since server awakening”

Want me to sketch the CSS magic next, or build a badge that unlocks when your Pi stays under 60°C for a full week? 🧊🏆

## 🧾 **CSS Magic:** `magic.css` **(Starter Snippet)**

```css
body {
  font-family: 'Papyrus', 'Trebuchet MS', sans-serif;
  background: url('../assets/parchment-bg.jpg') repeat;
  color: #3c2f2f;
  padding: 2em;
  line-height: 1.6;
}

h1, h2 {
  color: #5b3e19;
  text-shadow: 1px 1px #c9b89c;
}

li.unlocked {
  background: linear-gradient(to right, #f5e4c3, #e2d1af);
  border-left: 5px solid #b38b53;
  padding: 0.5em;
  margin: 0.3em 0;
  transition: transform 0.3s;
}
li.unlocked:hover {
  transform: scale(1.03);
}

li.locked {
  color: #7b7b7b;
  background: repeating-linear-gradient(
    45deg,
    #ccc,
    #ccc 10px,
    #bbb 10px,
    #bbb 20px
  );
  border-left: 5px solid #888;
  padding: 0.5em;
  margin: 0.3em 0;
  font-style: italic;
}

.section {
  border: 2px dashed #a68c62;
  background-color: rgba(255, 248, 220, 0.8);
  padding: 1em;
  margin-bottom: 2em;
  box-shadow: 0 4px 6px rgba(77, 52, 25, 0.4);
}
```

🔮 Want to add sparkle when a lore entry unlocks? Here’s a bonus shimmer effect:

```css
@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: 200px 0; }
}
li.unlocked.special {
  background: linear-gradient(90deg, #fff 25%, #e9d8a6 50%, #fff 75%);
  background-size: 400px 100%;
  animation: shimmer 2s infinite;
  border-left: 5px solid gold;
}
```

## Check Firewall Rules

Ensure the Pi isn’t blocking incoming traffic on port 25565. You can check with:

```bash
sudo ufw status
```

If needed:

```bash
sudo ufw allow 25565/tcp
```
