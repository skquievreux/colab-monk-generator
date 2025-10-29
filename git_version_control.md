# Git-Versionskontrolle für Colab-Sound Projekt

## Übersicht
Dieses Dokument beschreibt die Implementierung der Versionskontrolle für das Colab-Sound Projekt, um einzelne Code-Elemente versionieren und aus einem Git-Repository laden zu können.

## Aktuelle Struktur
- Mehrere Versionen der Colab-Zellen (zelle1_*.py, zelle2_*.py)
- Verschiedene Lösungsansätze in separaten Dateien
- Keine zentrale Versionskontrolle

## Geplante Architektur

### 1. Git-Repository Struktur
```
colab-sound/
├── src/
│   ├── setup.py          # Setup und Konfiguration
│   ├── generator.py      # Hook-Generator Funktion
│   ├── demo.py          # Demo-Funktionalität
│   └── utils.py         # Hilfsfunktionen
├── notebooks/
│   ├── zelle1.ipynb     # Colab-Zelle 1
│   └── zelle2.ipynb     # Colab-Zelle 2
├── requirements.txt
├── README.md
└── .gitignore
```

### 2. Git-Loader Funktion
```python
def load_from_git(repo_url, version='main', module='setup'):
    """
    Lädt ein Modul aus einem Git-Repository

    Args:
        repo_url (str): GitHub Repository URL
        version (str): Branch oder Tag (default: 'main')
        module (str): Zu ladendes Modul ('setup', 'generator', 'demo')
    """
    import requests

    base_url = f'https://raw.githubusercontent.com/{repo_url}/{version}/src'
    url = f'{base_url}/{module}.py'

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Führe den Code im globalen Namespace aus
        exec(response.text, globals())
        print(f"✅ Modul '{module}' aus {version} erfolgreich geladen")

    except Exception as e:
        print(f"❌ Fehler beim Laden von {module}: {e}")
```

### 3. Verwendung in Colab
```python
# Lade spezifische Versionen
load_from_git('user/colab-sound', 'v1.0.0', 'setup')
load_from_git('user/colab-sound', 'main', 'generator')
load_from_git('user/colab-sound', 'feature/demo', 'demo')
```

## Vorteile
- **Modularität**: Einzelne Komponenten können unabhängig versioniert werden
- **Rollback**: Einfaches Zurücksetzen auf vorherige Versionen
- **Collaboration**: Mehrere Entwickler können parallel arbeiten
- **Testing**: Neue Features können in Branches getestet werden

## Implementierungsschritte
1. Git-Repository erstellen
2. Code in Module aufteilen
3. Git-Loader Funktion implementieren
4. Colab-Zellen für Git-Loading anpassen
5. Dokumentation erstellen

## Sicherheitsaspekte
- Nur vertrauenswürdige Repositories verwenden
- Code-Review vor dem Merge in main
- Versions-Tags für stabile Releases verwenden