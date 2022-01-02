class GpytranslateException(Exception):
    pass


class TranslationError(GpytranslateException):
    def __init__(self, exception: Exception):
        self.args = (exception,)

    def __str__(self) -> str:
        return f"An error occurred while trying to translate/tts: {self.args[0]!r}"
