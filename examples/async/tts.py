import asyncio

import aiofiles

from gpytranslate import Translator


async def main() -> None:
    translator = Translator()

    async with aiofiles.open("test.mp3", "wb") as file:
        await translator.tts("Hello world!", file=file, targetlang="en")


if __name__ == "__main__":
    asyncio.run(main())
