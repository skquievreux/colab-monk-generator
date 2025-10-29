# =====================================================
# ZELLE 2: UI MIT DATEI-VORSCHAU (VERSION 1.1)
# =====================================================

%%blocks
import gradio as gr
import webbrowser

def preview_hooks(txt_file):
    """Zeigt Vorschau der zu generierenden Hooks"""
    if txt_file is None:
        return "❌ Keine Datei ausgewählt"

    try:
        with open(txt_file.name, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verwende die globalen Variablen aus Zelle 1
        trenner = globals().get('TRENNER', '---')  # Fallback auf '---'
        parts = [p.strip() for p in content.split(trenner) if p.strip()]

        if not parts:
            return f"❌ Kein Text gefunden oder falsches Trennzeichen ('{trenner}')!\n\n📄 Datei-Inhalt Vorschau:\n{content[:200]}{'...' if len(content) > 200 else ''}"

        preview = f"📁 {len(parts)} Hooks gefunden in Datei: {txt_file.name}\n\n"
        for i, text in enumerate(parts, 1):
            # Zeige ersten 100 Zeichen des Textes
            short_text = text[:100] + "..." if len(text) > 100 else text
            preview += f"🎵 Hook {i:02d}: {short_text}\n"

        preview += f"\n📦 Nach Generierung: {len(parts)} MP3-Dateien in ZIP"
        return preview

    except Exception as e:
        return f"❌ Fehler beim Lesen der Datei: {e}\n\n📄 Dateiname: {txt_file.name if txt_file else 'Unbekannt'}"

def generate_hooks_final(txt_file):
    """Generiert die Hooks nach Bestätigung"""
    if txt_file is None:
        return None, "❌ Keine Datei ausgewählt"

    try:
        with open(txt_file.name, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verwende die globalen Variablen aus Zelle 1
        trenner = globals().get('TRENNER', '---')  # Fallback auf '---'
        parts = [p.strip() for p in content.split(trenner) if p.strip()]

        if not parts:
            return None, f"❌ Kein Text oder falsches Trennzeichen ('{trenner}')!"

        print(f"🚀 Generiere {len(parts)} Hooks aus {txt_file.name}...")

        mp3_files = []
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

        for i, text in enumerate(parts):
            print(f"🎵 Generiere Hook {i+1:02d}: {text[:50]}{'...' if len(text) > 50 else ''}")
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
                print(f"✅ {file} fertig")
            else:
                return None, f"❌ Fehler bei Hook {i+1}: {response.text}"
            time.sleep(1.5)

        zip_name = "ACID_MONK_HOOKS.zip"
        with zipfile.ZipFile(zip_name, 'w') as z:
            for f in mp3_files:
                z.write(f)
                os.remove(f)

        return zip_name, f"✅ {len(mp3_files)} Hooks erfolgreich generiert aus {txt_file.name}!"

    except Exception as e:
        return None, f"❌ Fehler: {e}"

def open_gradio_link():
    """Öffnet den Gradio-Link in einem neuen Tab"""
    try:
        # Versuche den Link aus der globalen Variable zu bekommen
        link = globals().get('gradio_link')
        if link:
            webbrowser.open_new_tab(link)
            return "✅ Link in neuem Tab geöffnet!"
        else:
            return "❌ Link noch nicht verfügbar. Starte zuerst die App."
    except Exception as e:
        return f"❌ Fehler beim Öffnen des Links: {e}"

with gr.Blocks(title="ACID MONK Hook Generator v1.1") as demo:
    gr.Markdown("# ACID MONK Hook Generator v1.1")
    gr.Markdown("🐛 Bugfix: Verbesserte Dateivorschau und Fehlerbehandlung")
    gr.Markdown("1️⃣ Datei hochladen → 2️⃣ Vorschau ansehen → 3️⃣ Generieren")

    with gr.Row():
        txt_in = gr.File(label="TXT-Datei hochladen", file_types=[".txt"])
        preview_btn = gr.Button("👀 Vorschau anzeigen", variant="secondary")

    preview_out = gr.Textbox(
        label="📋 Hook-Vorschau",
        lines=10,
        placeholder="Hier erscheint die Vorschau deiner Hooks..."
    )

    with gr.Row():
        generate_btn = gr.Button("🚀 HOOKS GENERIEREN", variant="primary", size="lg")
        link_btn = gr.Button("🔗 App in neuem Tab öffnen", variant="secondary")

    with gr.Row():
        zip_out = gr.File(label="📦 Deine Hooks als ZIP")
        status = gr.Textbox(label="📊 Status")

    link_status = gr.Textbox(label="🔗 Link-Status", placeholder="Status der Link-Öffnung...")

    # Event-Handler
    preview_btn.click(preview_hooks, txt_in, preview_out)
    generate_btn.click(generate_hooks_final, txt_in, [zip_out, status])
    link_btn.click(open_gradio_link, outputs=link_status)

# Launch mit Link-Speicherung
print("🚀 Starte ACID MONK Hook Generator v1.1...")
try:
    result = demo.launch(share=True, debug=False, show_error=True)
    if result:
        # Speichere Link global für Button-Zugriff
        global gradio_link
        gradio_link = result
        print("✅ App erfolgreich gestartet!")
        print("🔗 Gradio-Link:")
        print(result)
        print("\n💡 Verwende den '🔗 App in neuem Tab öffnen' Button oder kopiere den Link oben.")
    else:
        print("❌ Fehler beim Starten")
except Exception as e:
    print(f"❌ Launch-Fehler: {e}")