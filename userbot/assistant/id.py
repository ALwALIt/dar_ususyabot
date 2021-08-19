#edit ~ @RR9R7
#For ~ @Jmthon
from telethon.utils import pack_bot_file_id
from telethon import events
from userbot import bot

@tgbot.on(events.NewMessage(pattern="/id ?(.*)"))
async def _(event):
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await tgbot.send_message(
                event.chat_id,
                "**ايـدي الـدردشة الـحالي هـو:** `{}`\n**ايدي المستـخدم:** `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                ),
            )
        else:
            await tgbot.send_message(
                event.chat_id,
                "**ايـدي الـدردشة الـحالي هـو:** `{}`\n**ايدي المستـخدم:** `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                ),
            )
    else:
        await bot.send_message(
            event.chat_id, "**ايـدي الـدردشة الـحالي هـو:** `{}`".format(str(event.chat_id))
        )
