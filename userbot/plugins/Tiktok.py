"""QuotLy: Avaible commands: .تحويل
"""
import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="تيكتوك ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("⌯︙يـجب. الرد علـى الرابط )")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("⌯︙يـجب. الرد علـى الرابط )")
       return
    chat = "@TIKTOKDOWNLOADROBOT"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("⌯︙يـجب. الرد علـى الرابط )")
       return
    await event.edit("⌯︙جار تحميل الفيديو")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users= 1598492699))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Please unblock me (@QuotLyBot) u Nigga```")
              return
          if response.text.startswith("Hi!"):
             await event.edit("⌯︙يجـب الغاء خصـوصية التوجيـه اولا")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
             
# Copyright (C) 2021 JepThon TEAM
# FILES WRITTEN BY  @RR7PP
