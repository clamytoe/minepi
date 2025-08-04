#!/bin/bash
MOD_DIR="../data/mods"
KNOWN_CLIENT_MODS=("shulkerboxtooltip" "notenoughanimations" "lambdynamiclights")

echo "🔍 Checking for known client-only mods..."
for mod in "${KNOWN_CLIENT_MODS[@]}"; do
  find "$MOD_DIR" -iname "*$mod*.jar" -exec echo "⚠️ Found: {} (known client-only)" \;
done

echo ""
echo "📦 Scanning mod metadata..."
for jar in "$MOD_DIR"/*.jar; do
  if unzip -l "$jar" | grep -q "fabric.mod.json"; then
    echo "🔧 [Fabric mod] $jar"
    unzip -p "$jar" fabric.mod.json | jq '. | {id, version, environment, depends}' 2>/dev/null
  elif unzip -l "$jar" | grep -q "META-INF/mods.toml"; then
    echo "🔧 [Forge mod] $jar"
    unzip -p "$jar" META-INF/mods.toml | grep -E 'modId|version|displayName|description' || echo "⚠️ Could not parse mods.toml"
  else
    echo "❓ $jar (Unknown mod format or missing metadata)"
  fi
  echo ""
done
