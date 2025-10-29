# =====================================================
# ZELLE 2: VEREINHEITLICHTES WEB-INTERFACE MIT TABS
# =====================================================
# Diese Zelle lädt das neue vereinheitlichte Interface mit Demo und Generator
# in einem einzigen Gradio-Interface mit Tabs.

# =====================================================
# Colab-Sound Unified Interface (Git-Version)
# =====================================================
# Diese Zelle startet das vereinheitlichte Web-Interface für Demo und Hook-Generierung

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
        from src.interface import create_unified_interface

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

print(f"✅ Alle Voraussetzungen erfüllt. Starte vereinheitlichtes Web-Interface (Version: {current_version})...")

# Erstelle und starte das vereinheitlichte Interface
try:
    interface = create_unified_interface(secrets, current_version)

    # Interface starten
    if __name__ == "__main__":
        interface.launch(
            share=False,
            inline=True,
            show_error=True
        )

    print("🎯 Zelle 2 abgeschlossen. Vereinheitlichtes Interface bereit!")

except Exception as e:
    print(f"❌ Fehler beim Starten des Interfaces: {e}")
    print("🔍 Debug-Informationen:")
    print(f"   Aktuelles Verzeichnis: {os.getcwd()}")
    print(f"   src/ existiert: {os.path.exists('src')}")
    if os.path.exists('src'):
        print(f"   Dateien in src/: {os.listdir('src')}")

    print("\n🔧 Fehlerbehebung:")
    print("1. Überprüfe die API-Keys in Colab Secrets")
    print("2. Stelle sicher, dass alle Module korrekt geladen wurden")
    print("3. Bei Netzwerkfehlern: Warte einen Moment und versuche erneut")
    raise