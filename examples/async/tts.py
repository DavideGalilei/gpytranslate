import asyncio

import aiofiles

from gpytranslate import Translator

"""Example showing how to use text-to-speech functionality."""


async def main() -> None:
    """Demonstrate text-to-speech generation."""
    translator = Translator()

    async with aiofiles.open("test.mp3", "wb") as file:
        await translator.tts("Hello world!", file=file, targetlang="en")


if __name__ == "__main__":
    asyncio.run(main())
