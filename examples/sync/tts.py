from gpytranslate import SyncTranslator

translator = SyncTranslator()

with open("test.mp3", "wb") as file:
    translator.tts("Hello world!", file=file, targetlang="en")
