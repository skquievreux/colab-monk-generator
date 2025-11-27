"""
Gemeinsame Test-Fixtures und Konfiguration für pytest
"""

import pytest
import tempfile
import os
from pathlib import Path


def pytest_addoption(parser):
    """Füge benutzerdefinierte CLI-Optionen hinzu"""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Führe Integration-Tests aus (benötigt echte API-Keys)"
    )


@pytest.fixture(scope="session")
def temp_dir():
    """Erstelle ein temporäres Verzeichnis für Tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_file(temp_dir):
    """Erstelle eine Beispiel-Text-Datei für Tests"""
    file_path = temp_dir / "sample.txt"
    content = "Sample Hook 1\n---\nSample Hook 2\n---\nSample Hook 3"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    yield file_path

    # Cleanup
    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def mock_env_vars():
    """Mock Umgebungsvariablen für Tests"""
    original_env = os.environ.copy()

    # Setze Test-Umgebungsvariablen
    os.environ['API_KEY'] = 'test_api_key'
    os.environ['VOICE_ID'] = 'test_voice_id'
    os.environ['TRENNER'] = '---'

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_api_response():
    """Mock API-Response für Tests"""
    class MockResponse:
        def __init__(self, status_code=200, content=b"fake audio data"):
            self.status_code = status_code
            self.content = content
            self.text = "Mock response"

        def iter_content(self, chunk_size):
            """Simuliere streaming content"""
            yield self.content

        def raise_for_status(self):
            """Simuliere raise_for_status"""
            if self.status_code != 200:
                raise Exception(f"HTTP {self.status_code}")

    return MockResponse
