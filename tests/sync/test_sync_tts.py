import io
import os.path

from gpytranslate import SyncTranslator


def test_sync_tts():
    translator = SyncTranslator()
    filename = "test.mp3"

    with open(filename, "wb") as file:
        translator.tts("Hello world!", file=file, targetlang="en")

    assert os.path.isfile(filename), "File doesn't exist"
    os.remove(filename)


def test_sync_tts_bytesio():
    translator = SyncTranslator()
    file = io.BytesIO()

    translator.tts("Hello world!", file=file, targetlang="en")
