"""Custom exceptions for gpytranslate."""
from typing import Tuple


class GpytranslateException(Exception):
    """Base exception for all gpytranslate errors."""


class TranslationError(GpytranslateException):
    """Raised when a translation or TTS operation fails."""
    
    def __init__(self, exception: Exception) -> None:
        """Initialize the error with the underlying exception.
        
        Args:
            exception: The original exception that caused this error
        """
        self.args: Tuple[Exception, ...] = (exception,)

    def __str__(self) -> str:
        """Get string representation of the error.
        
        Returns:
            str: Formatted error message with the underlying exception
        """
        return f"An error occurred while trying to translate/tts: {self.args[0]!r}"
