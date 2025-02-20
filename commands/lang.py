from utils.language import get_lang_manager

async def command(event, args):
    """
    Command: lang
    Description: Change bot language or list available languages
    Usage: 
        !lang - Show current language
        !lang list - List available languages
        !lang <code> - Change language (en/es/tr)
    """
    lang_manager = get_lang_manager()
    
    if not args:
        # Show current language
        current = lang_manager.get_current_language()
        native_names = lang_manager.get_available_languages()
        return {
            "prefix": "lang",
            "return": lang_manager.get_text("lang.current", lang=native_names[current])
        }
    
    if args[0].lower() == "list":
        # List available languages
        native_names = lang_manager.get_available_languages()
        languages = [f"• {code}: {name}" for code, name in native_names.items()]
        return {
            "prefix": "lang",
            "return": f"{lang_manager.get_text('lang.available')}\n\n" + "\n".join(languages)
        }
    
    # Change language
    new_lang = args[0].lower()
    if lang_manager.set_language(new_lang):
        native_names = lang_manager.get_available_languages()
        return {
            "prefix": "lang",
            "return": lang_manager.get_text("lang.changed", lang=native_names[new_lang])
        }
    else:
        native_names = lang_manager.get_available_languages()
        available = ", ".join(native_names.keys())
        return {
            "prefix": "lang",
            "return": lang_manager.get_text("lang.not_found", lang=new_lang, available=available)
        }
