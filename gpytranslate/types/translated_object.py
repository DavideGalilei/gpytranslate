"""Translation result object implementation."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslatedObject:
    """A dataclass that holds translation results."""
    raw: Dict[str, Any]
    orig: str
    text: str 
    orig_raw: List[str]
    text_raw: List[str]
    lang: str
    
    def __str__(self) -> str:
        """Get string representation with the translated text.
        
        Returns:
            str: The translated text
        """
        return self.text

    @classmethod
    def from_raw_response(cls, raw: Dict[str, Any]) -> "TranslatedObject":
        """Create TranslatedObject from raw API response.
        
        Args:
            raw: Raw response dictionary from the translation API
            
        Returns:
            TranslatedObject: Parsed translation result
        """
        return cls(
            raw=raw,
            orig=" ".join(s["orig"] for s in raw["sentences"] if "orig" in s),
            text=" ".join(s["trans"] for s in raw["sentences"] if "trans" in s),
            orig_raw=[s["orig"] for s in raw["sentences"] if "orig" in s],
            text_raw=[s["trans"] for s in raw["sentences"] if "trans" in s],
            lang=raw["src"]
        )
