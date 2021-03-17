from gpytranslate import Translator
import asyncio


async def main():
    tr = Translator()
    translation = await tr("🅱️🅱️ come va?", targetlang='en')
    language = await tr.detect("Ciao come stai? Io bene ahah.")
    print(f"Translation: {translation.text}\nDetected language: {language}")


if __name__ == "__main__":
    asyncio.run(main())
