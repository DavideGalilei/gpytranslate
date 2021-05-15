import unittest
from typing import List, Dict, Any

from gpytranslate import Translator, TranslatedObject


class Test(unittest.IsolatedAsyncioTestCase):
    async def test_translate_auto(self):
        translator = Translator()
        translation: TranslatedObject = await translator.translate(
            "Ciao Mondo.", targetlang="en"
        )
        self.assertEqual(
            translation.text,
            "Hello World.",
            "Translations are not equal.",
        )

    async def test_translate_source(self):
        translator = Translator()
        translation: TranslatedObject = await translator.translate(
            "Ciao.", sourcelang="it", targetlang="en"
        )

        self.assertEqual(
            translation.text,
            "Hello.",
            "Translations are not equal.",
        )

    async def test_translate_list(self):
        translator = Translator()
        translations: List[TranslatedObject] = await translator.translate(
            ["Ciao Mondo.", "Come stai?"], targetlang="en"
        )

        self.assertEqual(
            [translation.text for translation in translations],
            ["Hello World.", "How are you?"],
            "Translations are not equal.",
        )

    async def test_translate_dict(self):
        translator = Translator()
        translations: Dict[Any, TranslatedObject] = await translator.translate(
            {1: "Ciao Mondo.", 2: "Come stai?"}, targetlang="en"
        )

        self.assertEqual(
            {k: v.text for k, v in translations.items()},
            {1: "Hello World.", 2: "How are you?"},
            "Translations are not equal.",
        )
