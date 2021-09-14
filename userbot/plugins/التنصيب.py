from telethon import events
import random, re
from userbot.utils import admin_cmd
import asyncio 

@borg.on(admin_cmd("التنصيب"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("⌯︙**مـرحبا بـك عزيـزي** \n⌯︙رابط التنصيب - [اضغط هنا](https://dashboard.heroku.com/new?template=https://github.com/JMTHON-AR/JMTHON-PACK/)\n⌯︙قناة السورس - @JEEPTHON")
