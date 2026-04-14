FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    mpd mpc ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /app/venv

COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh dl_bot.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
