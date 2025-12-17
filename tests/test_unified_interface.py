"""
Test für das vereinheitlichte Interface mit Playwright
Prüft ob beide Tabs korrekt angezeigt werden und funktionieren
"""

import pytest
from playwright.sync_api import Page, expect, Browser, BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Browser-Konfiguration für Colab-URLs"""
    return {
        **browser_context_args,
        "ignore_https_errors": True,  # Für Colab-URLs
        "viewport": {"width": 1280, "height": 720}
    }


def test_unified_interface_tabs_visible(page: Page):
    """Test dass beide Tabs (Demo und Hook Generator) sichtbar sind"""
    # Navigiere zur Colab-URL
    page.goto("https://7862-m-s-1rmzud4u9lnor-a.asia-east1-0.prod.colab.dev/")

    # Warte auf das Interface
    page.wait_for_load_state("networkidle")

    # Prüfe dass beide Tabs vorhanden sind
    demo_tab = page.locator("text=🎧 Demo")
    generator_tab = page.locator("text=🚀 Hook Generator")

    expect(demo_tab).to_be_visible()
    expect(generator_tab).to_be_visible()

    # Screenshot für Dokumentation
    page.screenshot(path="tests/screenshot_tabs_visible.png")


def test_demo_tab_functionality(page: Page):
    """Test dass der Demo-Tab funktioniert"""
    page.goto("https://7862-m-s-1rmzud4u9lnor-a.asia-east1-0.prod.colab.dev/")

    # Klicke auf Demo-Tab
    page.locator("text=🎧 Demo").click()

    # Prüfe dass Demo-Button vorhanden ist
    demo_button = page.locator("text=🎵 Demo laden")
    expect(demo_button).to_be_visible()

    # Screenshot vor dem Klick
    page.screenshot(path="tests/screenshot_demo_before.png")

    # Klicke auf Demo laden (aber ohne tatsächliches Laden)
    # demo_button.click()

    # Prüfe dass Audio-Player und Status-Textbox vorhanden sind
    audio_player = page.locator("[data-testid='audio-player']")
    status_box = page.locator("label:has-text('Status')")

    # Diese Elemente sollten vorhanden sein (auch wenn noch nicht gefüllt)
    expect(audio_player).to_be_visible()
    expect(status_box).to_be_visible()

    # Screenshot nach dem Setup
    page.screenshot(path="tests/screenshot_demo_after.png")


def test_generator_tab_functionality(page: Page):
    """Test dass der Hook Generator-Tab funktioniert"""
    page.goto("https://7862-m-s-1rmzud4u9lnor-a.asia-east1-0.prod.colab.dev/")

    # Klicke auf Generator-Tab
    page.locator("text=🚀 Hook Generator").click()

    # Prüfe dass alle erforderlichen Elemente vorhanden sind
    file_input = page.locator("label:has-text('Text-Datei auswählen')")
    generate_button = page.locator("text=🚀 Hooks generieren")
    status_output = page.locator("label:has-text('📊 Status')")
    download_output = page.locator("label:has-text('📦 Generierte Hooks herunterladen')")

    expect(file_input).to_be_visible()
    expect(generate_button).to_be_visible()
    expect(status_output).to_be_visible()
    expect(download_output).to_be_visible()

    # Screenshot des Generator-Tabs
    page.screenshot(path="tests/screenshot_generator_tab.png")


def test_interface_title_and_description(page: Page):
    """Test dass Titel und Beschreibung korrekt angezeigt werden"""
    page.goto("https://7862-m-s-1rmzud4u9lnor-a.asia-east1-0.prod.colab.dev/")

    # Prüfe Titel
    title = page.locator("text=🎵 ACID MONK - Hook Generator")
    expect(title).to_be_visible()

    # Prüfe Beschreibung
    description = page.locator("text=einheitlicher Demo & Generator Oberfläche")
    expect(description).to_be_visible()

    # Screenshot der Kopfzeile
    page.screenshot(path="tests/screenshot_header.png")


if __name__ == "__main__":
    # Für manuelle Ausführung
    print("🎯 Starte Interface-Tests...")
    print("📸 Screenshots werden in tests/ gespeichert")
    print("✅ Tests prüfen Tab-Sichtbarkeit und grundlegende Funktionalität")