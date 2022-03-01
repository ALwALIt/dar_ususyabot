from telethon import *
from userbot import jmthon
from userbot.sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from . import *

@jmthon.on(admin_cmd(pattern="نشر_التلقائي ?(.*)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "امر التلقائي يستخدم فقط للقنوات")
    hel_ = event.pattern_match.group(1)
    if str(hel_).startswith("-100"):
        jp = str(hel_).replace("-100", "")
    else:
        jp = hel_
    if not jp.isdigit():
        return await edit_or_reply(event, "**رجاء قم بوضع ايدي القناه بجانب الأمر !!**")
    if is_post(jp , event.chat_id):
        return await edit_or_reply(event, "هذا القناه بلفعل متفعل فيها التلقائي.")
    add_post(jp, event.chat_id)
    await edit_or_reply(event, f"**📍 تم بدء امر التلقائي لقناه :** `{hel_}`")


@jmthon.on(admin_cmd(pattern="ايقاف_النشر ?(.*)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "امر التلقائي يستخدم فقط للقنوات.")
    hel_ = event.pattern_match.group(1)
    if str(hel_).startswith("-100"):
        jp = str(hel_).replace("-100", "")
    else:
        jp = hel_
    if not jp.isdigit():
        return await edit_or_reply(event, "**رجاء قم بوضع ايدي القناه بجانب الأمر !!**")
    if not is_post(jp, event.chat_id):
        return await edit_or_reply(event, "هذا القناه لم يتم وضع تلقائي فيها.")
    remove_post(jp, event.chat_id)
    await edit_or_reply(event, f"**📍 تم ايقاف التلقائي لقناه : ** `{hel_}`")

@jmthon.ar_cmd(incoming=True)
async def _(event):
    if event.is_private:
        return
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set  = get_all_post(chat_id)
    if channels_set == []:
        return
    for chat in channels_set:
        if event.media:
            await event.client.send_file(int(chat), event.media, caption=event.text)
        elif not event.media:
            await bot.send_message(int(chat), event.message)
