from .types import TranslatedObject
from typing import Union
import asyncio
import httpx


class Translator:
    async def __call__(self, text: str, sourcelang: Union[str, list, tuple, dict] = 'auto',
                       targetlang: Union[str, list, tuple, dict] = 'en', client: str = 'dict-chrome-ex', dt: str = 't',
                       ):
        """
        A function that translates text.

        Parameters:
            text: str = Text to translate.


            sourcelang: Union[str, list, tuple, dict] = 'text' original language, pass 'auto' for auto detection (default: 'auto').

                (If you pass a list or tuple, the input encoding (ie) will be sourcelang[1], example: ['auto', 'utf-8'];
                 Otherwise you can pass a dict, and it will take 'ie' key as sourcelang['ie'], example: {'sl': 'auto', 'ie': 'utf-8'})


            targetlang: Union[str, list, tuple, dict] = target language for translating 'text' (default: 'en').

                (If you pass a list or tuple, the output encoding (oe) will be targetlang[1], example: ['en', 'utf-8'];
                 Otherwise you can pass a dict, and it will take 'oe' key as targetlang['ie'], example: {'tl': 'en', 'ie': 'utf-8'})


            client: str = Google Translate client platform I guess, it's not well documented so I don't really know (default: 'dict-chrome-ex').

                (Will return the raw API json if 'client' is not 'dict-chrome-ex'. Try passing "gtx" as client.)


            dt: str = Specifies what to return in the API reply (default: 't').

                (Will return the raw API json if 'dt' is not 't'.
                 t - Translation of source text;
                 at - Alternate translations;
                 rm - Transcription / transliteration of source and translated texts;
                 bd - Dictionary, in case source text is one word (you get translations with articles, reverse translations, etc.);
                 md - Definitions of source text, if it's one word;
                 ss - Synonyms of source text, if it's one word;
                 ex - Examples;
                 rw - See also list;
                 dj - Json response with names. (dj=1).)

        Returns:
            JSON serialized object.
            """

        params = {
            k: v
            for k, v in
            {
                'client': client,
                'sl': (sourcelang[0] if isinstance(sourcelang, list) or isinstance(sourcelang, tuple) else (
                    sourcelang['sl'] if isinstance(sourcelang, dict) else sourcelang)).lower(),
                'tl': (targetlang[0] if isinstance(targetlang, list) or isinstance(targetlang, tuple) else (
                    targetlang['tl'] if isinstance(targetlang, dict) else targetlang)).lower(),
                'dt': dt,
                'q': text,
                'ie': (sourcelang[1] if isinstance(sourcelang, list) or isinstance(sourcelang, tuple) else (
                    sourcelang['ie'] if isinstance(sourcelang, dict) else '')).lower(),
                'oe': (targetlang[1] if isinstance(targetlang, list) or isinstance(targetlang, tuple) else (
                    targetlang['oe'] if isinstance(targetlang, dict) else '')).lower()
            }.items()
            if v
        }
        async with httpx.AsyncClient() as c:
            r = await c.get('https://clients5.google.com/translate_a/t', params=params)
            await c.__aexit__()

        r = r.json()
        if not client == "dict-chrome-ex":
            return r

        _tmp = {
            "raw": TranslatedObject(r),
            "orig": "".join([s['orig'] for s in r['sentences'] if 'orig' in s]),
            "text": "".join([s['trans'] for s in r['sentences'] if 'trans' in s]),
            "orig_raw": [s['orig'] for s in r['sentences'] if 'orig' in s],
            "text_raw": [s['trans'] for s in r['sentences'] if 'trans' in s],
            "lang": r['src']
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
