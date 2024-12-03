import asyncio

from gpytranslate import Translator

"""Example showing how to use HTTPS proxy with the translator."""


async def main() -> None:
    """Demonstrate translation using an HTTPS proxy."""
    t = Translator(proxies={"https://": "https://{proxy_ip_here}"})
    # Check out https://www.python-httpx.org/compatibility/#proxy-keys
    translation = await t.translate("Ciao Mondo!", targetlang="en")
    # Hello World!
    print(f"Translation: {translation.text}")


if __name__ == "__main__":
    asyncio.run(main())
