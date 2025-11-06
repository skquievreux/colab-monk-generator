"""
Zentrale Konfigurationsverwaltung für Colab-Sound Projekt
Alle Hardcoded-Werte werden hier definiert
"""

import os
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class ElevenLabsConfig:
    """Konfiguration für ElevenLabs API"""

    # Model-Einstellungen
    model_id: str = "eleven_v3"
    output_format: str = "mp3_44100_128"

    # Voice-Einstellungen (Default-Werte)
    default_stability: float = 0.0
    default_similarity_boost: float = 0.8
    default_style: float = 1.0

    # Rate Limiting
    rate_limit_delay: float = 1.5  # Sekunden zwischen API-Calls

    # Text-Limits
    max_text_length: int = 5000  # Zeichen pro Hook


@dataclass
class FileConfig:
    """Konfiguration für Dateiverwaltung"""

    # Datei-Limits
    max_file_size: int = 1024 * 1024  # 1MB

    # Output-Einstellungen
    default_zip_name: str = "ACID_MONK_HOOKS.zip"
    default_separator: str = "---"

    # Datei-Patterns
    hook_filename_pattern: str = "hook_{number:02d}.mp3"

    # Encoding
    default_encoding: str = "utf-8"


@dataclass
class DemoConfig:
    """Konfiguration für Demo-Funktionalität"""

    # Demo-URL
    demo_url: str = "https://pub-aa6154186add4631a26d1261deb9606f.r2.dev/acid-monk-obsession-arrived.mp3"

    # Cache-Einstellungen
    demo_file_name: str = "demo_hook.mp3"
    cache_demo: bool = True


@dataclass
class LoggingConfig:
    """Konfiguration für Logging"""

    # Log-Level
    default_level: str = "INFO"

    # Log-Datei (optional)
    log_file: str = None

    # Console-Logging
    console_logging: bool = True


@dataclass
class NetworkConfig:
    """Konfiguration für Netzwerk-Requests"""

    # Timeouts
    default_timeout: int = 30  # Sekunden
    download_timeout: int = 60  # Sekunden

    # Retry-Einstellungen
    max_retries: int = 3
    retry_delay: float = 2.0  # Sekunden


@dataclass
class AppConfig:
    """Haupt-Konfiguration für die Anwendung"""

    # Sub-Konfigurationen
    elevenlabs: ElevenLabsConfig = field(default_factory=ElevenLabsConfig)
    files: FileConfig = field(default_factory=FileConfig)
    demo: DemoConfig = field(default_factory=DemoConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    network: NetworkConfig = field(default_factory=NetworkConfig)

    # App-Metadaten
    app_name: str = "Colab-Sound Hook Generator"
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        """
        Konvertiert die Konfiguration in ein Dictionary

        Returns:
            Dict mit allen Konfigurationseinstellungen
        """
        return {
            'elevenlabs': self.elevenlabs.__dict__,
            'files': self.files.__dict__,
            'demo': self.demo.__dict__,
            'logging': self.logging.__dict__,
            'network': self.network.__dict__,
            'app_name': self.app_name,
            'version': self.version
        }

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """
        Erstellt Konfiguration aus Umgebungsvariablen

        Returns:
            AppConfig-Instanz
        """
        config = cls()

        # ElevenLabs-Konfiguration aus Umgebung
        if os.getenv('ELEVENLABS_MODEL_ID'):
            config.elevenlabs.model_id = os.getenv('ELEVENLABS_MODEL_ID')

        if os.getenv('RATE_LIMIT_DELAY'):
            config.elevenlabs.rate_limit_delay = float(os.getenv('RATE_LIMIT_DELAY'))

        # Datei-Konfiguration
        if os.getenv('TEXT_SEPARATOR'):
            config.files.default_separator = os.getenv('TEXT_SEPARATOR')

        if os.getenv('ZIP_NAME'):
            config.files.default_zip_name = os.getenv('ZIP_NAME')

        # Logging-Konfiguration
        if os.getenv('LOG_LEVEL'):
            config.logging.default_level = os.getenv('LOG_LEVEL')

        if os.getenv('LOG_FILE'):
            config.logging.log_file = os.getenv('LOG_FILE')

        return config


# Globale Konfigurationsinstanz
_config: AppConfig = None


def get_config() -> AppConfig:
    """
    Holt die globale Konfiguration

    Returns:
        AppConfig-Instanz
    """
    global _config

    if _config is None:
        # Versuche aus Umgebung zu laden, sonst Defaults
        _config = AppConfig.from_env()

    return _config


def reload_config() -> AppConfig:
    """
    Lädt die Konfiguration neu

    Returns:
        Neue AppConfig-Instanz
    """
    global _config
    _config = AppConfig.from_env()
    return _config


def update_config(**kwargs) -> None:
    """
    Aktualisiert spezifische Konfigurationswerte

    Args:
        **kwargs: Key-Value-Paare für Updates
    """
    config = get_config()

    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)


# Konstanten für einfachen Zugriff
class Constants:
    """Globale Konstanten"""

    # Repository-Informationen
    REPO_OWNER = "skquievreux"
    REPO_NAME = "colab-monk-generator"
    REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"

    # API-Endpoints
    ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"

    # Supported file types
    SUPPORTED_TEXT_FORMATS = ['.txt']

    # HTTP Status Codes
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_NOT_FOUND = 404
    HTTP_RATE_LIMIT = 429
    HTTP_SERVER_ERROR = 500


# Beim Import initialisieren
_config = AppConfig.from_env()
