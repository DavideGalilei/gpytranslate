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
