#!/bin/bash
LOG_FILE="../logs/player_logins.json"

echo "📊 Playtime Report"
echo "-------------------------"

jq -r '.player' "$LOG_FILE" | sort | uniq | while read player; do
  count=$(jq -r --arg p "$player" '. | select(.player==$p)' "$LOG_FILE" | wc -l)
  minutes=$((count))  # 1 event = 1 Earn-A-Minute token
  echo "🧍 $player: $minutes min earned"
done