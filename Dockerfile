Dockerfile
FROM python:3.10-slim

# ImageMagick ve gerekli kütüphaneleri kur (Yazıların düzgün çıkması için şart)
RUN apt-get update && apt-get install -y \\
    imagemagick \\
    ffmpeg \\
    && rm -rf /var/lib/apt/lists/*

# ImageMagick güvenlik politikasını düzenle (MoviePy'nin yazı yazabilmesi için)
RUN sed -i 's/policy domain="path" rights="none" pattern="@\*"/policy domain="path" rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml

WORKDIR /app

# Kütüphaneleri kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Botu başlat
CMD ["python", "telegram_bot_server.py"]