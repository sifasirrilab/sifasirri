Dockerfile
FROM python:3.10-slim

# Sessiz kurulum için ortam değişkeni
ENV DEBIAN_FRONTEND=noninteractive

# Gerekli sistem paketlerini kur
RUN apt-get update && apt-get install -y \\
    imagemagick \\
    ffmpeg \\
    ghostscript \\
    && rm -rf /var/lib/apt/lists/*

# MoviePy / ImageMagick yetki hatasını kökten çözen ayar
RUN sed -i 's/policy domain="path" rights="none" pattern="@\*"/policy domain="path" rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml

WORKDIR /app

# Önce bağımlılıkları kopyala ve kur (Hızlı build için)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Botu çalıştır
CMD ["python", "telegram_bot_server.py"]