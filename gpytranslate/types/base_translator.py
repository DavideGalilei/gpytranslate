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

from collections.abc import Mapping
from typing import Union, Dict, List, Any

from .translated_object import TranslatedObject


class BaseTranslator:
    @staticmethod
    def parse(
        raw: Union[dict, Mapping], translated: bool = True
    ) -> Union[TranslatedObject, Dict[str, Union[TranslatedObject, str, List[str]]]]:
        x = {
            "raw": TranslatedObject(raw),
            "orig": " ".join(s["orig"] for s in raw["sentences"] if "orig" in s),
            "text": " ".join(s["trans"] for s in raw["sentences"] if "trans" in s),
            "orig_raw": [s["orig"] for s in raw["sentences"] if "orig" in s],
            "text_raw": [s["trans"] for s in raw["sentences"] if "trans" in s],
            "lang": raw["src"],
        }
        if translated:
            return TranslatedObject(x)
        return x

    def check(
        self,
        text: Union[str, Mapping, Any],
        raw: Union[Mapping, List],
        client: str,
        dt: str,
    ):
        if client != "gtx" or dt != "t":
            return raw

        if isinstance(text, str):
            return self.parse(raw)
        elif isinstance(text, Mapping):
            return {k: self.parse(v) for k, v in raw.items()}
        else:
            return [self.parse(elem) for elem in raw]

    @staticmethod
    def parse_tts(
        client: str,
        targetlang: str,
        idx: int,
        prev: str,
        text: str,
        textlen: int,
        extra: dict,
    ) -> Dict[str, Union[str, int]]:
        return {
            k: v
            for k, v in {
                "client": client,
                "tl": targetlang,
                "ie": "utf-8",
                "oe": "utf-8",
                "idx": idx,
                "prev": prev,
                "textlen": len(text) if textlen is None else textlen,
                "q": text,
                **extra,
            }.items()
            if v is not None
        }
