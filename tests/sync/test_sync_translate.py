from typing import Any, Dict, List

from gpytranslate import SyncTranslator, TranslatedObject


def test_sync_translate_auto() -> None:
    """Test automatic language detection and translation from Italian to English."""
    translator = SyncTranslator()
    translation: TranslatedObject = translator.translate("Ciao Mondo.", targetlang="en")
    assert translation.text == "Hello World.", "Translations are not equal."


def test_sync_translate_source() -> None:
    """Test translation with explicitly specified source language."""
    translator = SyncTranslator()
    translation: TranslatedObject = translator.translate("Ciao.", sourcelang="it", targetlang="en")

    assert translation.text in ("Hello.", "HI."), "Translations are not equal."


def test_sync_translate_list() -> None:
    """Test translation of a list of strings."""
    translator = SyncTranslator()
    translations: List[TranslatedObject] = translator.translate(["Ciao Mondo.", "Come stai?"], targetlang="en")

    assert [translation.text for translation in translations] == [
        "Hello World.",
        "How are you?",
    ], "Translations are not equal."


def test_sync_translate_dict() -> None:
    """Test translation of dictionary values."""
    translator = SyncTranslator()
    translations: Dict[Any, TranslatedObject] = translator.translate(
        {1: "Ciao Mondo.", 2: "Come stai?"}, targetlang="en"
    )

    assert {k: v.text for k, v in translations.items()} == {
        1: "Hello World.",
        2: "How are you?",
    }, "Translations are not equal."


if __name__ == "__main__":
    test_sync_translate_auto()
    test_sync_translate_source()
    test_sync_translate_list()
    test_sync_translate_dict()
