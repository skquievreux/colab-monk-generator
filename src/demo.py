"""
Demo-Modul für Colab-Sound Projekt
Zeigt eine Vorschau des Endprodukts mit Beispiel-Audio
"""

import requests
import os
from typing import Optional
from IPython.display import Audio, display, HTML

class DemoPlayer:
    """Verwaltet Demo-Funktionalität für Hook-Generator"""

    def __init__(self, demo_url: str = "https://pub-aa6154186add4631a26d1261deb9606f.r2.dev/acid-monk-obsession-arrived.mp3"):
        """
        Initialisiert den Demo-Player

        Args:
            demo_url: URL der Demo-MP3-Datei
        """
        self.demo_url = demo_url
        self.demo_file = "demo_hook.mp3"

    def download_demo(self) -> bool:
        """
        Lädt die Demo-MP3-Datei herunter

        Returns:
            bool: True bei Erfolg
        """
        try:
            response = requests.get(self.demo_url, timeout=30)
            response.raise_for_status()

            with open(self.demo_file, "wb") as f:
                f.write(response.content)

            print("✅ Demo-MP3 erfolgreich heruntergeladen")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Netzwerk-Fehler beim Download: {e}")
            return False
        except Exception as e:
            print(f"❌ Fehler beim Download: {e}")
            return False

    def show_demo_card(self) -> None:
        """Zeigt eine ansprechende Demo-Karte mit HTML/CSS"""
        html_content = """
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            border: 2px solid rgba(255,255,255,0.1);
        ">
            <h3 style="margin-top: 0; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                🎧 Hook-Generator Demo
            </h3>
            <p style="margin-bottom: 15px; font-size: 16px; line-height: 1.5;">
                Höre dir an, wie ein typischer generierter Hook klingt. Dies ist eine Vorschau auf das
                <strong>Endprodukt</strong> deiner Text-zu-Sprache-Konvertierung.
            </p>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                <p style="font-size: 14px; margin: 0; opacity: 0.9;">
                    💡 <strong>Tipp:</strong> Die Demo zeigt dir, wie professionell die generierten
                    Hooks klingen werden - perfekt für deine Musikproduktion!
                </p>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 15px;">
                <span style="font-size: 24px;">🎵</span>
                <span style="font-size: 14px; opacity: 0.8;">
                    Beispiel-Hook: "ACID MONK - Obsession Arrived"
                </span>
            </div>
        </div>
        """
        display(HTML(html_content))

    def play_demo(self, autoplay: bool = False) -> None:
        """
        Spielt die Demo-Datei ab

        Args:
            autoplay: Automatische Wiedergabe aktivieren
        """
        if not os.path.exists(self.demo_file):
            print("❌ Demo-Datei nicht gefunden. Lade sie zuerst herunter.")
            return

        try:
            # Audio-Player anzeigen
            audio_player = Audio(self.demo_file, autoplay=autoplay)
            display(audio_player)

            # Download-Link
            download_html = f'''
            <div style="text-align: center; margin-top: 15px;">
                <a href="{self.demo_file}" download
                   style="
                       background: linear-gradient(45deg, #4CAF50, #45a049);
                       color: white;
                       padding: 12px 24px;
                       text-decoration: none;
                       border-radius: 25px;
                       font-weight: bold;
                       box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                       transition: all 0.3s ease;
                       display: inline-block;
                   "
                   onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.3)';"
                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';">
                    ⬇️ Demo herunterladen
                </a>
            </div>
            '''
            display(HTML(download_html))

        except Exception as e:
            print(f"❌ Fehler bei der Audio-Wiedergabe: {e}")

    def run_demo(self) -> None:
        """Führt die komplette Demo durch"""
        print("🎬 Starte Hook-Generator Demo...")

        # Demo herunterladen
        if not self.download_demo():
            print("❌ Demo konnte nicht geladen werden")
            return

        # Demo-Karte anzeigen
        self.show_demo_card()

        # Demo abspielen
        self.play_demo()

        print("✅ Demo abgeschlossen!")

# Globale Instanz und Funktion
demo_player = DemoPlayer()

def show_hook_demo():
    """Vereinfachte Funktion zum Anzeigen der Demo"""
    demo_player.run_demo()

def download_demo_only():
    """Lädt nur die Demo-Datei herunter"""
    return demo_player.download_demo()

# Automatische Info beim Import
if __name__ != "__main__":
    print("🎧 Demo-Modul geladen")