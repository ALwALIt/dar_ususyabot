# Copyright (C) 2021 JMTHON TEAM
# FILES WRITTEN BY  @RRRD7

import asyncio

from userbot import jmthon

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import ALIVE_NAME

plugin_category = "fun"


@jmthon.ar_cmd(
    pattern="تهكير$",
    command=("تهكير", plugin_category),
    info={
        "header": "Fun Telegram hack animation.",
        "description": "Reply to user to show telegram hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}thack",
    },
)
async def _(event):
    "Fun Telegram hack animation."
    animation_interval = 2
    animation_ttl = range(12)
    if idd == 1614649021:
            await edit_or_reply(
                event, "This is My Master\nI can't hack my master's Account"
            )
    event = await edit_or_reply(event, "thack")
    animation_chars = [
        "**- يتم الربط بسيرفر الاختراق التابع لجـمثون...**",
                "**تم اختيار الضحية**",
                "**تهكير... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ **",
                "**تهكير... 84%\n█████████████████████▒▒▒▒ **",
                "**تهكير... 100%\n████████████████████████ **",
                f"**تم اختراق الضحية بنجاح 😈**...\n\n ادفع 96$ لـ  @JMTHON حتى ماننشر معلوماتك ❕",
            ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])