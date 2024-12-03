import asyncio

from gpytranslate import Translator


async def main():
    t = Translator(proxies={"socks5": "socks5://user:password@127.0.0.1:1080"})
    # Check out https://pypi.org/project/httpx-socks/
    translation = await t.translate("Ciao Mondo!", targetlang="en")
    # Hello World!
    print(f"Translation: {translation.text}")


if __name__ == "__main__":
    asyncio.run(main())
