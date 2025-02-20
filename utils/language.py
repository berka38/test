import os
import yaml
from typing import Dict, Any

class LanguageManager:
    def __init__(self, lang_dir: str = "languages"):
        self.lang_dir = lang_dir
        self.current_lang = "en"
        self.languages: Dict[str, Dict[str, Any]] = {}
        self.load_languages()
    
    def load_languages(self):
        """Load all language files from the languages directory."""
        for filename in os.listdir(self.lang_dir):
            if filename.endswith('.yml'):
                lang_code = filename[:-4]
                with open(os.path.join(self.lang_dir, filename), 'r', encoding='utf-8') as f:
                    self.languages[lang_code] = yaml.safe_load(f)
    
    def get_text(self, key: str, **kwargs) -> str:
        """
        Get text in current language.
        Example: get_text("help.title")
        """
        try:
            # Split the key into parts (e.g., "help.title" -> ["help", "title"])
            parts = key.split('.')
            
            # Navigate through the dictionary
            text = self.languages[self.current_lang]
            for part in parts:
                text = text[part]
            
            # Format the text with provided kwargs
            return text.format(**kwargs)
        except (KeyError, AttributeError):
            # Fallback to English if key not found in current language
            try:
                text = self.languages['en']
                for part in parts:
                    text = text[part]
                return text.format(**kwargs)
            except (KeyError, AttributeError):
                return f"Missing text: {key}"
    
    def set_language(self, lang_code: str) -> bool:
        """Change current language."""
        if lang_code in self.languages:
            self.current_lang = lang_code
            return True
        return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages with their native names."""
        return {
            'en': 'English',
            'es': 'Español',
            'tr': 'Türkçe'
        }
    
    def get_current_language(self) -> str:
        """Get current language code."""
        return self.current_lang

# Global instance
_lang_manager = None

def get_lang_manager() -> LanguageManager:
    global _lang_manager
    if _lang_manager is None:
        _lang_manager = LanguageManager()
    return _lang_manager
