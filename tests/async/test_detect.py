import pytest


from gpytranslate import Translator


@pytest.mark.asyncio
async def test_detect():
    translator = Translator()
    language: str = await translator.detect(text="Ciao Mondo.")

    assert language == "it", "Translations are not equal."
