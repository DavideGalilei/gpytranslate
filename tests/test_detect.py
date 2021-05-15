import unittest

from gpytranslate import Translator


class Test(unittest.IsolatedAsyncioTestCase):
    async def test_detect(self):
        translator = Translator()
        language: str = await translator.detect(
            text="Ciao Mondo."
        )

        self.assertEqual(
            language,
            "it",
            "Translations are not equal.",
        )
