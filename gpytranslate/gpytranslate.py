from collections.abc import Mapping
from typing import Union, Literal, Dict, List, Any

import httpx

from .types import TranslatedObject


class Translator:
    def __init__(
        self,
        proxies: Union[httpx.Proxy, Dict[str, str]] = None,
        url: str = "https://translate.googleapis.com/translate_a/single",
        **options
    ):
        self.url = url
        self.client: httpx.AsyncClient = httpx.AsyncClient(proxies=proxies, **options)

    async def translate(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: Literal["t", "at", "rm", "bd", "md", "ss", "ex", "rw", "dj"] = "t",
        dj: int = 1,
        **extra
    ) -> Union[TranslatedObject, List[TranslatedObject], Dict[str, TranslatedObject]]:

        """
        A function that translates text.

        Parameters:
            text: str = Text to translate.


            sourcelang: str = "text" original language, pass "auto" for auto detection (default: "auto").


            targetlang: str = target language for translating "text" (default: "en").


            client: str = Google Translate client platform I guess, it's not well documented. (default: "gtx")
                (Will return the raw API json if "client" is not "gtx")


            dt: str = Specifies what to return in the API reply (default: "t").
                (Will return the raw API json if "dt" is not "t".
                t - Translation of source text;
                at - Alternate translations;
                rm - Transcription / transliteration of source and translated texts;
                bd - Dictionary, in case source text is one word
                     (you get translations with articles, reverse translations, etc.);
                md - Definitions of source text, if it's one word;
                ss - Synonyms of source text, if it's one word;
                ex - Examples;
                rw - See also list;
                dj - Json response with names. (dj=1).)

            dj: int = Probably specifies dictionary output if true, else list (default: 1).

            extra: dict = Extra params to be sent to api endpoint.

        Returns:
            TranslatedObject or JSON serialized object.
        """

        params = {
            k: v
            for k, v in {
                "client": client,
                "sl": sourcelang,
                "tl": targetlang,
                "dt": dt,
                "ie": "utf-8",
                "oe": "utf-8",
                "dj": dj,
                **extra,
            }.items()
            if v
        }
        async with self.client as c:
            c: httpx.AsyncClient
            raw: Union[Mapping, List] = (
                (
                    await c.post(
                        self.url,
                        params={**params, "q": text},
                    )
                ).json()
                if isinstance(text, str)
                else (
                    {
                        k: (
                            await c.post(
                                self.url,
                                params={**params, "q": v},
                            )
                        ).json()
                        for k, v in text.items()
                    }
                    if isinstance(text, Mapping)
                    else [
                        (
                            await c.post(
                                self.url,
                                params={**params, "q": elem},
                            )
                        ).json()
                        for elem in text
                    ]
                )
            )

            if client != "gtx" or dt != "t":
                return raw

            if isinstance(text, str):
                return self.parse(raw)
            elif isinstance(text, Mapping):
                return {k: self.parse(v) for k, v in raw.items()}
            else:
                return [self.parse(elem) for elem in raw]

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

    async def detect(self, text: Union[str, list, dict]):
        if isinstance(text, str):
            return (await self(text)).lang
        elif isinstance(text, list):
            return [(await self(elem)).lang for elem in text]
        elif isinstance(text, dict):
            return {k: (await self(v)).lang for k, v in text.items()}
        else:
            raise ValueError("Language detection works only with str, list and dict")

    __call__ = translate  # Backwards compatibility
