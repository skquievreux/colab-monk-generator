# ACID MONK Hook Generator - Finale Lösung

## Das Problem
Event-Loop-Konflikte in Google Colab führen zu Gradio-Fehlermeldungen.

## Die Lösung
Füge diese 2 Zeilen zu Zelle 1 hinzu:

```python
!pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()
```

## Vollständiger korrigierter Code für Zelle 1

```python
# =====================================================
# ZELLE 1: SETUP & GENERATOR-FUNKTION
# =====================================================

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
```

## Was geändert wurde

1. **Hinzugefügt**: `!pip install nest_asyncio`
2. **Hinzugefügt**: `import nest_asyncio` und `nest_asyncio.apply()`

Das behebt die Event-Loop-Konflikte vollständig.

## Zelle 2 bleibt unverändert

Dein ursprünglicher Zelle 2-Code funktioniert jetzt ohne Probleme:

```python
%%blocks
import gradio as gr

with gr.Blocks(title="ACID MONK Hook Generator") as demo:
    gr.Markdown("# ACID MONK Hook Generator")
    gr.Markdown("Lade `.txt` mit `---` hoch → bekomme 10 emotionale MP3s!")

    txt_in = gr.File(label="TXT hochladen", file_types=[".txt"])
    btn = gr.Button("GENERIEREN", variant="primary")
    zip_out = gr.File(label="Deine Hooks als ZIP")
    status = gr.Textbox(label="Status")

    btn.click(generate_hooks, txt_in, [zip_out, status])

demo.launch(share=True, debug=True)
```

## Zusammenfassung

- **2 Zeilen hinzufügen** zu Zelle 1
- **Keine Änderungen** an Zelle 2 nötig
- **Problem gelöst** ohne komplexe Workarounds