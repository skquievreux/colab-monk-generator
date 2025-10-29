# =====================================================
# ZELLE 2: UI MIT VORSCHAU & LINK-ANZEIGE
# =====================================================

%%blocks
import gradio as gr
import os

def generate_hooks_with_preview(txt_file):
    """Erweiterte Version mit Dateivorschau"""
    try:
        # FIX: txt_file ist ein Pfad → öffne mit open(txt_file.name, 'r')
        with open(txt_file.name, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = [p.strip() for p in content.split(TRENNER) if p.strip()]

        if not parts:
            return None, "Kein Text oder falsches Trennzeichen!", "Keine Dateien gefunden"

        # Erstelle Vorschau der zu generierenden Dateien
        preview_text = "Zu generierende MP3-Dateien:\n\n"
        for i, text in enumerate(parts):
            preview_text += f"hook_{i+1:02d}.mp3: {text[:50]}{'...' if len(text) > 50 else ''}\n"

        print(f"{len(parts)} Hooks gefunden...")
        print("Vorschau:", preview_text)

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
                print(f"✅ {file} generiert")
            else:
                return None, f"Fehler bei Hook {i+1}: {response.text}", preview_text
            time.sleep(1.5)

        zip_name = "ACID_MONK_HOOKS.zip"
        with zipfile.ZipFile(zip_name, 'w') as z:
            for f in mp3_files:
                z.write(f)
                os.remove(f)

        # Zeige generierte Dateien
        generated_files = f"Generierte Dateien in {zip_name}:\n" + "\n".join(mp3_files)

        return zip_name, f"✅ {len(mp3_files)} Hooks generiert!", preview_text + "\n\n" + generated_files

    except Exception as e:
        return None, f"❌ Fehler: {e}", "Fehler bei der Verarbeitung"

with gr.Blocks(title="ACID MONK Hook Generator") as demo:
    gr.Markdown("# ACID MONK Hook Generator")
    gr.Markdown("Lade `.txt` mit `---` hoch → bekomme emotionale MP3-Hooks!")

    txt_in = gr.File(label="TXT hochladen", file_types=[".txt"])
    btn = gr.Button("GENERIEREN", variant="primary")
    zip_out = gr.File(label="Deine Hooks als ZIP")
    status = gr.Textbox(label="Status")
    preview = gr.Textbox(label="Vorschau & generierte Dateien", lines=10)

    btn.click(generate_hooks_with_preview, txt_in, [zip_out, status, preview])

# Launch mit Link-Anzeige
print("🚀 Starte Gradio-App...")
launch_result = demo.launch(share=True, debug=False, show_error=True)

if launch_result:
    print("✅ Gradio-App erfolgreich gestartet!")
    print("🔗 Öffne diesen Link in einem neuen Tab:")
    print(f"https://{launch_result.split('https://')[1]}")
else:
    print("❌ Fehler beim Starten der Gradio-App")