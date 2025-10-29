"""
Generator-Modul für Colab-Sound Projekt
Behandelt die Text-zu-Sprache Konvertierung mit ElevenLabs API
"""

import requests
import zipfile
import os
import time
from typing import Optional, Tuple, List
from pathlib import Path

class HookGenerator:
    """Generiert Audio-Hooks aus Text mit ElevenLabs API"""

    def __init__(self, api_key: str, voice_id: str, separator: str = "---"):
        """
        Initialisiert den Hook-Generator

        Args:
            api_key: ElevenLabs API Key
            voice_id: Voice ID für die Sprachsynthese
            separator: Text-Trennzeichen für einzelne Hooks
        """
        self.api_key = api_key
        self.voice_id = voice_id
        self.separator = separator
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        self.headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

    def parse_text_file(self, file_path: str) -> List[str]:
        """
        Parst eine Text-Datei und extrahiert einzelne Hook-Texte

        Args:
            file_path: Pfad zur Text-Datei

        Returns:
            List[str]: Liste der Hook-Texte
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Teile Text an Trennzeichen und entferne Leerzeilen
            parts = [p.strip() for p in content.split(self.separator) if p.strip()]

            if not parts:
                raise ValueError("Keine gültigen Texte gefunden")

            print(f"📝 {len(parts)} Hook-Texte gefunden")
            return parts

        except FileNotFoundError:
            raise FileNotFoundError(f"Text-Datei nicht gefunden: {file_path}")
        except Exception as e:
            raise Exception(f"Fehler beim Parsen der Text-Datei: {e}")

    def generate_audio_hook(self, text: str, output_path: str) -> bool:
        """
        Generiert einen einzelnen Audio-Hook

        Args:
            text: Hook-Text
            output_path: Ausgabepfad für die MP3-Datei

        Returns:
            bool: True bei Erfolg
        """
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

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                stream=True,
                timeout=30
            )

            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                print(f"🎵 Hook generiert: {output_path}")
                return True
            else:
                error_msg = f"API-Fehler {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Netzwerk-Fehler: {e}")
            return False
        except Exception as e:
            print(f"❌ Unerwarteter Fehler: {e}")
            return False

    def generate_hooks_batch(self, texts: List[str], output_dir: str = ".") -> Tuple[Optional[str], str]:
        """
        Generiert mehrere Hooks und packt sie in eine ZIP-Datei

        Args:
            texts: Liste der Hook-Texte
            output_dir: Ausgabeverzeichnis

        Returns:
            Tuple[Optional[str], str]: (ZIP-Pfad, Status-Nachricht)
        """
        if not texts:
            return None, "Keine Texte zum Generieren"

        print(f"🎯 Starte Generierung von {len(texts)} Hooks...")

        mp3_files = []
        output_dir = Path(output_dir)

        for i, text in enumerate(texts):
            file_name = "02d"
            file_path = output_dir / file_name

            if self.generate_audio_hook(text, str(file_path)):
                mp3_files.append(file_name)
            else:
                return None, f"Fehler bei Hook {i+1}"

            # Rate limiting
            if i < len(texts) - 1:  # Nicht nach dem letzten Hook warten
                time.sleep(1.5)

        if not mp3_files:
            return None, "Keine Hooks erfolgreich generiert"

        # ZIP-Datei erstellen
        zip_name = "ACID_MONK_HOOKS.zip"
        zip_path = output_dir / zip_name

        try:
            with zipfile.ZipFile(zip_path, 'w') as z:
                for mp3_file in mp3_files:
                    file_path = output_dir / mp3_file
                    z.write(str(file_path), mp3_file)
                    # Temporäre MP3-Dateien löschen
                    file_path.unlink(missing_ok=True)

            print(f"📦 ZIP-Datei erstellt: {zip_path}")
            return str(zip_path), f"✅ {len(mp3_files)} Hooks erfolgreich generiert!"

        except Exception as e:
            return None, f"Fehler beim Erstellen der ZIP-Datei: {e}"

    def generate_from_file(self, file_path: str, output_dir: str = ".") -> Tuple[Optional[str], str]:
        """
        Hauptfunktion: Generiert Hooks aus einer Text-Datei

        Args:
            file_path: Pfad zur Text-Datei
            output_dir: Ausgabeverzeichnis

        Returns:
            Tuple[Optional[str], str]: (ZIP-Pfad, Status-Nachricht)
        """
        try:
            # Text parsen
            texts = self.parse_text_file(file_path)

            # Hooks generieren
            return self.generate_hooks_batch(texts, output_dir)

        except Exception as e:
            return None, f"❌ Fehler: {e}"

# Globale Funktion für einfache Verwendung
def generate_hooks(file_path: str, api_key: str, voice_id: str,
                  separator: str = "---", output_dir: str = ".") -> Tuple[Optional[str], str]:
    """
    Vereinfachte Funktion zum Generieren von Hooks

    Args:
        file_path: Pfad zur Text-Datei
        api_key: ElevenLabs API Key
        voice_id: Voice ID
        separator: Text-Trennzeichen
        output_dir: Ausgabeverzeichnis

    Returns:
        Tuple[Optional[str], str]: (ZIP-Pfad, Status-Nachricht)
    """
    generator = HookGenerator(api_key, voice_id, separator)
    return generator.generate_from_file(file_path, output_dir)

# Automatische Info beim Import
if __name__ != "__main__":
    print("🎵 Hook-Generator Modul geladen")