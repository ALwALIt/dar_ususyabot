"""command: .تهكير & .تهكير """

import asyncio

from telethon.tl.functions.users import GetFullUserRequest

from . import ALIVE_NAME

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"


@bot.on(admin_cmd(pattern=r"تهكير$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"تهكير$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await event.client(GetFullUserRequest(reply_message.sender_id))
        idd = reply_message.sender_id
        if idd == 1694386561:
            await edit_or_reply(
                event, "ماكدر اهكر مطوري 😂♥️"
            )
        else:
            event = await edit_or_reply(event, "جـاري التـهكير..")
            animation_chars = [
                "`Connecting To Hacked Private Server...`",
                "`Target Selected.`",
                "`جـاري التـهكير ... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`جـاري التهكـير ... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`جـاري التـهكير ... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`جـاري التهكـير ... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`جـاري التـهكير ... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`جـاري التـهكير ... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`جـاري التهـكير ... 84%\n█████████████████████▒▒▒▒ `",
                "`جـاري التـهكير ... 100%\n█████████هكـررر███████████ `",
                f"`تم اختراق الحساب ادفع لـ @JMTHON..\n ` .",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(event, "لم يتم تعريف أي مستخدم \n لا يمكن اختراق الحساب")


CMD_HELP.update(
    {
   "تهكير": "**Plugin : **`hack`\
        \n\n**Syntax : **`.hack reply to a person`\
        \n**Function : **__shows an animation of hacking progess bar__\
        \n\n**Syntax : **`.thack reply to a person`\
        \n**Function : **__shows an animation of Telegram account hacking to a replied person__\
        \n\n**Syntax : **`.wahack reply to a person`\
        \n**Function : **__shows an animation of whatsapp account hacking to a replied person__\
    "
    }
)
