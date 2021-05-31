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
import io
from collections.abc import Mapping
from typing import Union, Dict, List, Any

import httpx
from aiofiles.threadpool import AsyncBufferedIOBase

from .types import TranslatedObject, BaseTranslator, BASE_HEADERS


class Translator(BaseTranslator):
    def __init__(
        self,
        proxies: Dict[str, str] = None,
        url: str = "https://translate.googleapis.com/translate_a/single",
        tts_url: str = "https://translate.google.com/translate_tts",
        headers: dict = ...,
        **options
    ):
        self.url = url
        self.tts_url = tts_url
        self.proxies = proxies
        self.options = options
        self.headers = BASE_HEADERS if headers is Ellipsis else headers
        self.client: httpx.AsyncClient = httpx.AsyncClient(proxies=proxies, **options)

    async def translate(
        self,
        text: Union[str, List[str], Dict[Any, str], Mapping],
        sourcelang: str = "auto",
        targetlang: str = "en",
        client: str = "gtx",
        dt: str = "t",
        # Literal["t", "at", "rm", "bd", "md", "ss", "ex", "rw", "dj"] = "t",
        # broken compatibility with python <3.8 :(
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
            if v is not None
        }
        async with self.client as c:
            c: httpx.AsyncClient
            raw: Union[Mapping, List] = (
                (
                    await c.post(
                        self.url,
                        params={**params, "q": text},
                        headers=self.headers,
                    )
                ).json()
                if isinstance(text, str)
                else (
                    {
                        k: (
                            await c.post(
                                self.url,
                                params={**params, "q": v},
                                headers=self.headers,
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
                                headers=self.headers,
                            )
                        ).json()
                        for elem in text
                    ]
                )
            )

        return self.check(raw=raw, client=client, dt=dt, text=text)

    async def detect(self, text: Union[str, list, dict]):
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
        text: Union[str, List[str], Dict[Any, str], Mapping],
        file: Union[AsyncBufferedIOBase, io.BytesIO],
        targetlang: str = "en",
        client: str = "at",
        idx: int = 0,
        prev: str = "input",
        chunk_size: int = 1024,
        textlen: int = None,
        **extra
    ) -> AsyncBufferedIOBase:
        params = self.parse_tts(
            client=client,
            targetlang=targetlang,
            idx=idx,
            prev=prev,
            text=text,
            textlen=textlen,
            extra=extra,
        )
        async with self.client.stream(
            "GET",
            url=self.tts_url,
            params=params,
            headers=self.headers,
        ) as response:
            response: httpx.Response
            if isinstance(file, io.BytesIO):
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    file.write(chunk)
            else:
                file: AsyncBufferedIOBase
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    await file.write(chunk)
        return file

    __call__ = translate  # Backwards compatibility
