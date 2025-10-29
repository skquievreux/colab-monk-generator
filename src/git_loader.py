"""
Git-Loader für Colab-Sound Projekt
Lädt Code-Module aus einem Git-Repository für Versionskontrolle
"""

import requests
import os
from typing import Optional

class GitLoader:
    """Lädt und verwaltet Code-Module aus einem Git-Repository"""

    def __init__(self, repo_url: str, default_branch: str = 'main'):
        """
        Initialisiert den Git-Loader

        Args:
            repo_url: GitHub Repository URL (z.B. 'user/repo-name')
            default_branch: Standard-Branch für Versionen
        """
        self.repo_url = repo_url
        self.default_branch = default_branch
        self.base_url = f'https://raw.githubusercontent.com/{repo_url}'

    def load_module(self, module_name: str, version: Optional[str] = None,
                   namespace: Optional[dict] = None) -> bool:
        """
        Lädt ein Modul aus dem Git-Repository

        Args:
            module_name: Name des Moduls (ohne .py)
            version: Branch, Tag oder Commit-Hash (default: main)
            namespace: Namespace zum Ausführen des Codes (default: globals())

        Returns:
            bool: True bei Erfolg, False bei Fehler
        """
        if version is None:
            version = self.default_branch

        if namespace is None:
            namespace = globals()

        url = f'{self.base_url}/{version}/src/{module_name}.py'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Führe den Code im angegebenen Namespace aus
            exec(response.text, namespace)

            print(f"✅ Modul '{module_name}' aus {version} erfolgreich geladen")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Netzwerk-Fehler beim Laden von {module_name}: {e}")
            return False
        except Exception as e:
            print(f"❌ Fehler beim Ausführen von {module_name}: {e}")
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
    init_git_loader('user/colab-sound')

    # Einzelne Module laden
    load_from_git('setup')
    load_from_git('generator', 'v1.0.0')
    load_from_git('demo', 'feature/enhanced-demo')

    # Mehrere Module laden
    modules = ['setup', 'generator', 'demo']
    results = git_loader.load_multiple_modules(modules, 'main')
    print("Lade-Status:", results)