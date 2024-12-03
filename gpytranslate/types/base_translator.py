from collections.abc import Mapping
from typing import Any, Dict, List, Union

from .translated_object import TranslatedObject


class BaseTranslator:
    headers: Union[dict, callable]

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

    def get_headers(self) -> dict:
        return self.headers() if callable(self.headers) else self.headers

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
