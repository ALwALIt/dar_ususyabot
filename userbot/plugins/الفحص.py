import random
import re
import time
from platform import python_version

from telethon import version, Button
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, jmthon, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@jmthon.ar_cmd(
    pattern="السورس$",
    command=("السورس", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, 'السورس')
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@jmthon.ar_cmd(
    pattern="فحص$",
    command=("فحص", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  - "
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or " SOURCE JMTHON "
    CAT_IMG = gvarstatus("ALIVE_PIC") or " https://telegra.ph/file/794e7311e8e3aadcf8dff.jpg "
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        cat_caption += f"𓍹———————×———————————𓍻\n"
        cat_caption += f"**{EMOJI} قاعدة البيانات :** تـعمل بنجـاح\n"
        cat_caption += f"**{EMOJI} نسخـۿ التليثون  :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI} نسخـۿ جـمثون :** `{catversion}`\n"
        cat_caption += f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI} مدة التشغيل :** `{uptime}\n`"
        cat_caption += f"**{EMOJI} المستخدم:** {mention}\n"
        cat_caption += f"**{EMOJI}**  **[مطور السورس]**(t.me/JMTHON)   \n"
        cat_caption += f"𓍹———————×———————————𓍻\n"
        await event.client.send_file(
            event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} قاعدۿ البيانات :** `تـعمل بنجـاح`\n"
            f"**{EMOJI} نسخۿ تليثون :** `{version.__version__}\n`"
            f"**{EMOJI} نسخـۿ جـمثون :** `{catversion}`\n"
            f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
            f"**{EMOJI} الوقت :** `{uptime}\n`"
            f"**{EMOJI} المنشئ:** {mention}\n",
        )

@jmthon.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
