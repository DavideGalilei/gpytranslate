from typing import Any, Dict, List

import pytest

from gpytranslate import TranslatedObject, Translator


@pytest.mark.asyncio
async def test_translate_auto() -> None:
    """Test automatic language detection and translation from Italian to English."""
    translator = Translator()
    translation: TranslatedObject = await translator.translate("Ciao Mondo.", targetlang="en")
    assert translation.text == "Hello World.", "Translations are not equal."


@pytest.mark.asyncio
async def test_translate_source() -> None:
    """Test translation with explicitly specified source language."""
    translator = Translator()
    translation: TranslatedObject = await translator.translate("Ciao.", sourcelang="it", targetlang="en")

    assert translation.text in ("Hello.", "HI."), "Translations are not equal."


@pytest.mark.asyncio
async def test_translate_list() -> None:
    """Test translation of a list of strings."""
    translator = Translator()
    translations: List[TranslatedObject] = await translator.translate(["Ciao Mondo.", "Come stai?"], targetlang="en")

    assert [translation.text for translation in translations] == [
        "Hello World.",
        "How are you?",
    ], "Translations are not equal."


@pytest.mark.asyncio
async def test_translate_dict() -> None:
    """Test translation of dictionary values."""
    translator = Translator()
    translations: Dict[Any, TranslatedObject] = await translator.translate(
        {1: "Ciao Mondo.", 2: "Come stai?"}, targetlang="en"
    )

    assert {k: v.text for k, v in translations.items()} == {
        1: "Hello World.",
        2: "How are you?",
    }, "Translations are not equal."
