import re
import time
from platform import python_version

from telethon import version
from telethon.events import CallbackQuery

from userbot import StartTime, catub, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from . import mention

CUSTOM_ALIVE_TEXT = Config.CUSTOM_ALIVE_TEXT or "⇝ 𝗪َ𝗘𝗟َِ𝗖𝗢𝗠َِ𝙀َِ 𝗧𝗢 𝗝𝗠𝗧𝗛𝗢𝗡 𝄵 ⇜"
EMOJI = Config.CUSTOM_ALIVE_EMOJI or "  - "

plugin_category = "utils"


@catub.cat_cmd(
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
    if Config.ALIVE_PIC:
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        cat_caption += f"**{EMOJI} قاعدۿ البيانات :** `{check_sgnirts}`\n"
        cat_caption += f"**{EMOJI} نسخۿ تليثون :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI} نسخـۿ جـمثون:** `{catversion}`\n"
        cat_caption += f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI} الوقت :** `{uptime}\n`"
        cat_caption += f"**{EMOJI} المنشئ:** {mention}\n"
        cat_caption += f"**{EMOJI}**  **[𝗦𝗼𝘂𝗿𝗰𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹]**(t.me/jmthon)   .\n"
        await alive.client.send_file(
            event.chat_id, Config.ALIVE_PIC, caption=cat_caption, reply_to=reply_to_id
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} قاعدۿ البيانات :** `تعمل بنجاح`\n"
            f"**{EMOJI} نسخۿ تليثون :** `{version.__version__}\n`"
            f"**{EMOJI} نسخـۿ جـمثون :** `{catversion}`\n"
            f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
            f"**{EMOJI} الوقت :** `{uptime}\n`"
            f"**{EMOJI} المنشئ:** {mention}\n"
            f"**{EMOJI} قنـاة السـورس**: (t.me/jmthon)\n",
        )


@catub.cat_cmd(
    pattern="السورس$",
    command=("السورس", plugin_category),
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
    cat_caption = f"**⇝ 𝗪َ𝗘𝗟َِ𝗖𝗢𝗠َِ𝙀َِ 𝗧𝗢 𝗝𝗠𝗧𝗛𝗢𝗡 𝄵 ⇜**\n"
    cat_caption += f"**{EMOJI} نسخۿ تليثون :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} نسخـۿ جـمثون :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} نسخـۿ البايثون :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} المنشئ:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
