import os
from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
import moviepy.video.fx as vfx

def gonderi_olustur(baslik, alt_metin, dosya_adi):
    try:
        # Klasör kontrolü
        if not os.path.exists("vitrin_gonderi"):
            os.makedirs("vitrin_gonderi")

        # Dosya yolları
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

        # 3. Metinler - Timeout hatasını önlemek için basitleştirilmiş render
        # Başlık: Genişlik (w) 850px ile sınırlandı, yükseklik (h) metne göre otomatik.
        txt_baslik = (TextClip(
                        text=baslik, 
                        font=font_path, 
                        font_size=80, 
                        color='#FFD700',
                        text_align='center',
                        method='caption',
                        size=(850, None)) # 'w' yerine size=(genişlik, None)
                    .with_position(('center', 440))) 

        txt_alt = (TextClip(
                        text=alt_metin, 
                        font=font_path, 
                        font_size=40, 
                        color='white', 
                        text_align='center',
                        method='caption',
                        size=(800, None)) # 'w' yerine size=(genişlik, None)
                    .with_position(('center', 680)))

        # 4. Birleştirme ve Kayıt
        final = CompositeVideoClip([bg, logo, txt_baslik, txt_alt], size=(1080, 1080))
        cikti_yolu = f"vitrin_gonderi/IG_{dosya_adi}.png"
        
        # Timeout'u engellemek için bazen logger kapatmak işe yarar
        final.save_frame(cikti_yolu)
        
        # Temizlik
        bg_video.close()
        final.close()
        return True
    except Exception as e:
        print(f"🔥 Post Motoru Hatası: {e}")
        return False