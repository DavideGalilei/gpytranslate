import asyncio

from gpytranslate import Translator


async def main():
    t = Translator(proxies={"https://": "https://{proxy_ip_here}"})
    # Check out https://www.python-httpx.org/compatibility/#proxy-keys
    translation = await t.translate("Ciao Mondo!", targetlang="en")
    # Hello World!
    print(f"Translation: {translation.text}")


if __name__ == "__main__":
    asyncio.run(main())
