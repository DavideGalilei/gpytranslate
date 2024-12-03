from gpytranslate import SyncTranslator


def test_sync_detect():
    translator = SyncTranslator()
    language: str = translator.detect(text="Ciao Mondo.")

    assert language == "it", "Translations are not equal."
