"""
Interface-Modul für Colab-Sound Projekt
Vereinheitlicht Demo und Hook-Generator in einem Gradio-Interface mit Tabs
"""

import gradio as gr
from pathlib import Path
from typing import Optional, Tuple
from src.generator import generate_hooks
from src.demo import demo_player

class UnifiedInterface:
    """Vereinheitlichtes Interface für Demo und Hook-Generierung"""

    def __init__(self, secrets: dict, current_version: str = "main"):
        """
        Initialisiert das vereinheitlichte Interface

        Args:
            secrets: Dictionary mit API-Keys und Konfiguration
            current_version: Aktuelle Version für Anzeige
        """
        self.secrets = secrets
        self.current_version = current_version

    def process_file(self, file_obj) -> Tuple[Optional[str], str]:
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
                api_key=self.secrets['API_KEY'],
                voice_id=self.secrets['VOICE_ID'],
                separator=self.secrets['TRENNER'],
                output_dir=str(output_dir)
            )

            if zip_path:
                return zip_path, f"✅ {message}"
            else:
                return None, f"❌ {message}"

        except Exception as e:
            return None, f"❌ Fehler bei der Verarbeitung: {e}"

    def run_demo(self) -> str:
        """
        Führt die Demo aus und gibt HTML für Anzeige zurück

        Returns:
            str: HTML-String für Gradio-Anzeige
        """
        try:
            # Demo herunterladen falls nötig
            if not demo_player.download_demo():
                return "<div style='color: red; padding: 20px;'>❌ Demo konnte nicht geladen werden</div>"

            # Demo-Karte anzeigen
            demo_player.show_demo_card()

            # Demo abspielen
            demo_player.play_demo()

            return "<div style='color: green; padding: 20px;'>✅ Demo erfolgreich gestartet! Überprüfe die Audio-Ausgabe oben.</div>"

        except Exception as e:
            return f"<div style='color: red; padding: 20px;'>❌ Demo-Fehler: {e}</div>"

    def create_interface(self) -> gr.Blocks:
        """
        Erstellt das vereinheitlichte Gradio-Interface

        Returns:
            gr.Blocks: Das konfigurierte Interface
        """
        with gr.Blocks(
            title=f"🎵 ACID MONK - Hook Generator {self.current_version}",
            theme=gr.themes.Soft()
        ) as interface:

            gr.Markdown(f"""
            # 🎵 ACID MONK - Hook Generator
            **Version {self.current_version} mit einheitlicher Demo & Generator Oberfläche**

            Entdecke die Möglichkeiten der KI-gestützten Hook-Generierung mit ElevenLabs.
            Verwende die Tabs unten, um zwischen Demo und Hook-Generierung zu wechseln.
            """)

            with gr.Tabs():

                # Tab 1: Demo
                with gr.TabItem("🎧 Demo", id="demo"):
                    gr.Markdown("""
                    ### 🎵 Höre dir ein Beispiel an

                    Diese Demo zeigt dir, wie professionell die generierten Hooks klingen werden.
                    Klicke auf den Button, um eine Beispiel-Audio-Datei zu laden und abzuspielen.
                    """)

                    demo_button = gr.Button(
                        "🎵 Demo abspielen",
                        variant="primary",
                        size="lg"
                    )

                    demo_output = gr.HTML(
                        value="<div style='text-align: center; padding: 20px; color: #666;'>Klicke auf 'Demo abspielen', um zu starten</div>"
                    )

                    demo_button.click(
                        fn=self.run_demo,
                        inputs=[],
                        outputs=[demo_output]
                    )

                # Tab 2: Hook Generator
                with gr.TabItem("🚀 Hook Generator", id="generator"):
                    gr.Markdown("""
                    ### 🎯 Generiere deine eigenen Hooks

                    Lade eine Text-Datei hoch und erstelle professionelle Audio-Hooks mit KI.
                    """)

                    with gr.Row():
                        with gr.Column(scale=2):
                            gr.Markdown("""
                            #### 📤 Datei hochladen
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
                            #### 📋 Anleitung
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
                            label="📊 Status",
                            interactive=False,
                            lines=3,
                            placeholder="Status-Nachrichten werden hier angezeigt..."
                        )

                    with gr.Row():
                        download_output = gr.File(
                            label="📦 Generierte Hooks herunterladen",
                            interactive=False
                        )

                    # Event-Handler
                    generate_btn.click(
                        fn=self.process_file,
                        inputs=[file_input],
                        outputs=[download_output, status_output]
                    )

        return interface

# Globale Funktion für einfache Verwendung
def create_unified_interface(secrets: dict, current_version: str = "main") -> gr.Blocks:
    """
    Erstellt ein vereinheitlichtes Interface für Demo und Hook-Generierung

    Args:
        secrets: Dictionary mit API-Keys und Konfiguration
        current_version: Aktuelle Version für Anzeige

    Returns:
        gr.Blocks: Das konfigurierte Gradio-Interface
    """
    ui = UnifiedInterface(secrets, current_version)
    return ui.create_interface()

# Automatische Info beim Import
if __name__ != "__main__":
    print("🎛️ Interface-Modul geladen")