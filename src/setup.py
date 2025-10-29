"""
Setup-Modul für Colab-Sound Projekt
Behandelt Installation, Konfiguration und Initialisierung
"""

import subprocess
import sys
from typing import List, Dict, Any

class ColabSetup:
    """Verwaltet Setup und Konfiguration für Google Colab"""

    def __init__(self):
        self.installed_packages = set()
        self.config = {}

    def install_packages(self, packages: List[str], quiet: bool = True) -> bool:
        """
        Installiert Python-Packages mit pip

        Args:
            packages: Liste der zu installierenden Packages
            quiet: Unterdrückt Ausgabe wenn True

        Returns:
            bool: True bei Erfolg
        """
        try:
            cmd = [sys.executable, '-m', 'pip', 'install']
            if quiet:
                cmd.append('-q')
            cmd.extend(packages)

            result = subprocess.run(cmd, capture_output=quiet, text=True, check=True)

            for package in packages:
                self.installed_packages.add(package.split('>=')[0].split('==')[0])

            print(f"✅ Packages installiert: {', '.join(packages)}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Fehler bei Package-Installation: {e}")
            return False

    def setup_gradio(self) -> bool:
        """Richtet Gradio für Colab ein"""
        try:
            # Gradio installieren
            if not self.install_packages(["gradio>=4.0"]):
                return False

            # Nest asyncio installieren
            if not self.install_packages(["nest_asyncio"]):
                return False

            # Gradio Extension laden
            get_ipython().run_line_magic('load_ext', 'gradio')

            # Nest asyncio aktivieren
            import nest_asyncio
            nest_asyncio.apply()

            print("✅ Gradio-Setup abgeschlossen")
            return True

        except Exception as e:
            print(f"❌ Fehler beim Gradio-Setup: {e}")
            return False

    def load_secrets(self) -> Dict[str, str]:
        """
        Lädt Secrets aus Google Colab userdata

        Returns:
            Dict mit API_KEY, VOICE_ID, TRENNER
        """
        try:
            from google.colab import userdata

            secrets = {
                'API_KEY': userdata.get('API_KEY'),
                'VOICE_ID': userdata.get('VOICE_ID'),
                'TRENNER': userdata.get('TRENNER')
            }

            # Überprüfe ob alle Secrets vorhanden sind
            missing = [k for k, v in secrets.items() if v is None]
            if missing:
                print(f"⚠️  Fehlende Secrets: {', '.join(missing)}")
                print("Bitte stelle sicher, dass alle Secrets in Colab konfiguriert sind.")
                return {}

            print("✅ Secrets erfolgreich geladen")
            return secrets

        except ImportError:
            print("❌ Google Colab nicht verfügbar - Secrets können nicht geladen werden")
            return {}
        except Exception as e:
            print(f"❌ Fehler beim Laden der Secrets: {e}")
            return {}

    def initialize(self) -> Dict[str, Any]:
        """
        Führt vollständige Initialisierung durch

        Returns:
            Dict mit Setup-Status und Konfiguration
        """
        print("🚀 Starte Colab-Sound Setup...")

        # Gradio Setup
        gradio_ok = self.setup_gradio()

        # Secrets laden
        secrets = self.load_secrets()

        # Status zusammenfassen
        status = {
            'gradio_setup': gradio_ok,
            'secrets_loaded': bool(secrets),
            'packages_installed': list(self.installed_packages),
            'secrets': secrets
        }

        if gradio_ok and secrets:
            print("✅ Setup erfolgreich abgeschlossen!")
        else:
            print("⚠️  Setup unvollständig - einige Funktionen könnten nicht verfügbar sein")

        return status

# Globale Instanz
setup = ColabSetup()

def init_colab():
    """Vereinfachte Initialisierungsfunktion"""
    return setup.initialize()

# Automatische Initialisierung beim Import
if __name__ != "__main__":
    print("🔧 Colab-Sound Setup-Modul geladen")