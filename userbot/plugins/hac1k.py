"""command: .hack & .thack """
# @RRRD7  - @UUNZZ
import asyncio

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
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
        if idd == 1614649021:
            await edit_or_reply(
                event, "**هذا مطور سورسك لا يمكن اختراقه ❕**"
            )
        else:
            event = await edit_or_reply(event, "يتم الاختراق ..")
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
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "لم يتم العثور على المستخدم \n لا يمكن التهكير",
            parse_mode=_format.parse_pre,
        )