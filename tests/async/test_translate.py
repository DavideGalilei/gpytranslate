from typing import Any, Dict, List

import pytest

from gpytranslate import TranslatedObject, Translator


@pytest.mark.asyncio
async def test_translate_auto():
    translator = Translator()
    translation: TranslatedObject = await translator.translate("Ciao Mondo.", targetlang="en")
    assert translation.text == "Hello World.", "Translations are not equal."


@pytest.mark.asyncio
async def test_translate_source():
    translator = Translator()
    translation: TranslatedObject = await translator.translate("Ciao.", sourcelang="it", targetlang="en")

    assert translation.text in ("Hello.", "HI."), "Translations are not equal."


@pytest.mark.asyncio
async def test_translate_list():
    translator = Translator()
    translations: List[TranslatedObject] = await translator.translate(["Ciao Mondo.", "Come stai?"], targetlang="en")

    assert [translation.text for translation in translations] == [
        "Hello World.",
        "How are you?",
    ], "Translations are not equal."


@pytest.mark.asyncio
async def test_translate_dict():
    translator = Translator()
    translations: Dict[Any, TranslatedObject] = await translator.translate(
        {1: "Ciao Mondo.", 2: "Come stai?"}, targetlang="en"
    )

    assert {k: v.text for k, v in translations.items()} == {
        1: "Hello World.",
        2: "How are you?",
    }, "Translations are not equal."
