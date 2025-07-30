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