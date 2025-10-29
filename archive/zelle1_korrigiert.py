# =====================================================
# ZELLE 1: SETUP, DEMO & GENERATOR-FUNKTION
# =====================================================
# Diese Zelle richtet die Umgebung ein, zeigt eine Demo des Endprodukts
# und definiert die Hauptfunktion zur Generierung von Hooks aus Text.

!pip install "gradio>=4.0" -q
!pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()
%load_ext gradio

from google.colab import userdata
API_KEY = userdata.get('API_KEY')
VOICE_ID = userdata.get('VOICE_ID')
TRENNER = userdata.get('TRENNER')

print("Setup fertig. Generator bereit.")

# Demo: Lade und spiele eine Beispiel-MP3 ab, um das Endprodukt vorzustellen
import requests
from IPython.display import Audio, display, HTML

demo_url = "https://pub-aa6154186add4631a26d1261deb9606f.r2.dev/acid-monk-obsession-arrived.mp3"
demo_file = "demo_hook.mp3"

try:
    response = requests.get(demo_url)
    if response.status_code == 200:
        with open(demo_file, "wb") as f:
            f.write(response.content)
        print("✅ Demo-MP3 erfolgreich geladen.")
    else:
        print("❌ Fehler beim Laden der Demo-MP3.")
except Exception as e:
    print(f"❌ Fehler beim Laden der Demo: {e}")

# Zeige eine ansprechende Demo mit HTML5 Audio-Player
display(HTML("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: white;">🎧 Hook-Generator Demo</h3>
    <p style="margin-bottom: 15px; font-size: 16px;">
        Höre dir an, wie ein typischer generierter Hook klingt. Dies ist eine Vorschau auf das Endprodukt deiner Text-zu-Sprache-Konvertierung.
    </p>
    <p style="font-size: 14px; opacity: 0.9;">
        Die Demo zeigt dir, wie professionell die generierten Hooks klingen werden - perfekt für deine Musikproduktion!
    </p>
</div>
"""))

# Spiele die Demo-Datei ab
if os.path.exists(demo_file):
    display(Audio(demo_file, autoplay=False))
    display(HTML(f'<p style="text-align: center; margin-top: 10px;"><a href="{demo_file}" download style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">⬇️ Demo herunterladen</a></p>'))
else:
    display(HTML('<p style="color: red;">Demo-Datei konnte nicht geladen werden.</p>'))

import requests
import zipfile
import os
import time

def generate_hooks(txt_file):
    try:
        # FIX: txt_file ist ein Pfad → öffne mit open(txt_file.name, 'r')
        with open(txt_file.name, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = [p.strip() for p in content.split(TRENNER) if p.strip()]

        if not parts:
            return None, "Kein Text oder falsches Trennzeichen!"

        print(f"{len(parts)} Hooks gefunden...")

        mp3_files = []
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

        for i, text in enumerate(parts):
            payload = {
                "text": text,
                "model_id": "eleven_v3",
                "voice_settings": {
                    "stability": 0.0,
                    "similarity_boost": 0.8,
                    "style": 1.0
                },
                "output_format": "mp3_44100_128"
            }
            response = requests.post(url, json=payload, headers=headers, stream=True)

            if response.status_code == 200:
                file = f"hook_{i+1:02d}.mp3"
                with open(file, "wb") as f:
                    for chunk in response.iter_content(1024):
                        if chunk: f.write(chunk)
                mp3_files.append(file)
            else:
                return None, f"Fehler bei Hook {i+1}: {response.text}"
            time.sleep(1.5)

        zip_name = "ACID_MONK_HOOKS.zip"
        with zipfile.ZipFile(zip_name, 'w') as z:
            for f in mp3_files:
                z.write(f)
                os.remove(f)

        return zip_name, f"{len(mp3_files)} Hooks generiert!"

    except Exception as e:
        return None, f"Fehler: {e}"

print("Zelle 1 abgeschlossen. Jetzt Zelle 2 ausführen!")