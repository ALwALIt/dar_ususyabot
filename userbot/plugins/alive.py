#BY @RRRD7 
import random
import re
import time
from platform import python_version
from datetime import datetime

from telethon import version
from telethon.events import CallbackQuery

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import StartTime, catub, catversion, mention

ANIME_QUOTE = [
    "WELCOME TO JMTHON  BOT",
]
plugin_category = "utils"

start = datetime.now()
@catub.cat_cmd(
    pattern="فحص$",
    command=("فحص", plugin_category),
    info={
        "header": "To check bot's alive status, Plugin by [∞](https://t.me/Infinity20998),[Λｙａｎ](https://t.me/not_ayan)",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    ANIME = f"{random.choice(ANIME_QUOTE)}"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or ANIME
    CAT_IMG = gvarstatus("ALIVE_PIC")
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        cat_caption += f"**{EMOJI} نسخـۿ جـمثون:** `{catversion}`\n"
        cat_caption += f"**{EMOJI} نسخۿ تليثون  :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI} قاعدۿ البيانات:** `{check_sgnirts}\n`"
        cat_caption += f"**{EMOJI} المنشئ:** {mention}\n"
        cat_caption += f"**{EMOJI} الوقت :** `{uptime}`\n"
        cat_caption += f"*{EMOJI} قـناة السـورس: @JMTHON \n" 
        await event.client.send_file(
            event.chat_id,
            PIC,
            caption=cat_caption,
            reply_to=reply_to_id,
            allow_cache=True,
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{ALIVE_TEXT}**\n\n"
            f"**{EMOJI} قاعدۿ البيانات :** `{check_sgnirts}`\n"
            f"**{EMOJI} نسخۿ تليثون  :** `{version.__version__}\n`"
            f"**{EMOJI} نسخـۿ جـمثون :** `{catversion}`\n"
            f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
            f"**{EMOJI} الوقت :** `{uptime}\n`"
            f"**{EMOJI} المنشئ:** {mention}\n",
        )



@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
