# 🎵 telegram-local-music-bot

> Tired of ads interrupting your music? So was I.

I got fed up with streaming platforms — ads every few minutes, songs disappearing overnight, and paying for a subscription just to listen without interruption. So I built my own.

This is a self-hosted music system controlled entirely through a Telegram bot. Send a YouTube URL, it downloads the audio, adds it to your library, and streams it to any device — no ads, no subscriptions, no nonsense.

---

## ✨ Features

- 📥 **Download music** from YouTube directly via Telegram
- 🎧 **Stream anywhere** over HTTP — works with VLC, browser, or any media player
- ⏯ **Full playback controls** via Telegram keyboard — Play, Pause, Stop, Next, Prev
- 📜 **Browse your library** from chat
- 🔒 **Single-user access** — only your Telegram ID can use the bot
- 🐳 **Fully Dockerized** — runs anywhere with one command

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python + pyTelegramBotAPI | Telegram bot |
| yt-dlp | YouTube audio downloader |
| MPD (Music Player Daemon) | Music server + HTTP streaming |
| MPC | MPD command-line controller |
| ffmpeg | Audio conversion & metadata embedding |
| Docker + Docker Compose | Containerization |

---

## 📋 Requirements

- A Linux server (Ubuntu recommended)
- Docker and Docker Compose
- A Telegram bot token — get one from [@BotFather](https://t.me/BotFather)
- Your Telegram user ID — get it from [@userinfobot](https://t.me/userinfobot)

---

## 🚀 Installation

**1. Clone the repo**
```bash
git clone https://github.com/assachandev/telegram-local-music-bot.git
cd telegram-local-music-bot
```

**2. Run the install script**
```bash
chmod +x install.sh
./install.sh
```
This will install Docker if not present, and generate a `.env` file from the template.

**3. Fill in your credentials**
```bash
nano .env
```
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_USER_ID=your_telegram_user_id
MUSIC_DIR=/music
```

**4. Start the bot**
```bash
./install.sh
```

The bot is now running. Your HTTP stream is live at `http://your-server-ip:8000`.

---

## 📱 Usage

### Downloading Music
Send any YouTube URL directly to the bot:
```
https://youtu.be/xxxxxxxxxxx
```
The bot downloads it as MP3, embeds the thumbnail and metadata, adds it to your library, and queues it automatically.

### Playback Controls

| Button | Action |
|--------|--------|
| ▶ Play | Start playback (auto-loads library if queue is empty) |
| ⏸ Pause | Pause / Resume |
| ⏹ Stop | Stop playback |
| ⏮ Prev | Previous track |
| ⏭ Next | Next track |
| 📜 List Music | Show your music library |

### Listening

Open the stream in VLC, your browser, or any media player:
```
http://your-server-ip:8000
```

---

## 🔒 Remote Access with Tailscale

By default, the stream is only accessible on your local network. To listen from anywhere, use [Tailscale](https://tailscale.com) — a zero-config VPN that connects your devices privately.

**1. Install Tailscale on your server**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**2. Install Tailscale on your phone/device**
Download from [tailscale.com/download](https://tailscale.com/download) and sign in with the same account.

**3. Use your Tailscale IP for the stream**
```
http://100.x.x.x:8000
```

Your music is now accessible from anywhere — without exposing any ports to the public internet.

---

## 🎵 How It Works

```
[You] ── YouTube URL ──▶ [Telegram Bot] ── yt-dlp ──▶ [Music Library]
                                │                             │
                          mpc controls                  mpc update
                                │                             │
                          [MPD Server] ◀────────────────────┘
                                │
                         HTTP Stream :8000
                                │
                  [VLC / Browser / Any Media Player]
```

---

## 📁 Project Structure

```
telegram-local-music-bot/
├── bot.py                 # Telegram bot & playback controls
├── dl_bot.sh              # Download script using yt-dlp
├── mpd.conf               # MPD configuration with HTTP streaming
├── entrypoint.sh          # Container startup (MPD + bot)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── install.sh             # One-command setup
├── .env.example
└── Music/                 # Your music library (gitignored)
```

---

## License

MIT
