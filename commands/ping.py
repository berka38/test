from utils.language import get_lang_manager

async def command(event, args):
    """
    Command: ping
    Description: Check if the bot is responsive
    Usage: !ping
    """
    lang_manager = get_lang_manager()
    return {
        "prefix": "ping",
        "return": lang_manager.get_text("ping.response", default="Pong! 🏓")
    }
