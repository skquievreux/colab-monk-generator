# =====================================================
# ZELLE 1: SETUP, DEMO & GENERATOR-FUNKTION (GIT-VERSION)
# =====================================================
# Diese Zelle lädt Code-Module aus einem Git-Repository für Versionskontrolle
# und führt Setup, Demo und Generator-Funktion aus.

# =====================================================
# Colab-Sound Setup & Demo (Git-Version)
# =====================================================
# Diese Zelle klont das Repository und lädt die Module

import sys
import os

# Konfiguration aus Colab Secrets laden
try:
    from google.colab import userdata
    REPO_URL = userdata.get('REPO_URL') or 'https://github.com/your-username/colab-sound'
    # VERSION automatisch aus Git-Tags laden (neueste Version)
    try:
        VERSION = userdata.get('VERSION')  # Spezifische Version falls gesetzt
    except:
        VERSION = 'main'  # Fallback auf main falls VERSION nicht existiert
except ImportError:
    # Fallback für lokale Entwicklung
    REPO_URL = "https://github.com/your-username/colab-sound"
    VERSION = "main"  # Lokale Entwicklung verwendet main

REPO_DIR = "/content/colab-sound"  # Colab-Pfad

print("🔗 Colab-Sound Git-Loader")
print(f"📦 Repository: {REPO_URL}")
print(f"🏷️  Version: {VERSION} (automatisch aus Secrets oder 'main' als Fallback)")
print(f"📁 Ziel-Verzeichnis: {REPO_DIR}")
print("💡 Tipp: Setze VERSION in Colab Secrets für spezifische Version (z.B. 'v1.0.0')")

# Repository klonen/updaten
if not os.path.exists(REPO_DIR):
    print("📥 Klone Repository...")
    os.system(f"git clone {REPO_URL} {REPO_DIR}")
    os.chdir(REPO_DIR)
    os.system(f"git checkout {VERSION}")
else:
    print("🔄 Update Repository...")
    os.chdir(REPO_DIR)
    os.system("git fetch")
    os.system(f"git checkout {VERSION}")
    os.system("git pull")

print(f"📂 Wechsle zu: {REPO_DIR}")
os.chdir(REPO_DIR)

# Pfad für Module hinzufügen
sys.path.insert(0, REPO_DIR)

# Abhängigkeiten installieren
print("📦 Installiere Abhängigkeiten...")
os.system("pip install -r requirements.txt -q")

# Module laden
try:
    print("🔄 Lade Module...")

    from src.setup import init_colab
    from src.demo import show_hook_demo
    from src.generator import generate_hooks

    print("✅ Alle Module erfolgreich geladen")

    # Setup ausführen
    print("🚀 Führe Setup aus...")
    setup_status = init_colab()

    # Demo anzeigen
    print("🎬 Zeige Demo...")
    show_hook_demo()

    print("✅ Setup und Demo abgeschlossen!")

except ImportError as e:
    print(f"❌ Fehler beim Laden der Module: {e}")
    print("🔍 Debug-Informationen:")
    print(f"   Aktuelles Verzeichnis: {os.getcwd()}")
    print(f"   src/ existiert: {os.path.exists('src')}")
    if os.path.exists('src'):
        print(f"   Dateien in src/: {os.listdir('src')}")

    print("\n🔧 Fehlerbehebung:")
    print("1. Überprüfe die REPO_URL - ist das Repository öffentlich?")
    print("2. Stelle sicher, dass die Version existiert")
    print("3. Bei Netzwerkfehlern: Warte einen Moment und versuche erneut")
    print("4. Alternativ: Klone manuell mit:")
    print(f"   !git clone {REPO_URL} {REPO_DIR}")
    print(f"   !cd {REPO_DIR} && git checkout {VERSION}")

print("🎯 Zelle 1 abgeschlossen. Jetzt Zelle 2 ausführen!")