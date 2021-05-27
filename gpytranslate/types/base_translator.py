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
