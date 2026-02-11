FROM python:3.10-slim

# Sessiz kurulum için ortam değişkeni
ENV DEBIAN_FRONTEND=noninteractive

# Gerekli sistem paketlerini kur
RUN apt-get update && apt-get install -y \
    imagemagick \
    ffmpeg \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# --- DÜZELTME: ImageMagick 7 klasör yolunu dinamik olarak bul ve yetkiyi aç ---
RUN MAGICK_POLICY=$(find /etc/ImageMagick-* -name policy.xml) && \
    sed -i 's/policy domain="path" rights="none" pattern="@\*"/policy domain="path" rights="read|write" pattern="@\*"/g' "$MAGICK_POLICY"

# MoviePy'nin ImageMagick 7'yi tanıması için ortam değişkeni
ENV IMAGEMAGICK_BINARY=/usr/bin/magick

WORKDIR /app

# Bağımlılıkları kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Botu başlat
CMD ["python", "telegram_bot_server.py"]