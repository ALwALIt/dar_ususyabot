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
    JMTHON = gvarstatus("ALIVE_EMOJI") or "  - "
    JMTHON_TEXT = gvarstatus("ALIVE_TEXT") or "**- JMTHON USERBOT.**"
    JMTHON_IMG = gvarstatus("ALIVE_PIC") or " https://telegra.ph/file/794e7311e8e3aadcf8dff.jpg "
    if JMTHON_IMG:
        RRRD7 = [x for x in JMTHON_IMG.split()]
        A_IMG = list(RRRD7)
        PIC = random.choice(A_IMG)
        RRRD7_caption = f"**{JMTHON_TEXT}**\n"
        RRRD7_caption += f"✛━━━━━━━━━━━━━✛\n"
        RRRD7_caption += f"**{JMTHON} قاعدة البيانات ›** تـعمل بنجـاح\n"
        RRRD7_caption += f"**{JMTHON} نسخـۿ التليثون  ›** {version.__version__}\n"
        RRRD7_caption += f"**{JMTHON} نسخـۿ جـمثون ›** {catversion}\n"
        RRRD7_caption += f"**{JMTHON} نسخـۿ البايثون ›** {python_version()}\n"
        RRRD7_caption += f"**{JMTHON} مدة التشغيل ›** {uptime}\n"
        RRRD7_caption += f"**{JMTHON} المستخدم ›** {mention}\n"
        RRRD7_caption += f"**{JMTHON}**  **[مطور السورس]**(t.me/JMTHON)   \n"
        RRRD7_caption += f"✛━━━━━━━━━━━━━✛\n"
        await event.client.send_file(
            event.chat_id, PIC, caption=RRRD7_caption, reply_to=reply_to_id
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{JMTHON_TEXT}**\n\n"
            f"**{JMTHON} قاعدۿ البيانات ›** `تـعمل بنجـاح`\n"
            f"**{JMTHON} نسخۿ تليثون ›** `{version.__version__}\n`"
            f"**{JMTHON} نسخـۿ جـمثون ›** `{catversion}`\n"
            f"**{JMTHON} نسخـۿ البايثون ›** `{python_version()}\n`"
            f"**{JMTHON} الوقت ›** `{uptime}\n`"
            f"**{JMTHON} المنشئ›** {mention}\n",
        )

@jmthon.ar_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  - "
    cat_caption = f"**سـورس جـمثـون يعـمل بـنجاح ✅**\n"
    cat_caption += f"**{EMOJI} نسخـۿ التليثون :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} نسخـۿ جـمثون :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} المستخدم :** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()

@jmthon.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
