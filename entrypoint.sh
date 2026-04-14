#!/bin/bash
set -e

export PATH="/app/venv/bin:$PATH"

mkdir -p /var/lib/mpd /run/mpd /var/log/mpd

mpd /app/mpd.conf
sleep 2

mpc update --wait 2>/dev/null || true
mpc repeat on

exec python bot.py
