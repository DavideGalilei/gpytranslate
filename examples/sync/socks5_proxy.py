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

from httpx_socks import SyncProxyTransport

from gpytranslate import SyncTranslator

t = SyncTranslator(
    transport=SyncProxyTransport.from_url("socks5://user:password@127.0.0.1:1080")
)
# Check out https://pypi.org/project/httpx-socks/
translation = await t.translate("Ciao Mondo!", targetlang="en")
# Hello World!
print(f"Translation: {translation.text}")
