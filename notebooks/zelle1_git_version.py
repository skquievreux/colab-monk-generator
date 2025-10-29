# =====================================================
# ZELLE 1: SETUP, DEMO & GENERATOR-FUNKTION (GIT-VERSION)
# =====================================================
# Diese Zelle lädt Code-Module aus einem Git-Repository für Versionskontrolle
# und führt Setup, Demo und Generator-Funktion aus.

# Git-Loader initialisieren (ändere dies zu deinem Repository)
import sys
import os

# Pfad zu den lokalen Modulen hinzufügen
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from git_loader import init_git_loader, load_from_git
    print("✅ Git-Loader aus lokalem Modul geladen")
except ImportError:
    print("⚠️  Git-Loader nicht verfügbar - verwende direkte Imports")

# TODO: Ersetze 'user/colab-sound' mit deinem tatsächlichen GitHub Repository
REPO_URL = 'user/colab-sound'  # Ändere dies zu deinem Repository!

try:
    # Git-Loader initialisieren
    init_git_loader(REPO_URL, default_branch='main')

    # Module aus Git laden
    print("🔄 Lade Module aus Git-Repository...")

    # Setup-Modul laden
    if load_from_git('setup'):
        from setup import init_colab
        setup_status = init_colab()
    else:
        print("❌ Setup-Modul konnte nicht geladen werden")
        setup_status = None

    # Demo-Modul laden und ausführen
    if load_from_git('demo'):
        from demo import show_hook_demo
        print("🎬 Zeige Demo...")
        show_hook_demo()
    else:
        print("❌ Demo-Modul konnte nicht geladen werden")

    # Generator-Modul laden
    if load_from_git('generator'):
        from generator import generate_hooks
        print("✅ Generator-Modul bereit")
    else:
        print("❌ Generator-Modul konnte nicht geladen werden")

except Exception as e:
    print(f"❌ Fehler beim Laden aus Git: {e}")
    print("🔄 Fallback: Verwende lokale Module...")

    # Fallback auf lokale Module falls Git-Loading fehlschlägt
    try:
        from setup import init_colab
        from demo import show_hook_demo
        from generator import generate_hooks

        setup_status = init_colab()
        show_hook_demo()

        print("✅ Lokale Module erfolgreich geladen")

    except ImportError as e:
        print(f"❌ Auch lokale Module nicht verfügbar: {e}")
        print("Bitte stelle sicher, dass alle Module vorhanden sind.")
        print("Du kannst auch die Module direkt aus dem src/ Verzeichnis importieren:")
        print("from src.setup import init_colab")
        print("from src.demo import show_hook_demo")
        print("from src.generator import generate_hooks")

print("🎯 Zelle 1 abgeschlossen. Jetzt Zelle 2 ausführen!")