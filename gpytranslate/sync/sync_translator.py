from collections.abc import Mapping
from typing import Any, BinaryIO, Callable, Dict, List, Optional, TypeVar, Union, overload

import httpx

from ..exceptions import TranslationError
from ..types import (
    DEFAULT_TRANSLATION_ENDPOINT,
    DEFAULT_TTS_ENDPOINT,
    BaseTranslator,
    TranslatedObject,
    get_base_headers,
)

T = TypeVar("T", str, List[str], Dict[Any, str], Mapping)


class SyncTranslator(BaseTranslator):
    def __init__(
        self,
        proxies: Optional[Dict[str, str]] = None,
        url: str = DEFAULT_TRANSLATION_ENDPOINT,
        tts_url: str = DEFAULT_TTS_ENDPOINT,
        headers: Optional[Union[dict, Callable[[], dict]]] = None,
        **options,
    ):
        self.url = url
        self.tts_url = tts_url
        self.proxies = proxies
        self.options = options
        self.headers = get_base_headers if headers is None else headers

    @overload
    def translate(
        self,
        text: str,
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra,
    ) -> TranslatedObject: ...

    @overload
    def translate(
        self,
        text: List[str],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra,
    ) -> List[TranslatedObject]: ...

    @overload
    def translate(
        self,
        text: Dict[Any, str],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra,
    ) -> Dict[str, TranslatedObject]: ...

    def translate(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra,
    ) -> Union[TranslatedObject, List[TranslatedObject], Dict[str, TranslatedObject]]:
        """
        A function that translates text.

        Parameters:
            text: str = Text to translate.


            sourcelang: str = "text" original language, pass "auto" for auto-detection (default: "auto").


            targetlang: str = target language for translating "text" (default: "en").


            client: str = Google Translate client platform I guess, it's not well documented. (default: "gtx")
                (Will return the raw API json if "client" is not "gtx")


            dt: str = Specifies what to return to the API reply (default: "t").
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
            if v is not None
        }

        try:
            proxies: Dict[str, httpx.HTTPTransport] = {}
            if self.proxies:
                if proxies.get("https"):
                    proxies["https"] = httpx.HTTPTransport(proxy=self.proxies["https"])
                if proxies.get("http"):
                    proxies["http"] = httpx.HTTPTransport(proxy=self.proxies["http"])
                if proxies.get("socks5"):
                    proxies["socks5"] = httpx.HTTPTransport(proxy=self.proxies["socks5"])
                if proxies.get("socks5h"):
                    proxies["socks5h"] = httpx.HTTPTransport(proxy=self.proxies["socks5h"])

            with httpx.Client(mounts=proxies, **self.options) as c:
                raw: Union[Mapping, List] = (
                    c.post(
                        self.url,
                        params={**params, "q": text},
                        headers=self.get_headers(),
                    ).json()
                    if isinstance(text, str)
                    else (
                        {
                            k: c.post(
                                self.url,
                                params={**params, "q": v},
                                headers=self.get_headers(),
                            ).json()
                            for k, v in text.items()
                        }
                        if isinstance(text, Mapping)
                        else [
                            c.post(
                                self.url,
                                params={**params, "q": elem},
                                headers=self.get_headers(),
                            ).json()
                            for elem in text
                        ]
                    )
                )
                c.close()

            return self.check(raw=raw, client=client, dt=dt, text=text)
        except Exception as e:
            raise TranslationError(e) from None

    def detect(self, text: Union[str, list, dict]):
        if isinstance(text, str):
            return self(text).lang
        elif isinstance(text, list):
            return [self(elem).lang for elem in text]
        elif isinstance(text, dict):
            return {k: self(v).lang for k, v in text.items()}
        else:
            raise ValueError("Language detection works only with str, list and dict")

    def tts(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping],
        file: BinaryIO,
        targetlang: str = "en",
        client: str = "at",
        idx: int = 0,
        prev: str = "input",
        chunk_size: int = 1024,
        textlen: Optional[int] = None,
        **extra,
    ) -> BinaryIO:
        params = self.parse_tts(
            client=client,
            targetlang=targetlang,
            idx=idx,
            prev=prev,
            text=text,
            textlen=textlen,
            extra=extra,
        )
        try:
            proxies: Dict[str, httpx.HTTPTransport] = {}
            if self.proxies:
                if proxies.get("https"):
                    proxies["https"] = httpx.HTTPTransport(proxy=self.proxies["https"])
                if proxies.get("http"):
                    proxies["http"] = httpx.HTTPTransport(proxy=self.proxies["http"])
                if proxies.get("socks5"):
                    proxies["socks5"] = httpx.HTTPTransport(proxy=self.proxies["socks5"])
                if proxies.get("socks5h"):
                    proxies["socks5h"] = httpx.HTTPTransport(proxy=self.proxies["socks5h"])

            with httpx.stream(
                "GET",
                url=self.tts_url,
                params=params,
                headers=self.get_headers(),
            ) as resp:
                resp: httpx.Response
                for chunk in resp.iter_bytes(chunk_size=chunk_size):
                    file.write(chunk)
            return file
        except Exception as e:
            raise TranslationError(e) from None

    __call__ = translate
