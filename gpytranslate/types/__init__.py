import random

from .translated_object import TranslatedObject
from .base_translator import BaseTranslator

DEFAULT_TRANSLATION_ENDPOINT: str = "https://translate.google.com/translate_a/single"
DEFAULT_TTS_ENDPOINT: str = "https://translate.google.com/translate_tts"


class Device:
    DEVICES: tuple = (
        "Linux; U; Android 10; Pixel 4",
        "Linux; U; Android 10; Pixel 4 XL",
        "Linux; U; Android 10; Pixel 4a",
        "Linux; U; Android 10; Pixel 4a XL",
        "Linux; U; Android 11; Pixel 4",
        "Linux; U; Android 11; Pixel 4 XL",
        "Linux; U; Android 11; Pixel 4a",
        "Linux; U; Android 11; Pixel 4a XL",
        "Linux; U; Android 11; Pixel 5",
        "Linux; U; Android 11; Pixel 5a",
        "Linux; U; Android 12; Pixel 4",
        "Linux; U; Android 12; Pixel 4 XL",
        "Linux; U; Android 12; Pixel 4a",
        "Linux; U; Android 12; Pixel 4a XL",
        "Linux; U; Android 12; Pixel 5",
        "Linux; U; Android 12; Pixel 5a",
        "Linux; U; Android 12; Pixel 6",
        "Linux; U; Android 12; Pixel 6 Pro",
    )

    __i = 0

    @classmethod
    def shift(cls) -> str:
        cls.__i += 1
        cls.__i %= len(cls.DEVICES)
        return cls.DEVICES[cls.__i]


def get_base_headers() -> dict:
    return {
        "User-Agent": "GoogleTranslate/6.28.0.05.421483610 ({device})".format(
            device=Device.shift(),
        )
    }
