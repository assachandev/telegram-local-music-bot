import telebot
import subprocess
import os
import re
from telebot import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Get configurations from environment variables ---
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER_ID = os.getenv('ALLOWED_USER_ID')
MUSIC_DIR = os.path.abspath(os.getenv('MUSIC_DIR', './Music'))
DOWNLOAD_SCRIPT = os.getenv('DOWNLOAD_SCRIPT_PATH', os.path.abspath("./dl_bot.sh"))

bot = telebot.TeleBot(API_TOKEN, threaded=True)

# Ensure MUSIC_DIR exists
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR, exist_ok=True)

# Function to create a main keyboard
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("▶ Play"),
        types.KeyboardButton("⏸ Pause"),
        types.KeyboardButton("⏹ Stop")
    )
    markup.row(
        types.KeyboardButton("⏮ Prev"),
        types.KeyboardButton("⏭ Next")
    )
    markup.row(types.KeyboardButton("📜 List Music"))
    return markup

# Security decorator
def restricted(func):
    def wrapper(message, *args, **kwargs):
        user_id = str(message.from_user.id)
        if ALLOWED_USER_ID and user_id != str(ALLOWED_USER_ID):
            bot.reply_to(message, f"⛔ Access Denied! Your ID is {user_id}. Please contact the owner.")
            return
        return func(message, *args, **kwargs)
    return wrapper

# Function to validate YouTube URL
def is_yt_url(url):
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    return re.match(pattern, url)

@bot.message_handler(commands=['start'])
@restricted
def send_welcome(message):
    bot.reply_to(message, "🎵 Send a YouTube URL to download.", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "▶ Play")
@restricted
def play_track(message):
    try:
        queue = subprocess.check_output(['mpc', 'playlist'], text=True).strip()
        if not queue:
            subprocess.run('mpc ls | mpc add', shell=True, check=True)
        subprocess.run(['mpc', 'play'], check=True)
        current = subprocess.check_output(['mpc', 'current'], text=True).strip()
        bot.reply_to(message, f"▶ Playing\n🎵 {current}", reply_markup=main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "⏮ Prev")
@restricted
def prev_track(message):
    try:
        subprocess.run(['mpc', 'prev'], check=True)
        current = subprocess.check_output(['mpc', 'current'], text=True).strip()
        bot.reply_to(message, f"⏮ Previous\n🎵 {current}", reply_markup=main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "⏸ Pause")
@restricted
def pause_track(message):
    try:
        subprocess.run(['mpc', 'toggle'], check=True)
        status = subprocess.check_output(['mpc', 'status'], text=True).split('\n')
        state_line = status[1] if len(status) > 1 else ""
        state = "▶ Playing" if "[playing]" in state_line else "⏸ Paused"
        bot.reply_to(message, state, reply_markup=main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "⏭ Next")
@restricted
def next_track(message):
    try:
        subprocess.run(['mpc', 'next'], check=True)
        current = subprocess.check_output(['mpc', 'current'], text=True).strip()
        bot.reply_to(message, f"⏭ Next\n🎵 {current}", reply_markup=main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "⏹ Stop")
@restricted
def stop_track(message):
    try:
        subprocess.run(['mpc', 'stop'], check=True)
        bot.reply_to(message, "⏹ Stopped", reply_markup=main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "📜 List Music")
@bot.message_handler(commands=['list'])
@restricted
def list_music(message):
    try:
        files = []
        for root, dirs, filenames in os.walk(MUSIC_DIR):
            for filename in sorted(filenames):
                if filename.endswith('.mp3'):
                    name = re.sub(r'\s*\[[^\]]+\]\.mp3$', '', filename).strip()
                    files.append(name)

        if not files:
            bot.reply_to(message, "Library is empty.", reply_markup=main_keyboard())
            return

        lines = [f"{i+1}. {name}" for i, name in enumerate(files[:20])]
        total = f"({len(files)} songs)" if len(files) <= 20 else f"(showing 20/{len(files)})"
        list_text = f"🎵 *Library* {total}\n\n" + "\n".join(lines)

        bot.reply_to(message, list_text, parse_mode='Markdown', reply_markup=main_keyboard())
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
@restricted
def handle_text(message):
    url = message.text.strip()
    
    if is_yt_url(url):
        bot.reply_to(message, "📥 Downloading... Please wait.")
        try:
            env = os.environ.copy()
            env['MUSIC_DIR'] = MUSIC_DIR
            process = subprocess.Popen([DOWNLOAD_SCRIPT, url], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE, 
                                        text=True,
                                        env=env)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                bot.reply_to(message, f"✅ Done!\n\n{stdout}", reply_markup=main_keyboard())
            else:
                bot.reply_to(message, f"❌ Failed:\n{stderr}", reply_markup=main_keyboard())
        except Exception as e:
            bot.reply_to(message, f"💣 Error: {str(e)}", reply_markup=main_keyboard())
    else:
        # If it's not a URL and not a command, just show help
        bot.reply_to(message, "Please send a YouTube URL or use the menu below.", reply_markup=main_keyboard())

if __name__ == "__main__":
    if not API_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found.")
        exit(1)
        
    print(f"Bot started. Authorized user: {ALLOWED_USER_ID}")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
