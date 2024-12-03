from collections.abc import Mapping
from typing import Any, Callable, Dict, List, Union

from .translated_object import TranslatedObject


class BaseTranslator:
    headers: Union[dict, Callable[[], dict]]

    @staticmethod
    def parse(
        raw: Dict[str, Any], translated: bool = True
    ) -> Union[TranslatedObject, Dict[str, Any]]:
        """Parse raw API response into TranslatedObject.
        
        Args:
            raw: Raw response from translation API
            translated: Whether to return TranslatedObject or dict
            
        Returns:
            Either TranslatedObject or raw dict based on translated parameter
        """
        if translated:
            return TranslatedObject.from_raw_response(raw)
        return raw

    def check(
        self,
        text: Union[str, Mapping, List[str]],
        raw: Union[Mapping, List],
        client: str,
        dt: str,
    ) -> Union[TranslatedObject, Dict[str, TranslatedObject], List[TranslatedObject]]:
        """Check and parse API response based on input type.
        
        Args:
            text: Original input text
            raw: Raw API response
            client: API client type
            dt: Data type parameter
            
        Returns:
            Parsed translation result(s)
        """
        if client != "gtx" or dt != "t":
            return raw  # type: ignore

        if isinstance(text, str):
            return self.parse(raw)  # type: ignore
        elif isinstance(text, Mapping):
            return {k: self.parse(v) for k, v in raw.items()}  # type: ignore
        else:
            return [self.parse(elem) for elem in raw]  # type: ignore

    def get_headers(self) -> dict:
        return self.headers() if callable(self.headers) else self.headers

    @staticmethod
    def parse_tts(
        client: str,
        targetlang: str,
        idx: int,
        prev: str,
        text: Union[str, List[str], Dict[Any, str], Mapping[Any, Any]],
        textlen: Optional[int],
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
