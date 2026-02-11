import os
import sys
import logging
import asyncio
import textwrap
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
import moviepy.video.fx as vfx

# 1. Hata Günlüğünü Yapılandır
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. Modülleri Yola Ekle
sys.path.append(os.path.join(os.getcwd(), "scripts"))

try:
    from post_generator import gonderi_olustur
    from generator import reels_uret_bot
    print("✅ Jeneratör modülleri başarıyla bağlandı.")
except Exception as e:
    print(f"❌ Modül yükleme hatası: {e}")

# --- KELİME BÖLMEYİ ENGELLEYEN YARDIMCI FONKSİYON ---
def metni_sar(metin, genislik=40):
    return "\n".join(textwrap.wrap(metin, width=genislik))

# --- GÖNDERİ ÜRETME MOTORU ---
def gonderi_olustur(baslik, alt_metin, dosya_adi):
    try:
        if not os.path.exists("vitrin_gonderi"):
            os.makedirs("vitrin_gonderi")

        bg_path = "assets/arka_plan.mp4"
        logo_path = "assets/logo.png"
        font_path = "assets/BalooBhai2-VariableFont_wght.ttf"

        # 1. Arka Plan
        bg_video = VideoFileClip(bg_path)
        bg = bg_video.to_ImageClip(t=1).resized(height=1080)
        if bg.w > 1080:
            bg = bg.cropped(x1=(bg.w-1080)//2, y1=0, x2=(bg.w+1080)//2, y2=1080)
        bg = bg.with_effects([vfx.MultiplyColor(0.25)])

        # 2. Logo
        logo = (ImageClip(logo_path).resized(width=420).with_position(('center', 120)))

        # 3. Metinler
        # BAŞLIK: Yüksekliği 200px olarak sabit kalsın (Dikey kesilmeyi önler)
        txt_baslik = (TextClip(
                        text=baslik.upper(), 
                        font=font_path, 
                        font_size=80, 
                        color='#FFD700',
                        text_align='center',
                        method='caption',
                        size=(950, 200)) 
                    .with_position(('center', 420))) 

        # ALT METİN: İsteğin üzerine yüksekliği artırdık (None yerine 350px sabitlendi)
        # 350px yükseklik sayesinde satır araları ferahlayacak ve alt kısımlar kesilmeyecek.
        duzenli_alt_metin = metni_sar(alt_metin, genislik=40)
        
        txt_alt = (TextClip(
                        text=duzenli_alt_metin, 
                        font=font_path, 
                        font_size=42, 
                        color='white',
                        text_align='center',
                        method='caption',
                        size=(900, 350)) # Yüksekliği 350 yaparak 'başlıyor' kelimesini kurtardık.
                    .with_position(('center', 690))) # Kutuyu biraz aşağı aldık ki başlıktan uzaklaşsın.

        # 4. Birleştirme ve Kayıt
        final = CompositeVideoClip([bg, logo, txt_baslik, txt_alt], size=(1080, 1080))
        cikti_yolu = f"vitrin_gonderi/IG_{dosya_adi}.png"
        final.save_frame(cikti_yolu)
        
        bg_video.close()
        final.close()
        return True
    except Exception as e:
        print(f"🔥 Post Motoru Hatası: {e}")
        return False

# --- BOT MANTIĞI ---
TOKEN = '8588937681:AAFUXoAqPOBbeNGR-ptt60AjClOBTF0bJOk'

async def icerik_isle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = update.message.text
    if "|" not in mesaj: return

    try:
        parcalar = [p.strip() for p in mesaj.split("|")]
        if len(parcalar) >= 4:
            komut = parcalar[0].lower()
            dosya_adi = parcalar[1].replace(" ", "_")
            baslik = parcalar[2]
            alt_metin = parcalar[3]

            if komut == "gönderi":
                status = await update.message.reply_text("⏳ Açıklama yüksekliği optimize ediliyor...")
                if gonderi_olustur(baslik, alt_metin, dosya_adi):
                    path = f"vitrin_gonderi/IG_{dosya_adi}.png"
                    await asyncio.sleep(1)
                    with open(path, 'rb') as doc:
                        await update.message.reply_document(document=doc, caption="✅ Açıklama ferahlatıldı, kesilme sorunu çözüldü!")
                    await status.delete()
                else:
                    await update.message.reply_text("❌ Hata oluştu.")

            elif komut == "reels":
                status = await update.message.reply_text("🎬 Reels hazırlanıyor...")
                video_path = reels_uret_bot(baslik, alt_metin, dosya_adi)
                if video_path and os.path.exists(video_path):
                    with open(video_path, 'rb') as video:
                        await update.message.reply_video(video=video)
                    await status.delete()

    except Exception as e:
        print(f"Bot ana hata: {e}")

# --- BOT KURULUMU ---
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), icerik_isle))

if __name__ == "__main__":
    print("🤖 Bot AKTİF (Açıklama Yüksekliği Düzenlendi)...")
    application.run_polling()