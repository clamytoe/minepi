#!/bin/bash
# network-check.sh — Scan for open ports on local and public interfaces

echo "🔍 Local Listening Ports:"
ss -tuln | awk 'NR>1 {print $1, $5}' | sort

echo ""
echo "🌐 Public IP:"
PUBLIC_IP=$(curl -s https://api.ipify.org)
echo "$PUBLIC_IP"

echo ""
echo "🧪 Scanning Public IP for open ports (common range)..."
nmap -Pn -T4 -p 1-1024 "$PUBLIC_IP" | grep -E '^[0-9]+/tcp'
