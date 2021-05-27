from collections.abc import Mapping
from typing import Union, Dict, List, Any

import requests

from ..types import TranslatedObject, BaseTranslator


class SyncTranslator(BaseTranslator):
    def __init__(
        self,
        proxies: Dict[str, str] = None,
        url: str = "https://translate.googleapis.com/translate_a/single",
        **options
    ):
        super().__init__()
        self.url = url
        self.proxies = proxies
        self.options = options

    def translate(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
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
        raw: Union[Mapping, List] = (
            (
                requests.post(
                    self.url,
                    params={**params, "q": text},
                    proxies=self.proxies,
                    **self.options,
                )
            ).json()
            if isinstance(text, str)
            else (
                {
                    k: requests.post(
                        self.url,
                        params={**params, "q": v},
                        proxies=self.proxies,
                        **self.options,
                    ).json()
                    for k, v in text.items()
                }
                if isinstance(text, Mapping)
                else [
                    requests.post(
                        self.url,
                        params={**params, "q": elem},
                        proxies=self.proxies,
                        **self.options,
                    ).json()
                    for elem in text
                ]
            )
        )

        return self.check(raw=raw, client=client, dt=dt, text=text)

    def detect(self, text: Union[str, list, dict]):
        if isinstance(text, str):
            return self(text).lang
        elif isinstance(text, list):
            return [self(elem).lang for elem in text]
        elif isinstance(text, dict):
            return {k: self(v).lang for k, v in text.items()}
        else:
            raise ValueError("Language detection works only with str, list and dict")

    __call__ = translate
