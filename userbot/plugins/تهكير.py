# Copyright (C) 2021 JMTHON TEAM
# FILES WRITTEN BY  @RR7PP

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
        "header": "Fun hack animation.",
        "description": "Reply to user to show hack animation",
        "note": "This is just for fun. Not real hacking.",
        "usage": "{tr}hack",
    },
)
async def _(event):
    "Fun hack animation."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        idd = reply_message.sender_id
        if idd == 1694386561:
            await edit_or_reply(
                event, "**⌯︙عـذرا لا استـطيع اخـتراق مـطوري اعـتذر او سيقـوم بتهـكيرك**"
            )
        else:
            event = await edit_or_reply(event, "يتـم الاختـراق ..")
            animation_chars = [
                "⌯︙تـم الربـط بسـيرفرات الـتهكير الخـاصة",
                "تـم تحـديد الضحـية",
                "**تهكيـر**... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ ",
                "**تهكيـر**... 84%\n█████████████████████▒▒▒▒ ",
                "**تهكيـر**... 100%\n████████████████████████ ",
                f"⌯︙** تـم اخـتراق الضـحية**..\n\nقـم بالـدفع الى {ALIVE_NAME} لعـدم نشـر معلوماتك وصـورك",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "⌯︙لم يتـم التعـرف على المستـخدم",
            parse_mode=_format.parse_pre,
        )
