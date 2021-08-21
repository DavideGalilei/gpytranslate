"""
    gpytranslate - A Python3 library for translating text using Google Translate API.
    MIT License

    Copyright (c) 2021 Davide Galilei

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import json

from typing import Union


class TranslatedObject(dict):
    def __getattr__(self: Union[str, dict, list], attr: str):
        if isinstance(self, list):
            return [TranslatedObject(elem) for elem in self]
        return (
            TranslatedObject(dict.get(self, attr))
            if isinstance(dict.get(self, attr), dict)
            else dict.get(self, attr)
        )

    def __str__(self):
        return json.dumps(
            {k: v if len(str(v)) < 200 else "..." for k, v in self.items()}, indent=4
        )

    __setattr__ = dict.__setitem__

    __delattr__ = dict.__delitem__
