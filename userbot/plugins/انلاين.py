from userbot.Config import Config
import asyncio

import requests
from telethon import functions
from . import *
from . import ALIVE_NAME


import requests
from telethon import functions
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot, BotInlineDisabledError as noinline, YouBlockedUserError
from ..core.managers import edit_or_reply

botname = Config.TG_BOT_USERNAME

@bot.on(admin_cmd(pattern="انلاين تفعيل ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="انلاين تفعيل ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Jepthon")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            jepiq = await edit_or_reply(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎تـم تفعيـل انـلاين بـوتك .. بنجـاح ☑️**\n\n**❈╎جـاري اعـادة تشغيل البـوت الرجـاء الانتظـار  ▬▭...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("Jepthon")
                    sixth = await conv.get_response()
                    seventh = await conv.send_message(perf)
                    eighth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await jeptiq.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تفعيـل انـلاين بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await edit_or_reply(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")


@bot.on(admin_cmd(pattern="انلاين تعطيل ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="انلاين تعطيل ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Jepthon")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            jepiq = await edit_or_reply(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎تـم تعطيـل انـلاين بـوتك .. بنجـاح ☑️**\n\n**❈╎جـاري اعـادة تشغيل البـوت الرجـاء الانتظـار  ▬▭...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("/empty")
                    sixth = await conv.get_response()
                    seventh = await conv.send_message(perf)
                    eighth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await jepiq.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تعطيـل انـلاين بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await edit_or_reply(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")
