from telethon import events
import random, re
from userbot.utils import admin_cmd
import asyncio 



@borg.on(admin_cmd("السورس"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("⦑ مرحبا بك في جمثون ⦒\n\n⌁ ¦ JMTHON TEAM \n┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉\n⌁ ¦ [قناة سورس جمثون](t.me/JMTHON)\n\n⌁ ¦  [قناة مساعدة جمثون](t.me/JMTHON_TOOLS)      \n\n⌁ ¦ [المطور السورس¹](T.ME/RRRD7)\n\n⌁ ¦ [المطور السورس²](t.me/UUNZZ)\n ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ \n\n⌁ ¦ [كروب المساعدة](t.me/JMTHON_CHAT)")
