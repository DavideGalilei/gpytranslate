"""Translation result object implementation."""
import json
from typing import Any, Dict, List, Union


class TranslatedObject(dict):
    """A dictionary subclass that holds translation results with attribute access."""
    
    def __getattr__(self, attr: str) -> Union['TranslatedObject', List['TranslatedObject'], Any]:
        """Get attributes allowing dot notation access.
        
        Args:
            attr: The attribute name to access
            
        Returns:
            The attribute value, wrapped in TranslatedObject if it's a dict
        """
        if isinstance(self, list):
            return [TranslatedObject(elem) for elem in self]
            
        value = dict.get(self, attr)
        if isinstance(value, dict):
            return TranslatedObject(value)
        return value

    def __str__(self) -> str:
        """Get string representation, truncating long values.
        
        Returns:
            str: JSON formatted string with truncated values
        """
        return json.dumps(
            {k: v if len(str(v)) < 200 else "..." for k, v in self.items()},
            indent=4
        )

    # Maintain dict-like attribute access
    __setattr__ = dict.__setitem__  # type: ignore
    __delattr__ = dict.__delitem__  # type: ignore
