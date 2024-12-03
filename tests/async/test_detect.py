import pytest

from gpytranslate import Translator


@pytest.mark.asyncio
async def test_detect() -> None:
    translator = Translator()
    language = await translator.detect(text="Ciao Mondo.")
    assert isinstance(language, str)

    assert language == "it", "Translations are not equal."
