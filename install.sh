#!/bin/bash
set -e

if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and back in, then run this script again."
    exit 0
fi

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env — fill in your values then run this script again."
    exit 0
fi

# Stop host MPD if running to free port 8000
if systemctl is-active --quiet mpd; then
    echo "Stopping host MPD to free port 8000..."
    sudo systemctl stop mpd
    sudo systemctl disable mpd
fi

docker compose up -d --build
echo "Bot is running. Stream available at http://$(hostname -I | awk '{print $1}'):8000"
