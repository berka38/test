import platform
import psutil
import time
from datetime import datetime
from utils.language import get_lang_manager

async def command(event, args):
    """
    Command: sysinfo
    Description: Shows system information and bot status
    Usage: !sysinfo
    """
    lang_manager = get_lang_manager()
    
    # Get system info
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    
    # Format the information
    info = [
        lang_manager.get_text("sysinfo.title"),
        lang_manager.get_text("sysinfo.os", os=f"{uname.system} {uname.release}"),
        lang_manager.get_text("sysinfo.machine", machine=uname.machine),
        lang_manager.get_text("sysinfo.processor", processor=uname.processor),
        lang_manager.get_text("sysinfo.cpu_usage", usage=cpu_usage),
        lang_manager.get_text("sysinfo.memory_usage", usage=memory.percent),
        lang_manager.get_text("sysinfo.uptime", uptime=str(datetime.now() - boot_time)),
        "",
        lang_manager.get_text("sysinfo.bot_info"),
        lang_manager.get_text("sysinfo.python_version", version=platform.python_version()),
        lang_manager.get_text("sysinfo.platform", platform=platform.platform()),
    ]
    
    return {
        "prefix": "sysinfo",
        "return": "\n".join(info)
    }
