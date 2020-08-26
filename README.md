# gpytranslate
A Python3 library for translating text using Google Translate API.

----
## Features

  - **Dot accessible values**
  - **Supports emoji**
  - **Asynchronous**
  - **Type hinted**
  - **Free to use**
  - **Easy**

----
## Quick Start

### Installation
Requirements:
- Python 3.6 or higher.


```
$ python -m pip install gpytranslate
```
----
### Usage

[Example:](https://github.com/DavideGalilei/gpytranslate/blob/master/examples/example.py)
```
from gpytranslate import Translator
import asyncio


async def main():
    tr = Translator()
    translation = await tr("Ciao come stai? Io bene ahah.", targetlang='en')
    language = await tr.detect("Ciao come stai? Io bene ahah.")
    print(f"Translation: {translation.text}\nDetected language: {language}")


if __name__ == "__main__":
    asyncio.run(main())
```

Output:
```
Translation: Hello how are you? I'm fine, haha.
Detected language: it
```
----
## Development

Want to contribute? Pull requests are accepted!

----
## License
GNU GPLv3
