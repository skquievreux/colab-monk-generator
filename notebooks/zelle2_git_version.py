# =====================================================
# ZELLE 2: WEB-INTERFACE MIT GIT-VERSIONEN
# =====================================================
# Diese Zelle lädt die neueste Version der Web-Interface aus Git
# und ermöglicht das Hochladen von Text-Dateien zur Hook-Generierung.

# =====================================================
# Colab-Sound Web-Interface (Git-Version)
# =====================================================
# Diese Zelle startet das Web-Interface für die Hook-Generierung

import sys
import os

# Verwende dasselbe Repository-Verzeichnis wie Zelle 1
REPO_DIR = "/content/colab-sound"

# Stelle sicher, dass wir im richtigen Verzeichnis sind
if os.path.exists(REPO_DIR):
    os.chdir(REPO_DIR)
    print(f"📂 Wechsle zu Repository: {REPO_DIR}")
else:
    print(f"⚠️  Repository-Verzeichnis nicht gefunden: {REPO_DIR}")
    print("Führe Zelle 1 zuerst aus!")

# Pfad für Module hinzufügen
sys.path.insert(0, REPO_DIR)

# Prüfe ob Setup aus Zelle 1 erfolgreich war
if 'setup_status' not in globals() or not setup_status:
    print("⚠️  Setup wurde nicht ausgeführt. Führe Zelle 1 zuerst aus!")
    print("🔄 Versuche Module direkt zu laden...")

    try:
        from src.setup import init_colab
        from src.demo import show_hook_demo
        from src.generator import generate_hooks

        print("🔄 Führe Setup aus...")
        setup_status = init_colab()

    except ImportError as e:
        print(f"❌ Fehler beim Laden der Module: {e}")
        print("Bitte stelle sicher, dass:")
        print("1. Du Zelle 1 zuerst ausgeführt hast")
        print("2. Das Repository wurde geklont")
        print("3. Alle Dateien in src/ vorhanden sind")
        raise

# Prüfe Setup-Status
if not setup_status.get('secrets_loaded', False):
    print("⚠️  API-Keys nicht verfügbar. Konfiguriere Colab Secrets!")
    print("Gehe zu: Runtime → Secrets")
    print("Füge hinzu:")
    print("- API_KEY: Dein ElevenLabs API-Key")
    print("- VOICE_ID: Voice-ID für Sprachsynthese")
    print("- TRENNER: Text-Trennzeichen (z.B. ---)")
    raise ImportError("API-Keys fehlen")

secrets = setup_status['secrets']

# Aktuelle Version ermitteln
current_version = "main"  # Default
try:
    from google.colab import userdata
    current_version = userdata.get('VERSION') or 'main'
except:
    current_version = 'main'

print(f"✅ Alle Voraussetzungen erfüllt. Starte Web-Interface (Version: {current_version})...")

# Web-Interface mit Gradio
import gradio as gr
from pathlib import Path

def process_file(file_obj):
    """
    Verarbeitet die hochgeladene Datei und generiert Hooks

    Args:
        file_obj: Gradio File-Objekt

    Returns:
        Tuple: (zip_path, message)
    """
    if file_obj is None:
        return None, "❌ Bitte wähle eine Text-Datei aus!"

    try:
        # Erstelle temporäres Verzeichnis für Ausgabe
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # Generiere Hooks mit den geladenen Secrets
        zip_path, message = generate_hooks(
            file_path=file_obj.name,
            api_key=secrets['API_KEY'],
            voice_id=secrets['VOICE_ID'],
            separator=secrets['TRENNER'],
            output_dir=str(output_dir)
        )

        if zip_path:
            return zip_path, f"✅ {message}"
        else:
            return None, f"❌ {message}"

    except Exception as e:
        return None, f"❌ Fehler bei der Verarbeitung: {e}"

# Erstelle Gradio Interface
with gr.Blocks(title=f"🎵 Hook-Generator {current_version}", theme=gr.themes.Soft()) as interface:

    gr.Markdown(f"""
    # 🎵 ACID MONK - Hook Generator
    **Version {current_version} mit Git-Versionskontrolle**

    Lade eine Text-Datei hoch und generiere professionelle Audio-Hooks mit ElevenLabs KI.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("""
            ## 📤 Datei hochladen
            Wähle eine Text-Datei mit deinen Hook-Texten aus.
            Verwende das konfigurierte Trennzeichen, um einzelne Hooks zu trennen.
            """)

            file_input = gr.File(
                label="Text-Datei auswählen",
                file_types=[".txt"],
                type="filepath"
            )

            generate_btn = gr.Button(
                "🚀 Hooks generieren",
                variant="primary",
                size="lg"
            )

        with gr.Column(scale=1):
            gr.Markdown("""
            ## 📋 Anleitung
            1. **Text-Datei erstellen**: Schreibe deine Hook-Texte
            2. **Trennzeichen verwenden**: Trenne Hooks mit `---`
            3. **Datei hochladen**: Wähle deine .txt-Datei aus
            4. **Generieren**: Klicke auf "Hooks generieren"
            5. **Herunterladen**: Speichere die ZIP-Datei

            ### 🎯 Beispiel-Format:
            ```
            Hook 1: Dieser Text wird gesprochen
            ---
            Hook 2: Und dieser auch
            ---
            Hook 3: So viele du willst!
            ```
            """)

    # Status und Download-Bereich
    with gr.Row():
        status_output = gr.Textbox(
            label="Status",
            interactive=False,
            lines=3
        )

    with gr.Row():
        download_output = gr.File(
            label="📦 Generierte Hooks herunterladen",
            interactive=False
        )

    # Event-Handler
    generate_btn.click(
        fn=process_file,
        inputs=[file_input],
        outputs=[download_output, status_output]
    )

# Interface starten
if __name__ == "__main__":
    interface.launch(
        share=False,
        inline=True,
        show_error=True
    )

print("🎯 Zelle 2 abgeschlossen. Web-Interface bereit!")