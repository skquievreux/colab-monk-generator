"""
Tests für logger.py Modul
"""

import pytest
import logging
from src.logger import setup_logger, get_logger, set_log_level


class TestLogger:
    """Tests für Logging-Funktionalität"""

    def test_setup_logger_default(self):
        """Test: Logger mit Standard-Konfiguration"""
        logger = setup_logger(name="test_logger")

        assert logger is not None
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO

    def test_setup_logger_custom_level(self):
        """Test: Logger mit benutzerdefiniertem Level"""
        logger = setup_logger(name="test_debug", level="DEBUG")

        assert logger.level == logging.DEBUG

    def test_setup_logger_invalid_level(self):
        """Test: Logger mit ungültigem Level sollte INFO verwenden"""
        logger = setup_logger(name="test_invalid", level="INVALID")

        assert logger.level == logging.INFO

    def test_get_logger(self):
        """Test: get_logger Funktion"""
        logger = get_logger("test_module")

        assert logger is not None
        assert "colab-sound" in logger.name

    def test_get_logger_default(self):
        """Test: get_logger ohne Name"""
        logger = get_logger()

        assert logger is not None
        assert logger.name == "colab-sound"

    def test_set_log_level(self):
        """Test: Log-Level ändern"""
        logger = get_logger()
        original_level = logger.level

        set_log_level("ERROR")
        assert logger.level == logging.ERROR

        # Zurücksetzen
        set_log_level("INFO")
        assert logger.level == logging.INFO

    def test_logger_handlers(self):
        """Test: Logger hat mindestens einen Handler"""
        logger = get_logger()

        assert len(logger.handlers) > 0

    def test_logger_console_output(self, caplog):
        """Test: Logger schreibt auf Console"""
        logger = get_logger("test_console")

        with caplog.at_level(logging.INFO):
            logger.info("Test-Nachricht")

        assert "Test-Nachricht" in caplog.text
