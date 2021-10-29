
import random
import re
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, jmthon

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention


@jmthon.on(admin_cmd(pattern="(السورس|سورس)(?: |$)(.*)"))    
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "⎈ ⦙"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "أهـلا بـك فـي جيبثون العربي  👾"
    RR7_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/80727a17d54a33e821d16.jpg"
    me = await event.client.get_me()
    my_last = me.last_name
    my_mention = f"[{me.last_name}](tg://user?id={me.id})"
    TM = time.strftime("%I:%M")
    if RR7_IMG:
        CAT = [x for x in jmthon_IMG.split()]
        A_IMG = list(CAT
                    )
        PIC = random.choice(A_IMG
                           )
        cat_caption = f"**{ALIVE_TEXT}**\n 𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n" 
**{EMOJI} مـدة الـتشغيل  : {uptime} **
**{EMOJI} حسـابك  :   {my_mention} **
**{EMOJI} الـوقت  : {TM} **
**{EMOJI} السـورس :** @Jepthon 
𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻"""
        try:
            await event.client.send_file(event.chat_id, 
                 PIC, caption=cat_caption, 
                    reply_to=reply_to_id
                                        )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(event
                                      )
    else:
        await edit_or_reply(event,
            f"**{ALIVE_TEXT}**\n\n"
            f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧJEP⁦⁦ⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n 
            f"**{EMOJI} ❬ ٰمـدة الـتشغيل  : {uptime}  ٍَ❭**\n"
            f"**{EMOJI} ❬ ِحسـابك  :   zatlin2  ٍَ❭**\n"
            f"**{EMOJI} ❬ ٰ الـوقت  : {TM}  ٍَ❭**\n"
            f"**{EMOJI} ❬ ٰالسـورس :** @Jepthon  ٍَ❭\n"
            f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧJEP⁦⁦ⵧⵧⵧⵧⵧⵧⵧⵧ𓍻" )
