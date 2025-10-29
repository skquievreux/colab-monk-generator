# =====================================================
# ZELLE 2: UI MIT RELOAD MODE - VERBESSERTE VERSION
# =====================================================

import gradio as gr
import asyncio
import nest_asyncio
import traceback
from google.colab import forms
import os
import time

# Event-Loop-Fix für Colab
nest_asyncio.apply()

def create_gradio_interface():
    """Erstellt die Gradio-Oberfläche mit Fehlerbehandlung"""
    try:
        with gr.Blocks(title="ACID MONK Hook Generator") as demo:
            gr.Markdown("# ACID MONK Hook Generator")
            gr.Markdown("Lade `.txt` mit `---` hoch → bekomme emotionale MP3-Hooks!")

            txt_in = gr.File(label="TXT hochladen", file_types=[".txt"])
            btn = gr.Button("GENERIEREN", variant="primary")
            zip_out = gr.File(label="Deine Hooks als ZIP")
            status = gr.Textbox(label="Status")

            btn.click(generate_hooks, txt_in, [zip_out, status])

        return demo
    except Exception as e:
        print(f"Fehler beim Erstellen der Gradio-Oberfläche: {e}")
        return None

def launch_gradio_app():
    """Startet die Gradio-App mit verbesserter Fehlerbehandlung"""
    try:
        demo = create_gradio_interface()
        if demo is None:
            print("Fallback: Gradio-Interface konnte nicht erstellt werden.")
            return False

        # Colab-spezifische Launch-Parameter
        demo.launch(
            share=True,
            debug=False,  # Debug auf False setzen um Fehler zu vermeiden
            show_error=True,
            server_name="0.0.0.0",
            server_port=7860,
            quiet=True
        )
        return True
    except Exception as e:
        print(f"Fehler beim Starten der Gradio-App: {e}")
        print("Traceback:", traceback.format_exc())
        return False

def create_colab_form():
    """Erstellt ein Colab-Form als Fallback"""
    try:
        form = forms.Form()

        # Datei-Upload über Colab Forms
        txt_file = form.file_upload("TXT-Datei hochladen", accept=".txt")

        submitted = form.form_submitted("Hook generieren")

        if submitted:
            if txt_file:
                print("🔄 Verarbeite Datei...")
                result = generate_hooks(txt_file)
                if result[0]:
                    print(f"✅ Erfolg: {result[1]}")
                    print("ZIP-Datei wurde erstellt und ist im Files-Bereich verfügbar.")
                    # Zeige verfügbare Dateien
                    files = [f for f in os.listdir('.') if f.endswith('.zip')]
                    if files:
                        print(f"📁 Verfügbare ZIP-Dateien: {', '.join(files)}")
                else:
                    print(f"❌ Fehler: {result[1]}")
            else:
                print("⚠️ Bitte wähle eine .txt-Datei aus.")

        return form
    except Exception as e:
        print(f"Fehler beim Erstellen des Colab-Forms: {e}")
        return None

def manual_generation_interface():
    """Manuelle Schnittstelle für direkte Verwendung"""
    print("\n" + "="*60)
    print("MANUELLE VERWENDUNG")
    print("="*60)
    print("Falls beide UI-Optionen fehlschlagen, verwende diese Funktion:")
    print()
    print("from google.colab import files")
    print("uploaded = files.upload()")
    print("file_name = list(uploaded.keys())[0]")
    print("result = generate_hooks(file_name)")
    print("if result[0]:")
    print("    files.download(result[0])")
    print()
    print("Oder direkt mit einem Dateinamen:")
    print("generate_hooks('deine_datei.txt')")
    print("="*60)

# Hauptlogik mit Fallback
print("Starte ACID MONK Hook Generator...")

success = launch_gradio_app()

if not success:
    print("\n" + "="*50)
    print("FALLBACK: Verwende Colab-Forms")
    print("="*50)

    # Versuche Colab Forms als Alternative
    colab_form = create_colab_form()
    if colab_form:
        colab_form.display()
    else:
        manual_generation_interface()
else:
    print("Gradio-App erfolgreich gestartet!")
    print("Web-Interface ist verfügbar unter dem angezeigten Link.")