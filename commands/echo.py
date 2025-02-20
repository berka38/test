from utils.language import get_lang_manager

async def command(event, args):
    """
    Command: echo
    Description: Repeats the given message
    Usage: !echo <message>
    """
    lang_manager = get_lang_manager()
    
    if not args:
        return {
            "prefix": "echo",
            "return": lang_manager.get_text("echo.no_message")
        }
    
    return {
        "prefix": "echo",
        "return": " ".join(args)
    }
