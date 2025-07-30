#!/bin/bash
MOD_DIR="./data/mods"
KNOWN_CLIENT_MODS=("shulkerboxtooltip" "notenoughanimations")

echo "🔍 Checking for client-only mods..."
for mod in "${KNOWN_CLIENT_MODS[@]}"; do
  find "$MOD_DIR" -iname "*$mod*.jar" -exec echo "⚠️ Found: {}" \;
done
