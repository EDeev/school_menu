#!/bin/sh
# BOT_TOKEN, BOT_ID, TECH_GROUP_ID — из окружения
cp -n /opt/db-seed/* /app/db/ 2>/dev/null || true
exec python bot.py
