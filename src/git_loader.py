"""
Git-Loader für Colab-Sound Projekt
Lädt Code-Module aus einem Git-Repository für Versionskontrolle

SICHERHEITSHINWEIS:
Dieses Modul lädt und führt Code aus einem Git-Repository aus.
Stelle sicher, dass du dem Repository-Inhalt vertraust!
"""

import requests
import os
import hashlib
from typing import Optional, Dict
from src.logger import get_logger

logger = get_logger("git_loader")

class GitLoader:
    """Lädt und verwaltet Code-Module aus einem Git-Repository"""

    # Whitelist von erlaubten Modulen (Sicherheit)
    ALLOWED_MODULES = {'setup', 'generator', 'demo', 'interface', 'logger', 'git_loader'}

    # Optionale SHA256-Hashes für Code-Validierung
    # Format: {module_name: {version: hash}}
    MODULE_HASHES: Dict[str, Dict[str, str]] = {}

    def __init__(self, repo_url: str, default_branch: str = 'main', verify_hashes: bool = False):
        """
        Initialisiert den Git-Loader

        Args:
            repo_url: GitHub Repository URL (z.B. 'user/repo-name')
            default_branch: Standard-Branch für Versionen
            verify_hashes: Ob Code-Hashes verifiziert werden sollen
        """
        self.repo_url = repo_url
        self.default_branch = default_branch
        self.base_url = f'https://raw.githubusercontent.com/{repo_url}'
        self.verify_hashes = verify_hashes

        logger.info(f"GitLoader initialisiert für Repository: {repo_url}")

    def validate_module_name(self, module_name: str) -> bool:
        """
        Validiert den Modulnamen gegen die Whitelist

        Args:
            module_name: Name des Moduls

        Returns:
            bool: True wenn erlaubt, False sonst
        """
        if module_name not in self.ALLOWED_MODULES:
            logger.error(f"Modul '{module_name}' nicht in Whitelist. Erlaubt: {self.ALLOWED_MODULES}")
            return False
        return True

    def calculate_hash(self, code: str) -> str:
        """
        Berechnet SHA256-Hash des Codes

        Args:
            code: Python-Code als String

        Returns:
            str: SHA256-Hash
        """
        return hashlib.sha256(code.encode('utf-8')).hexdigest()

    def verify_code_hash(self, module_name: str, version: str, code: str) -> bool:
        """
        Verifiziert den Code gegen gespeicherte Hashes

        Args:
            module_name: Name des Moduls
            version: Version des Moduls
            code: Code zum Verifizieren

        Returns:
            bool: True wenn Hash übereinstimmt oder keine Verifikation nötig
        """
        if not self.verify_hashes:
            return True

        if module_name not in self.MODULE_HASHES:
            logger.warning(f"Keine Hashes für Modul '{module_name}' gespeichert")
            return True

        if version not in self.MODULE_HASHES[module_name]:
            logger.warning(f"Kein Hash für Version '{version}' von Modul '{module_name}'")
            return True

        expected_hash = self.MODULE_HASHES[module_name][version]
        actual_hash = self.calculate_hash(code)

        if expected_hash != actual_hash:
            logger.error(f"Hash-Mismatch für {module_name}@{version}!")
            logger.error(f"Erwartet: {expected_hash}")
            logger.error(f"Erhalten: {actual_hash}")
            return False

        logger.info(f"Hash für {module_name}@{version} verifiziert ✓")
        return True

    def load_module(self, module_name: str, version: Optional[str] = None,
                   namespace: Optional[dict] = None, force: bool = False) -> bool:
        """
        Lädt ein Modul aus dem Git-Repository

        SICHERHEITSWARNUNG:
        Diese Funktion verwendet exec() zum Ausführen von Remote-Code.
        Stelle sicher, dass du dem Repository vertraust!

        Args:
            module_name: Name des Moduls (ohne .py)
            version: Branch, Tag oder Commit-Hash (default: main)
            namespace: Namespace zum Ausführen des Codes (default: globals())
            force: Umgehe Whitelist-Check (nur für Entwicklung!)

        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        # Validiere Modulname
        if not force and not self.validate_module_name(module_name):
            logger.error(f"Modul '{module_name}' ist nicht erlaubt")
            return False

        if version is None:
            version = self.default_branch

        if namespace is None:
            namespace = globals()

        url = f'{self.base_url}/{version}/src/{module_name}.py'

        try:
            logger.info(f"Lade Modul '{module_name}' von {url}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            code = response.text

            # Hash-Verifikation (optional)
            if not self.verify_code_hash(module_name, version, code):
                logger.error("Hash-Verifikation fehlgeschlagen! Abbruch.")
                return False

            # SICHERHEITSWARNUNG vor exec()
            logger.warning(f"⚠️  Führe Remote-Code aus: {module_name}@{version}")
            logger.warning("⚠️  Stelle sicher, dass du diesem Repository vertraust!")

            # Führe den Code im angegebenen Namespace aus
            # HINWEIS: exec() ist inhärent unsicher!
            exec(code, namespace)

            logger.info(f"Modul '{module_name}' aus {version} erfolgreich geladen")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerk-Fehler beim Laden von {module_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Fehler beim Ausführen von {module_name}: {e}")
            return False

    def load_multiple_modules(self, modules: list, version: Optional[str] = None) -> dict:
        """
        Lädt mehrere Module gleichzeitig

        Args:
            modules: Liste der Modulnamen
            version: Version für alle Module

        Returns:
            dict: Status für jedes Modul
        """
        results = {}
        for module in modules:
            results[module] = self.load_module(module, version)
        return results

    def get_available_versions(self) -> list:
        """
        Holt verfügbare Branches/Tags (vereinfacht - nur main/master zurückgegeben)

        Returns:
            list: Liste verfügbarer Versionen
        """
        # Vereinfachte Implementierung - in der Praxis würde man die GitHub API verwenden
        return [self.default_branch, 'develop', 'v1.0.0']

# Globale Instanz für einfache Verwendung
git_loader = None

def init_git_loader(repo_url: str, default_branch: str = 'main'):
    """Initialisiert den globalen Git-Loader"""
    global git_loader
    git_loader = GitLoader(repo_url, default_branch)
    print(f"🔗 Git-Loader initialisiert für Repository: {repo_url}")

def load_from_git(module: str, version: Optional[str] = None):
    """
    Lädt ein Modul aus dem Git-Repository (vereinfachte Funktion)

    Args:
        module: Modulname
        version: Version (optional)
    """
    if git_loader is None:
        print("❌ Git-Loader nicht initialisiert. Verwende init_git_loader() zuerst.")
        return False

    return git_loader.load_module(module, version)

# Beispiel für die Verwendung:
if __name__ == "__main__":
    # Initialisierung
    init_git_loader('skquievreux/colab-monk-generator')

    # Einzelne Module laden
    load_from_git('setup')
    load_from_git('generator', 'v1.0.0')
    load_from_git('demo', 'feature/enhanced-demo')

    # Mehrere Module laden
    modules = ['setup', 'generator', 'demo']
    results = git_loader.load_multiple_modules(modules, 'main')
    print("Lade-Status:", results)