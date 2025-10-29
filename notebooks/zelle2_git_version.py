# =====================================================
# ZELLE 2: WEB-INTERFACE MIT GIT-VERSIONEN
# =====================================================
# Diese Zelle lädt die neueste Version der Web-Interface aus Git
# und ermöglicht das Hochladen von Text-Dateien zur Hook-Generierung.

# Stelle sicher, dass die Module aus Zelle 1 geladen sind
try:
    # Prüfe ob Setup erfolgreich war
    if 'setup_status' not in globals() or not setup_status:
        print("⚠️  Setup wurde nicht ausgeführt. Führe Zelle 1 zuerst aus!")
        raise ImportError("Setup fehlt")

    # Prüfe ob Secrets verfügbar sind
    if not setup_status.get('secrets_loaded', False):
        print("⚠️  API-Keys nicht verfügbar. Konfiguriere Colab Secrets!")
        raise ImportError("Secrets fehlen")

    secrets = setup_status['secrets']

    # Importiere Generator-Funktion
    if 'generate_hooks' not in globals():
        print("⚠️  Generator-Funktion nicht verfügbar")
        raise ImportError("Generator fehlt")

    print("✅ Alle Voraussetzungen erfüllt. Starte Web-Interface...")

except ImportError as e:
    print(f"❌ Fehler: {e}")
    print("🔄 Fallback: Lade lokale Version...")

    # Fallback auf lokale Version falls Git-Loading fehlschlägt
    try:
        from zelle2_final import *
        print("✅ Lokale Zelle 2 geladen")
    except ImportError:
        print("❌ Auch lokale Version nicht verfügbar")
        print("Bitte führe Zelle 1 zuerst aus!")

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
with gr.Blocks(title="🎵 Hook-Generator v2.0", theme=gr.themes.Soft()) as interface:

    gr.Markdown("""
    # 🎵 ACID MONK - Hook Generator
    **Version 2.0 mit Git-Versionskontrolle**

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