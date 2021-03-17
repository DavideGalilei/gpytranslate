import json
from typing import Union

import httpx

from .types import TranslatedObject


class Translator:
    async def __call__(
        self,
        text: str,
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        **extra
    ):

        """
        A function that translates text.

        Parameters:
            text: str = Text to translate.


            sourcelang: str = "text" original language, pass "auto" for auto detection (default: "auto").


            targetlang: str = target language for translating "text" (default: "en").


            client: str = Google Translate client platform I guess, it"s not well documented so I don"t really know (default: "gtx").

                (Will return the raw API json if "client" is not "gtx")


            dt: str = Specifies what to return in the API reply (default: "t").

                (Will return the raw API json if "dt" is not "t".
                 t - Translation of source text;
                 at - Alternate translations;
                 rm - Transcription / transliteration of source and translated texts;
                 bd - Dictionary, in case source text is one word (you get translations with articles, reverse translations, etc.);
                 md - Definitions of source text, if it"s one word;
                 ss - Synonyms of source text, if it"s one word;
                 ex - Examples;
                 rw - See also list;
                 dj - Json response with names. (dj=1).)

            extra: dict = Extra params to be sent to api endpoint.

        Returns:
            JSON serialized object.
        """

        params = {
            k: v
            for k, v in {
                "client": client,
                "sl": (
                    sourcelang[0]
                    if isinstance(sourcelang, list) or isinstance(sourcelang, tuple)
                    else (
                        sourcelang["sl"] if isinstance(sourcelang, dict) else sourcelang
                    )
                ).lower(),
                "tl": (
                    targetlang[0]
                    if isinstance(targetlang, list) or isinstance(targetlang, tuple)
                    else (
                        targetlang["tl"] if isinstance(targetlang, dict) else targetlang
                    )
                ).lower(),
                "dt": dt,
                "q": text,
                "ie": "utf-8",
                "oe": "utf-8",
                **extra,
            }.items()
            if v
        }
        async with httpx.AsyncClient() as c:
            r = await c.post(
                "https://translate.googleapis.com/translate_a/single?dj=1",
                params=params,
            )
            await c.__aexit__()

        r = json.loads(r.content.decode("utf-8"))

        if not client == "gtx":
            return r

        _tmp = {
            "raw": TranslatedObject(r),
            "orig": " ".join([s["orig"] for s in r["sentences"] if "orig" in s]),
            "text": " ".join([s["trans"] for s in r["sentences"] if "trans" in s]),
            "orig_raw": [s["orig"] for s in r["sentences"] if "orig" in s],
            "text_raw": [s["trans"] for s in r["sentences"] if "trans" in s],
            "lang": r["src"],
        }

        return TranslatedObject(_tmp)

    async def detect(self, text: Union[str, list, dict]):
        if isinstance(text, str):
            return (await self(text)).lang
        elif isinstance(text, list):
            return [(await self(elem)).lang for elem in text]
        elif isinstance(text, dict):
            return {k: (await self(v)).lang for k, v in text.items()}
        else:
            raise ValueError("Language detection works only with str, list and dict")
