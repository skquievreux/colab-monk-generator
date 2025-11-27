"""
Logging-Modul für Colab-Sound Projekt
Zentrale Konfiguration für strukturiertes Logging
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Logging-Level-Mapping für einfache Konfiguration
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class ColoredFormatter(logging.Formatter):
    """Formatter mit Farben für bessere Lesbarkeit in der Console"""

    # ANSI-Farbcodes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Grün
        'WARNING': '\033[33m',    # Gelb
        'ERROR': '\033[31m',      # Rot
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    # Emoji für verschiedene Log-Level
    EMOJIS = {
        'DEBUG': '🔍',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨'
    }

    def format(self, record):
        # Farbe und Emoji basierend auf Level
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        emoji = self.EMOJIS.get(record.levelname, '')
        reset = self.COLORS['RESET']

        # Original-Format mit Farbe
        log_fmt = f"{color}{emoji} {record.levelname}{reset} - {record.getMessage()}"

        # Bei Exceptions: Stack-Trace hinzufügen
        if record.exc_info:
            log_fmt += f"\n{self.formatException(record.exc_info)}"

        return log_fmt

def setup_logger(
    name: str = "colab-sound",
    level: str = "INFO",
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Richtet einen Logger mit konfigurierbarem Output ein

    Args:
        name: Name des Loggers
        level: Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional: Pfad zur Log-Datei
        console: Soll auf Console geloggt werden?

    Returns:
        logging.Logger: Konfigurierter Logger
    """
    # Logger erstellen
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))

    # Verhindere doppelte Handler
    if logger.handlers:
        logger.handlers.clear()

    # Console-Handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)

    # Datei-Handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # In Datei alles loggen

        # Detaillierteres Format für Datei
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

# Globaler Logger für das gesamte Projekt
_default_logger: Optional[logging.Logger] = None

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Holt den Logger für ein Modul

    Args:
        name: Optional: Name des Loggers (default: colab-sound)

    Returns:
        logging.Logger: Logger-Instanz
    """
    global _default_logger

    if _default_logger is None:
        # Ersten Logger initialisieren
        _default_logger = setup_logger()

    if name:
        return logging.getLogger(f"colab-sound.{name}")

    return _default_logger

def set_log_level(level: str) -> None:
    """
    Setzt das Log-Level für alle Logger

    Args:
        level: Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger = get_logger()
    logger.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))

    for handler in logger.handlers:
        handler.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))

# Logger beim Import initialisieren
_default_logger = setup_logger()
