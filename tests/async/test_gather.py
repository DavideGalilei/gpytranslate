import asyncio

import pytest

from gpytranslate import Translator


@pytest.mark.asyncio
async def test_gather() -> None:
    translator = Translator()
    tasks = [
        translator.translate("Hello world!", targetlang="it"),
        translator.translate("Ciao mondo!", targetlang="en"),
    ]

    results = await asyncio.gather(*tasks)

    assert results[0].text.lower() == "ciao mondo!", "Translation is wrong"
    assert results[1].text.lower() == "hello world!", "Translation is wrong"
