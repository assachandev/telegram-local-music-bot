#!/bin/bash
# Script for Bot usage (non-interactive)
# Usage: ./dl_bot.sh "URL" "FOLDER_NAME (optional)"

URL=$1
FOLDER=${2:-"Downloads"}

# Use MUSIC_DIR from environment if set, otherwise default to ~/Music
TARGET_MUSIC_DIR="${MUSIC_DIR:-$HOME/Music}"
DEST="$TARGET_MUSIC_DIR/$FOLDER"

if [ -z "$URL" ]; then
    echo "Usage: $0 <URL> [FOLDER]"
    exit 1
fi

mkdir -p "$DEST"

echo "Downloading from $URL to $DEST..."
yt-dlp -x --audio-format mp3 --embed-thumbnail --add-metadata \
  -o "$DEST/%(title)s [%(id)s].%(ext)s" "$URL"

echo "Updating MPD database..."
mpc update --wait

NEWEST=$(ls -t "$DEST"/*.mp3 2>/dev/null | head -1)
if [ -n "$NEWEST" ]; then
    RELATIVE=$(realpath --relative-to="$TARGET_MUSIC_DIR" "$NEWEST")
    mpc add "$RELATIVE"
    echo "Added to queue: $RELATIVE"
fi

echo "Done!"
