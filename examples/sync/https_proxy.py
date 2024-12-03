from gpytranslate import SyncTranslator

t = SyncTranslator(proxies={"https://": "https://{proxy_ip_here}"})
# Check out https://www.python-httpx.org/compatibility/#proxy-keys
translation = t.translate("Ciao Mondo!", targetlang="en")
# Hello World!
print(f"Translation: {translation.text}")
