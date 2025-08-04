#!/bin/bash
MOD_DIR="/home/clamytoe/minecraft-server/data/mods"
CLIENT_MODS=("shulkerboxtooltip" "notenoughanimations" "lambdynamiclights")

echo "Scanning for client-side mods..." > client_mods_report.txt
for mod in "${CLIENT_MODS[@]}"; do
  matches=$(find "$MOD_DIR" -iname "*$mod*.jar")
  if [ -n "$matches" ]; then
    echo "⚠️ Found client-only mod: $mod" >> client_mods_report.txt
    echo "$matches" >> client_mods_report.txt
  fi
done
