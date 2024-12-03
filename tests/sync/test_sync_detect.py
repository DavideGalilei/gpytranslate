from gpytranslate import SyncTranslator


def test_sync_detect() -> None:
    translator = SyncTranslator()
    language = translator.detect(text="Ciao Mondo.")
    assert isinstance(language, str)

    assert language == "it", "Translations are not equal."
