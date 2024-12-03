import pytest

from gpytranslate import Translator


"""Tests for the async language detection functionality."""

@pytest.mark.asyncio
async def test_detect() -> None:
    """Test that language detection works correctly for Italian text."""
    translator = Translator()
    language = await translator.detect(text="Ciao Mondo.")
    assert isinstance(language, str)

    assert language == "it", "Translations are not equal."
