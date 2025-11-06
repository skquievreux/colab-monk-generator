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
from src.logger import get_logger
from src.config import get_config

logger = get_logger("generator")
config = get_config()

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

    def validate_text_file(self, file_path: str) -> None:
        """
        Validiert eine Text-Datei vor dem Parsen

        Args:
            file_path: Pfad zur Text-Datei

        Raises:
            ValueError: Bei ungültiger Datei
            FileNotFoundError: Wenn Datei nicht existiert
        """
        # Prüfe ob Datei existiert
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Text-Datei nicht gefunden: {file_path}")

        # Prüfe Dateigröße (aus Config)
        max_size = config.files.max_file_size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise ValueError("Text-Datei ist leer")
        if file_size > max_size:
            raise ValueError(f"Text-Datei zu groß ({file_size} bytes). Maximum: {max_size} bytes")

        # Prüfe ob Datei lesbar ist
        try:
            with open(file_path, 'r', encoding=config.files.default_encoding) as f:
                f.read(1)  # Versuche ein Zeichen zu lesen
        except UnicodeDecodeError:
            raise ValueError(f"Text-Datei hat ungültiges Encoding. Bitte {config.files.default_encoding} verwenden")
        except PermissionError:
            raise ValueError(f"Keine Leseberechtigung für Datei: {file_path}")

    def parse_text_file(self, file_path: str) -> List[str]:
        """
        Parst eine Text-Datei und extrahiert einzelne Hook-Texte

        Args:
            file_path: Pfad zur Text-Datei

        Returns:
            List[str]: Liste der Hook-Texte
        """
        # Validiere Datei zuerst
        self.validate_text_file(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Teile Text an Trennzeichen und entferne Leerzeilen
            parts = [p.strip() for p in content.split(self.separator) if p.strip()]

            if not parts:
                raise ValueError("Keine gültigen Texte gefunden. Stelle sicher, dass die Datei Text enthält.")

            # Validiere einzelne Hook-Texte
            max_text_length = config.elevenlabs.max_text_length
            for i, text in enumerate(parts):
                if len(text) > max_text_length:
                    raise ValueError(f"Hook {i+1} ist zu lang ({len(text)} Zeichen). Maximum: {max_text_length} Zeichen")
                if len(text) < 1:
                    raise ValueError(f"Hook {i+1} ist leer")

            logger.info(f"📝 {len(parts)} Hook-Texte gefunden und validiert")
            return parts

        except FileNotFoundError:
            logger.error(f"Text-Datei nicht gefunden: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Fehler beim Parsen der Text-Datei: {e}")
            raise

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
            "model_id": config.elevenlabs.model_id,
            "voice_settings": {
                "stability": config.elevenlabs.default_stability,
                "similarity_boost": config.elevenlabs.default_similarity_boost,
                "style": config.elevenlabs.default_style
            },
            "output_format": config.elevenlabs.output_format
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                stream=True,
                timeout=config.network.default_timeout
            )

            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        if chunk:
                            f.write(chunk)
                logger.info(f"🎵 Hook generiert: {output_path}")
                return True
            else:
                error_msg = f"API-Fehler {response.status_code}: {response.text}"
                logger.error(error_msg)
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerk-Fehler: {e}")
            return False
        except Exception as e:
            logger.error(f"Unerwarteter Fehler: {e}")
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

        logger.info(f"🎯 Starte Generierung von {len(texts)} Hooks...")

        mp3_files = []
        output_dir = Path(output_dir)

        for i, text in enumerate(texts):
            file_name = f"hook_{i+1:02d}.mp3"
            file_path = output_dir / file_name

            if self.generate_audio_hook(text, str(file_path)):
                mp3_files.append(file_name)
            else:
                return None, f"Fehler bei Hook {i+1}"

            # Rate limiting (aus Config)
            if i < len(texts) - 1:  # Nicht nach dem letzten Hook warten
                time.sleep(config.elevenlabs.rate_limit_delay)

        if not mp3_files:
            return None, "Keine Hooks erfolgreich generiert"

        # ZIP-Datei erstellen (Name aus Config)
        zip_name = config.files.default_zip_name
        zip_path = output_dir / zip_name

        try:
            with zipfile.ZipFile(zip_path, 'w') as z:
                for mp3_file in mp3_files:
                    file_path = output_dir / mp3_file
                    z.write(str(file_path), mp3_file)
                    # Temporäre MP3-Dateien löschen
                    file_path.unlink(missing_ok=True)

            logger.info(f"📦 ZIP-Datei erstellt: {zip_path}")
            return str(zip_path), f"✅ {len(mp3_files)} Hooks erfolgreich generiert!"

        except Exception as e:
            logger.error(f"Fehler beim Erstellen der ZIP-Datei: {e}")
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
    logger.debug("Hook-Generator Modul geladen")