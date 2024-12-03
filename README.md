# gpytranslate

[![PyPI version](https://badge.fury.io/py/gpytranslate.svg)](https://badge.fury.io/py/gpytranslate)
[![Python Versions](https://img.shields.io/pypi/pyversions/gpytranslate.svg)](https://pypi.org/project/gpytranslate/)
[![License](https://img.shields.io/github/license/DavideGalilei/gpytranslate.svg)](https://github.com/DavideGalilei/gpytranslate/blob/master/LICENSE)

A Python3 library for translating text using Google Translate API.
## Features
 - **Both Synchronous and Asynchronous**
 - **Dot accessible values**
 - **Supports emoji**
 - **Type hinted**
 - **Free to use**
 - **Easy**

----
## Quick Start

### Installation

Requirements:
- Python 3.9 or higher
- httpx[socks] >= 0.28.0
- aiofiles >= 24.1.0
- typing-extensions >= 4.12.2

Install using pip:
```bash
python3 -m pip install -U gpytranslate
```

Or install with poetry:
```bash
poetry add gpytranslate
```
----
### Usage

[Async Example:](/examples/async/example.py)
```python
from gpytranslate import Translator
import asyncio


async def main():
    t = Translator()
    translation = await t.translate("Ciao come stai? Io bene ahah.", targetlang="en")
    language = await t.detect(translation.text)
    print(f"Translation: {translation.text}\nDetected language: {language}")


if __name__ == "__main__":
    asyncio.run(main())
```

[Sync Example:](/examples/sync/example.py)
```python
from gpytranslate import SyncTranslator

t = SyncTranslator()
translation = t.translate("Ciao come stai? Io bene ahah.", targetlang="en")
language = t.detect(translation.text)
print(f"Translation: {translation.text}\nDetected language: {language}")
```
❓ **Note:** you could also check [tests](/tests) folder for extra examples.

Output:
```
Translation: Hello how are you? I'm fine, haha.
Detected language: en
```

### Text to Speech
[Async Example:](/examples/async/tts.py)
```python
import asyncio, aiofiles
from gpytranslate import Translator

async def main():
    translator = Translator()
    async with aiofiles.open("test.mp3", "wb") as file:
        await translator.tts("Hello world!", file=file)

if __name__ == "__main__":
    asyncio.run(main())
```

[Sync Example:](/examples/sync/tts.py)
```python
from gpytranslate import SyncTranslator

translator = SyncTranslator()

with open("test.mp3", "wb") as file:
    translator.tts("Hello world!", file=file)
```

----
## Useful Resources
https://danpetrov.xyz/programming/2021/12/30/telegram-google-translate.html
https://vielhuber.de/en/blog/google-translation-api-hacking/
https://github.com/OwlGramDev/OwlGram/blob/b9bb8a247758adbf7be7aaf3eb150f680bec1269/TMessagesProj/src/main/java/it/owlgram/android/translator/GoogleAppTranslator.java

### Language Codes

The library uses ISO 639-1 two-letter language codes. Some common examples:

- English: 'en'
- Spanish: 'es' 
- French: 'fr'
- German: 'de'
- Italian: 'it'
- Japanese: 'ja'
- Chinese (Simplified): 'zh'

### Error Handling

The library raises `TranslationError` when translation fails:

```python
from gpytranslate import Translator, TranslationError

translator = Translator()
try:
    result = await translator.translate("Hello", targetlang="invalid")
except TranslationError as e:
    print(f"Translation failed: {e}")
```

## Development

### Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.
## License
Licensed under the MIT License.

Click [here](/LICENSE) for further information.
