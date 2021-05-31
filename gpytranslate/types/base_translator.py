"""
    gpytranslate - A Python3 library for translating text using Google Translate API.
    Copyright (C) 2020-2021  Davide Galilei

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
