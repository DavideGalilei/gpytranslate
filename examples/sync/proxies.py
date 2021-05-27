from gpytranslate import SyncTranslator

t = SyncTranslator(proxies={"https": "https://{proxy_ip_here}"})
# Check out https://docs.python-requests.org/en/latest/api/#module-requests
# or https://stackoverflow.com/questions/8287628/proxies-with-python-requests-module
translation = t.translate("Ciao come stai? Io bene ahah.", targetlang="en")
language = t.detect("Ciao come stai? Io bene ahah.")
print(f"Translation: {translation.text}\nDetected language: {language}")
