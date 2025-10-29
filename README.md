# 🎵 Colab-Sound: AI-Powered Hook Generator

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-username/colab-sound)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

> Transformiere Text in professionelle Audio-Hooks mit KI-gestützter Sprachsynthese für deine Musikproduktion.

## ✨ Features

- 🎯 **KI-gestützte Sprachsynthese** mit ElevenLabs API
- 🎵 **Mehrere Hooks gleichzeitig** aus Text-Dateien generieren
- 🎧 **Live-Demo** des Endprodukts vor der Generierung
- 🔄 **Git-basierte Versionskontrolle** für modulare Updates
- 🌐 **Google Colab Integration** für einfache Nutzung
- 📦 **Automatische ZIP-Generierung** der Audio-Dateien
- 🎨 **Moderne Web-Interface** mit Gradio

## 🚀 Schnellstart

### Option 1: Colab (Empfohlen)

1. **Öffne das Colab-Notebook:**
   ```bash
   # Lade die neueste Version aus Git
   ```

2. **Konfiguriere Secrets in Colab:**
   - Gehe zu: `Runtime` → `Secrets`
   - Füge hinzu:
     - `API_KEY`: Dein ElevenLabs API-Key
     - `VOICE_ID`: Voice-ID (z.B. für ACID MONK Style)
     - `TRENNER`: Text-Trennzeichen (z.B. `---`)

3. **Führe die Zellen aus:**
   - Zelle 1: Setup und Demo
   - Zelle 2: Web-Interface für Datei-Upload

### Option 2: Lokale Installation

1. **Repository klonen:**
   ```bash
   git clone https://github.com/your-username/colab-sound.git
   cd colab-sound
   ```

2. **Umgebung einrichten:**
   ```bash
   # .env.example nach .env kopieren und anpassen
   cp .env.example .env

   # .env mit deinen API-Keys füllen
   nano .env  # oder deinen bevorzugten Editor
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lokalen Server starten:**
   ```bash
   python -c "from src.demo import show_hook_demo; show_hook_demo()"
   ```

### Option 2: Lokale Installation

```bash
# Repository klonen
git clone https://github.com/your-username/colab-sound.git
cd colab-sound

# Abhängigkeiten installieren
pip install -r requirements.txt

# Umgebungsvariablen setzen
export ELEVENLABS_API_KEY="your-api-key"
export VOICE_ID="your-voice-id"
export TEXT_SEPARATOR="---"
```

## 📖 Verwendung

### Text-Datei Format

Erstelle eine `.txt`-Datei mit deinen Hook-Texten:

```
Hook 1: Dieser Text wird zu Audio konvertiert
---
Hook 2: Jeder Abschnitt wird ein separater Hook
---
Hook 3: So viele wie du möchtest!
```

### Web-Interface

1. **Datei hochladen**: Wähle deine Text-Datei aus
2. **Generieren**: Klicke auf "🚀 Hooks generieren"
3. **Herunterladen**: Speichere die ZIP-Datei mit allen Audio-Hooks

### Programmatische Nutzung

```python
from src.generator import generate_hooks

# Hooks generieren
zip_path, message = generate_hooks(
    file_path="hooks.txt",
    api_key="your-api-key",
    voice_id="your-voice-id",
    separator="---"
)

print(message)  # Status-Nachricht
# zip_path enthält Pfad zur ZIP-Datei
```

## 🏗️ Architektur

```
colab-sound/
├── src/
│   ├── setup.py          # Colab-Setup & Konfiguration
│   ├── generator.py      # Hook-Generierung (ElevenLabs)
│   ├── demo.py          # Demo-Funktionalität
│   └── git_loader.py    # Git-basierte Modul-Verwaltung
├── notebooks/
│   ├── zelle1_git_version.py    # Colab Zelle 1 (Git-Version)
│   └── zelle2_git_version.py    # Colab Zelle 2 (Git-Version)
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔧 API-Referenz

### Git-Loader

```python
from src.git_loader import init_git_loader, load_from_git

# Repository initialisieren
init_git_loader('your-username/colab-sound')

# Module laden
load_from_git('setup')           # Setup-Modul
load_from_git('generator')       # Generator-Modul
load_from_git('demo', 'v1.0.0')  # Spezifische Version
```

### Hook-Generator

```python
from src.generator import HookGenerator

generator = HookGenerator(api_key, voice_id, separator)
zip_path, message = generator.generate_from_file(text_file_path)
```

## 🎵 Demo

Die Demo zeigt dir, wie deine generierten Hooks klingen werden:

```python
from src.demo import show_hook_demo
show_hook_demo()  # Lädt und spielt Beispiel-Audio ab
```

## 🔐 Sicherheit

- API-Keys werden **nie** im Code gespeichert
- Verwende Colab Secrets oder Umgebungsvariablen
- Keine sensiblen Daten werden geloggt
- HTTPS-Verbindungen für alle API-Calls

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

### Entwicklungsrichtlinien

- Verwende Type Hints für bessere Code-Qualität
- Schreibe aussagekräftige Commit-Messages
- Teste Änderungen vor dem Commit
- Halte die modulare Struktur bei

## 📋 Changelog

### [1.0.0] - 2025-10-29
- 🎉 **Erstveröffentlichung** mit modularer Architektur
- ✨ Git-basierte Versionskontrolle implementiert
- 🎵 ElevenLabs Integration für professionelle Sprachsynthese
- 🎧 Live-Demo des Endprodukts
- 🌐 Google Colab Integration
- 📦 Automatische ZIP-Generierung
- 🎨 Moderne Gradio Web-Interface

### Geplante Features
- 🔄 Batch-Verarbeitung für große Text-Dateien
- 🎛️ Erweiterte Voice-Settings (Stabilität, Style, etc.)
- 📊 Generierungs-Statistiken und Logs
- 🎼 Integration mit DAWs (Digital Audio Workstations)
- 🌍 Mehrsprachige Unterstützung

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## 🙏 Danksagungen

- [ElevenLabs](https://elevenlabs.io/) für die professionelle Sprachsynthese API
- [Gradio](https://gradio.app/) für das benutzerfreundliche Web-Interface
- [Google Colab](https://colab.google/) für die kostenlose Cloud-Computing-Umgebung

## 📞 Support

Bei Fragen oder Problemen:

1. **GitHub Issues**: [Öffne ein Issue](https://github.com/your-username/colab-sound/issues)
2. **ElevenLabs Docs**: [API-Dokumentation](https://docs.elevenlabs.io/)
3. **Gradio Docs**: [Interface-Dokumentation](https://gradio.app/docs/)

---

**Made with ❤️ for Music Producers & AI Enthusiasts**

*Transform your ideas into sound with the power of AI!*