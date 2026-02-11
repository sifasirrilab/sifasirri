import os
from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
import moviepy.video.fx as vfx

def reels_uret_bot(baslik, alt_metin, dosya_adi):
    try:
        # 1. Klasör Kontrolü
        if not os.path.exists("vitrin_reels"):
            os.makedirs("vitrin_reels")

        # Dosya yolları
        video_bg_path = "assets/arka_plan.mp4"
        logo_path = "assets/logo.png"
        font_path = "assets/BalooBhai2-VariableFont_wght.ttf"

        # --- ARKA PLAN (9:16 Formatı) ---
        bg = (VideoFileClip(video_bg_path)
              .with_duration(7)
              .resized(height=1920))
        
        # Karartma
        bg = bg.with_effects([vfx.MultiplyColor(0.35)])

        # Ortadan dikey kırpma
        if bg.w > 1080:
            bg = bg.cropped(x1=(bg.w-1080)//2, y1=0, x2=(bg.w+1080)//2, y2=1920)

        # --- LOGO ---
        logo = (ImageClip(logo_path)
                .with_duration(7)
                .resized(width=680) 
                .with_position(('center', 400)))
        logo = logo.with_effects([vfx.FadeIn(1.5)])

        # --- BAŞLIK (Altın Sarısı ve Büyük) ---
        txt_baslik = (TextClip(
                        text=baslik, 
                        font=font_path, 
                        font_size=95, 
                        color='#FFD700', 
                        text_align='center',
                        method='caption', 
                        size=(1000, 250)) 
                    .with_duration(7)
                    .with_position(('center', 900))) 
        txt_baslik = txt_baslik.with_effects([vfx.FadeIn(1.5)])

        # --- ALT METİN (Beyaz ve Kibar) ---
        txt_alt = (TextClip(
                        text=alt_metin, 
                        font=font_path, 
                        font_size=50, 
                        color='white',
                        text_align='center',
                        method='caption', 
                        size=(900, 500)) 
                    .with_duration(7)
                    .with_position(('center', 1150))) 
        txt_alt = txt_alt.with_effects([vfx.FadeIn(2.5)])

        # --- BİRLEŞTİRME ---
        final = CompositeVideoClip([bg, logo, txt_baslik, txt_alt], size=(1080, 1920))
        output_file = f"vitrin_reels/REELS_{dosya_adi}.mp4"
        
        # --- PERFORMANS AYARLI KAYIT ---
        # threads=4: İşlemciyi daha verimli kullanır
        # preset='ultrafast': Render süresini kısaltarak Timeout hatasını önler
        final.write_videofile(
            output_file, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            threads=4,
            preset='ultrafast',
            logger=None # Terminal kirliliğini önlemek istersen kalabilir
        )
        
        # Temizlik
        final.close()
        bg.close()
        bg_video_clip = None # Bellek yönetimi için
        
        return output_file

    except Exception as e:
        print(f"❌ REELS MOTORU HATASI: {e}")
        return None