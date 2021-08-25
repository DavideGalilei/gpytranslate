"""
    gpytranslate - A Python3 library for translating text using Google Translate API.
    MIT License

    Copyright (c) 2021 Davide Galilei

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
import asyncio

import pytest


from gpytranslate import Translator


@pytest.mark.asyncio
async def test_gather():
    translator = Translator()
    tasks = [
        translator.translate("Hello world!", targetlang="it"),
        translator.translate("Ciao mondo!", targetlang="en"),
    ]

    results = await asyncio.gather(*tasks)

    assert results[0].text.lower() == "ciao mondo!", "Translation is wrong"
    assert results[1].text.lower() == "hello world!", "Translation is wrong"