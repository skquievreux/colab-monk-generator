"""
Tests für generator.py Modul
"""

import pytest
import tempfile
from pathlib import Path
from src.generator import HookGenerator


class TestHookGenerator:
    """Tests für die HookGenerator Klasse"""

    @pytest.fixture
    def generator(self):
        """Fixture für HookGenerator-Instanz"""
        return HookGenerator(
            api_key="test_api_key",
            voice_id="test_voice_id",
            separator="---"
        )

    @pytest.fixture
    def valid_text_file(self):
        """Fixture für eine gültige Text-Datei"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Hook 1 Text\n---\nHook 2 Text\n---\nHook 3 Text")
            return f.name

    @pytest.fixture
    def empty_text_file(self):
        """Fixture für eine leere Text-Datei"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            return f.name

    @pytest.fixture
    def large_text_file(self):
        """Fixture für eine zu große Text-Datei (>1MB)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            # Schreibe > 1MB Text
            large_text = "A" * (1024 * 1024 + 1)
            f.write(large_text)
            return f.name

    def test_parse_text_file_valid(self, generator, valid_text_file):
        """Test: Parsen einer gültigen Text-Datei"""
        parts = generator.parse_text_file(valid_text_file)

        assert len(parts) == 3
        assert parts[0] == "Hook 1 Text"
        assert parts[1] == "Hook 2 Text"
        assert parts[2] == "Hook 3 Text"

    def test_parse_text_file_empty(self, generator, empty_text_file):
        """Test: Parsen einer leeren Text-Datei sollte ValueError werfen"""
        with pytest.raises(ValueError, match="Text-Datei ist leer"):
            generator.parse_text_file(empty_text_file)

    def test_parse_text_file_not_found(self, generator):
        """Test: Parsen einer nicht existierenden Datei sollte FileNotFoundError werfen"""
        with pytest.raises(FileNotFoundError):
            generator.parse_text_file("/nicht/existierender/pfad.txt")

    def test_parse_text_file_too_large(self, generator, large_text_file):
        """Test: Parsen einer zu großen Datei sollte ValueError werfen"""
        with pytest.raises(ValueError, match="Text-Datei zu groß"):
            generator.parse_text_file(large_text_file)

    def test_validate_text_file_valid(self, generator, valid_text_file):
        """Test: Validierung einer gültigen Datei sollte ohne Fehler durchlaufen"""
        # Sollte keine Exception werfen
        generator.validate_text_file(valid_text_file)

    def test_validate_text_file_not_exist(self, generator):
        """Test: Validierung einer nicht existierenden Datei"""
        with pytest.raises(FileNotFoundError):
            generator.validate_text_file("/nicht/existierender/pfad.txt")

    def test_validate_text_file_empty(self, generator, empty_text_file):
        """Test: Validierung einer leeren Datei"""
        with pytest.raises(ValueError, match="Text-Datei ist leer"):
            generator.validate_text_file(empty_text_file)

    def test_hook_generator_initialization(self):
        """Test: Initialisierung des HookGenerators"""
        gen = HookGenerator(
            api_key="test_key",
            voice_id="test_voice",
            separator="||"
        )

        assert gen.api_key == "test_key"
        assert gen.voice_id == "test_voice"
        assert gen.separator == "||"
        assert "test_voice" in gen.url

    def test_parse_with_custom_separator(self):
        """Test: Parsen mit benutzerdefiniertem Trennzeichen"""
        gen = HookGenerator("key", "voice", separator="###")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Text 1###Text 2###Text 3")
            file_path = f.name

        parts = gen.parse_text_file(file_path)

        assert len(parts) == 3
        assert parts[0] == "Text 1"
        assert parts[1] == "Text 2"
        assert parts[2] == "Text 3"

    def test_parse_text_file_with_long_hook(self, generator):
        """Test: Parsen mit zu langem Hook-Text sollte ValueError werfen"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            # Erstelle Hook mit > 5000 Zeichen
            long_text = "A" * 5001
            f.write(long_text)
            file_path = f.name

        with pytest.raises(ValueError, match="Hook .* ist zu lang"):
            generator.parse_text_file(file_path)


# Integration Tests (werden übersprungen wenn API-Key fehlt)
class TestHookGeneratorIntegration:
    """Integration-Tests mit echter API (optional)"""

    @pytest.mark.skipif(
        not pytest.config.getoption("--run-integration", default=False),
        reason="Integration tests nur mit --run-integration ausführen"
    )
    def test_generate_audio_hook_real_api(self):
        """Test: Generierung mit echter API (nur wenn API-Key vorhanden)"""
        # Dieser Test würde einen echten API-Call machen
        # Sollte nur in CI/CD mit echtem API-Key laufen
        pass
