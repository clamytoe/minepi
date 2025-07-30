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
level-name=cobblemon
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