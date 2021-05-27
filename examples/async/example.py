import asyncio

from gpytranslate import Translator


async def main():
    t = Translator()
    # Note: you can use proxies by passing proxies parameter to Translator
    translation = await t.translate("Ciao come stai? Io bene ahah.", targetlang="en")
    # By default, sourcelang is "auto"
    language = await t.detect("Ciao come stai? Io bene ahah.")
    # Returns language code "it"
    print(f"Translation: {translation.text}\nDetected language: {language}")


if __name__ == "__main__":
    asyncio.run(main())
