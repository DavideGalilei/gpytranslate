from gpytranslate import SyncTranslator


"""Tests for the synchronous language detection functionality."""

def test_sync_detect() -> None:
    """Test that language detection works correctly for Italian text."""
    translator = SyncTranslator()
    language = translator.detect(text="Ciao Mondo.")
    assert isinstance(language, str)

    assert language == "it", "Translations are not equal."
