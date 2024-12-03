import asyncio

from gpytranslate import Translator


"""Example showing basic translation and language detection."""

async def main() -> None:
    """Demonstrate translation from Italian to English and language detection."""
    t = Translator()
    # Note: you can use proxies by passing proxies parameter to Translator
    translation = await t.translate("Ciao come stai? Io bene ahah.", targetlang="en")
    # By default, sourcelang is "auto"
    language = await t.detect(translation.text)
    # Returns language code "it"
    print(f"Translation: {translation.text}\nDetected language: {language}")


if __name__ == "__main__":
    asyncio.run(main())
