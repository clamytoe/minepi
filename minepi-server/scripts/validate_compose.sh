#!/bin/bash
echo "🔍 Validating docker-compose.yml..."
docker compose config --quiet && echo "✅ YAML is valid." || echo "❌ YAML has errors."
