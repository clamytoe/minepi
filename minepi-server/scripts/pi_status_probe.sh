#!/bin/bash
STATUS_FILE="/home/clamytoe/minecraft-server/logs/pi_status.json"
LOG_FILE="/home/clamytoe/minecraft-server/data/logs/latest.log"

echo "🧪 Gathering Pi stats..."

cpu_temp=$(vcgencmd measure_temp | sed "s/temp=//")
load_avg=$(uptime | awk -F'load average:' '{ print $2 }' | xargs)
uptime_days=$(uptime -p | sed "s/up //")

# Count lag warnings
lag_warnings=$(grep "Can't keep up!" "$LOG_FILE" | wc -l)

# Save status to JSON
cat <<EOF > "$STATUS_FILE"
{
  "cpu_temp": "$cpu_temp",
  "load_avg": "$load_avg",
  "uptime": "$uptime_days",
  "lag_warnings": $lag_warnings
}
EOF

echo "✅ Raspberry Pi status updated"
