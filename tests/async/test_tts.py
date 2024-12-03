import os.path

import aiofiles.os
import pytest

from gpytranslate import Translator


@pytest.mark.asyncio
async def test_tts() -> None:
    """Test TTS output to a file."""
    translator = Translator()
    filename = "test.mp3"

    async with aiofiles.open(filename, "wb") as file:
        await translator.tts("Hello world!", file=file, targetlang="en")

    assert os.path.isfile(filename), "File doesn't exist"

    await aiofiles.os.remove(filename)
