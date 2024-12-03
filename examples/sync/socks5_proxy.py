from gpytranslate import SyncTranslator

t = SyncTranslator(proxies={"socks5": "socks5://user:password@127.0.0.1:1080"})
# Check out https://pypi.org/project/httpx-socks/
translation = t.translate("Ciao Mondo!", targetlang="en")
# Hello World!
print(f"Translation: {translation.text}")
