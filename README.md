# gpytranslate
A Python3 library for translating text using Google Translate API.

----
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
- Python 3.6 or higher.


```bash
$ python3 -m pip install -U gpytranslate
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
## Development
Want to contribute? Pull requests are accepted!

----
## License
Licensed under the MIT License.

Click [here](/LICENSE) for further information.
