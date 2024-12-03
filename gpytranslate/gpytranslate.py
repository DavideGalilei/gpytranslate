import io
from collections.abc import Mapping
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union, overload

import httpx

from .exceptions import TranslationError
from .types import (
    DEFAULT_TRANSLATION_ENDPOINT,
    DEFAULT_TTS_ENDPOINT,
    BaseTranslator,
    TranslatedObject,
    get_base_headers,
)

T = TypeVar("T", str, List[str], Dict[Any, str], Mapping[Any, str])
K = TypeVar("K")


class AsyncBufferedIOBase(Protocol):
    async def write(self, data: bytes) -> int: ...
    async def close(self) -> None: ...


class Translator(BaseTranslator):
    def __init__(
        self,
        proxies: Optional[Dict[str, str]] = None,
        url: str = DEFAULT_TRANSLATION_ENDPOINT,
        tts_url: str = DEFAULT_TTS_ENDPOINT,
        headers: Optional[Union[Dict[str, str], Callable[[], Dict[str, str]]]] = None,
        **options: Any,
    ) -> None:
        """Initialize the translator.

        Args:
            proxies: Optional proxy configuration dictionary
            url: Translation API endpoint URL
            tts_url: Text-to-speech API endpoint URL
            headers: Custom headers or header generator function
            **options: Additional options passed to httpx.AsyncClient
        """
        self.url = url
        self.tts_url = tts_url
        self.proxies = proxies
        self.options = options
        self.headers = get_base_headers if headers is None else headers

    @overload
    async def translate(
        self,
        text: str,
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra: Any,
    ) -> TranslatedObject: ...

    @overload
    async def translate(
        self,
        text: List[str],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra: Any,
    ) -> List[TranslatedObject]: ...

    @overload
    async def translate(
        self,
        text: Dict[Any, str],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        dj: int = 1,
        **extra: Any,
    ) -> Dict[str, TranslatedObject]: ...

    async def translate(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping[str, str]],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        # Literal["t", "at", "rm", "bd", "md", "ss", "ex", "rw", "dj"] = "t",
        # broken compatibility with python <3.8 :(
        dj: int = 1,
        **extra: Any,
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
            proxies: Dict[str, httpx.AsyncHTTPTransport] = {}
            if self.proxies:
                if proxies.get("https"):
                    proxies["https"] = httpx.AsyncHTTPTransport(proxy=self.proxies["https"])
                if proxies.get("http"):
                    proxies["http"] = httpx.AsyncHTTPTransport(proxy=self.proxies["http"])
                if proxies.get("socks5"):
                    proxies["socks5"] = httpx.AsyncHTTPTransport(proxy=self.proxies["socks5"])
                if proxies.get("socks5h"):
                    proxies["socks5h"] = httpx.AsyncHTTPTransport(proxy=self.proxies["socks5h"])

            async with httpx.AsyncClient(mounts=proxies, **self.options) as http_client:
                raw: Union[Mapping[str, Any], List[Any]] = (
                    (
                        await http_client.post(
                            self.url,
                            params={**params, "q": text},
                            headers=self.get_headers(),
                        )
                    ).json()
                    if isinstance(text, str)
                    else (
                        {
                            k: (
                                await http_client.post(
                                    self.url,
                                    params={**params, "q": v},
                                    headers=self.get_headers(),
                                )
                            ).json()
                            for k, v in text.items()
                        }
                        if isinstance(text, Mapping)
                        else [
                            (
                                await http_client.post(
                                    self.url,
                                    params={**params, "q": elem},
                                    headers=self.get_headers(),
                                )
                            ).json()
                            for elem in text
                        ]
                    )
                )
                await http_client.aclose()

            return self.check(raw=raw, client=client, dt=dt, text=text)
        except Exception as e:
            raise TranslationError(e) from None

    async def detect(self, text: Union[str, List[Any], Dict[Any, Any]]) -> Union[str, List[str], Dict[Any, str]]:
        if isinstance(text, str):
            return (await self(text)).lang
        elif isinstance(text, list):
            return [(await self(elem)).lang for elem in text]
        elif isinstance(text, dict):
            return {k: (await self(v)).lang for k, v in text.items()}
        else:
            raise ValueError("Language detection works only with str, list and dict")

    async def tts(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping[K, str]],
        file: Union[AsyncBufferedIOBase, io.BytesIO],
        targetlang: str = "en",
        client: str = "at",
        idx: int = 0,
        prev: str = "input",
        chunk_size: int = 1024,
        textlen: Optional[int] = None,
        **extra: Any,
    ) -> Union[AsyncBufferedIOBase, io.BytesIO]:
        """Generate text-to-speech audio.

        Args:
            text: Text to convert to speech
            file: Output file or buffer
            targetlang: Target language code
            client: API client identifier
            idx: TTS segment index
            prev: Previous segment identifier
            chunk_size: Download chunk size
            textlen: Override text length
            **extra: Additional TTS parameters

        Returns:
            The output file/buffer with audio data

        Raises:
            TranslationError: If TTS generation fails
            ValueError: If targetlang is invalid
        """
        if not isinstance(targetlang, str) or len(targetlang) != 2:
            raise ValueError("targetlang must be a 2-letter language code")
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
            proxies: Dict[str, httpx.AsyncHTTPTransport] = {}
            if self.proxies:
                if proxies.get("https"):
                    proxies["https"] = httpx.AsyncHTTPTransport(proxy=self.proxies["https"])
                if proxies.get("http"):
                    proxies["http"] = httpx.AsyncHTTPTransport(proxy=self.proxies["http"])
                if proxies.get("socks5"):
                    proxies["socks5"] = httpx.AsyncHTTPTransport(proxy=self.proxies["socks5"])
                if proxies.get("socks5h"):
                    proxies["socks5h"] = httpx.AsyncHTTPTransport(proxy=self.proxies["socks5h"])

            async with httpx.AsyncClient(mounts=proxies, **self.options) as c:
                async with c.stream(
                    "GET",
                    url=self.tts_url,
                    params=params,
                    headers=self.get_headers(),
                ) as response:
                    if isinstance(file, io.BytesIO):
                        async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                            file.write(chunk)
                    else:
                        async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                            await file.write(chunk)
                await c.aclose()

            return file
        except Exception as e:
            raise TranslationError(e) from None

    __call__ = translate  # Backwards compatibility
