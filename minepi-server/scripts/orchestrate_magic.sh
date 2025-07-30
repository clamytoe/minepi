#!/bin/bash
# Orchestrator: MOTD rotation + playtime charting
# 🧙 By Martin Uribe

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