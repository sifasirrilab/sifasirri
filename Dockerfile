FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    imagemagick \
    ffmpeg \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# ImageMagick 7 yetki ayarını yapan garantili komut
RUN MAGICK_POLICY=$(find /etc/ImageMagick-* -name policy.xml) && \
    sed -i 's/policy domain="path" rights="none" pattern="@\*"/policy domain="path" rights="read|write" pattern="@\*"/g' "$MAGICK_POLICY"

ENV IMAGEMAGICK_BINARY=/usr/bin/magick

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "telegram_bot_server.py"]
