from gpytranslate import SyncTranslator

t = SyncTranslator()
translation = t.translate("Ciao come stai? Io bene ahah.", targetlang="en")
language = t.detect(translation.text)
print(f"Translation: {translation.text}\nDetected language: {language}")
