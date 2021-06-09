from telethon import events
import random, re
from userbot.utils import admin_cmd
import asyncio 



@borg.on(admin_cmd("السورس"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("⦑ Welcome to Source ⦒\n\n⌁ ¦ JMTHON TEAM \n┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉\n⌁ ¦ [SOURCE CHANNEL](t.me/JMTHON)\n\n⌁ ¦  [TOOLS CHANNEL](t.me/JMTHON_TOOLS)      \n\n⌁ ¦ [MUHMMAD DEV](T.ME/RRRD7)\n\n⌁ ¦ [JASEM DEV](t.me/UUNZZ)\n ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ \n\n⌁ ¦ [CHAT SUPPORT](T.ME/JMTHON_CHAT)")
