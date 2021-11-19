import os
from userbot import jmthon

from ..sql_helper.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from jmthon.functions.tools import create_tl_btn, format_btn, get_msg_button
from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id

from . import HNDLR, eor, get_string, mediainfo
from ._inline import something

Note = "\n\nNote: `{mention}`, `{group}`, `{count}`, `{name}`, `{fullname}`, `{username}`, `{userid}` can be used as formatting parameters.\n\n"


@jmthon.ar_cmd(pattern="ترحيب ميديا", groups_only=True)
async def save_welcome(event):
    x = await eor(event, get_string("com_1"))
    r = await event.get_reply_message()
    btn = format_btn(r.buttons) if (r and r.buttons) else None
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eor(x, get_string("com_4"), time=5)
            dl = await r.download_media()
            variable = uf(dl)
            os.remove(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "web":
            m = None
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            txt = r.text
            if not btn:
                txt, btn = get_msg_button(r.text)
            add_welcome_setting(event.chat_id, txt, m, btn)
        else:
            add_welcome_setting(event.chat_id, None, m, btn)
        await eor(x, get_string("grt_1"))
    elif r and r.text:
        txt = r.text
        if not btn:
            txt, btn = get_msg_button(r.text)
        add_welcome_setting(event.chat_id, txt, None, btn)
        await eor(x, get_string("grt_1"))
    else:
        await eor(x, get_string("grt_3"), time=5)


@jmthon.ar_cmd(pattern="حذف الترحيب$", groups_only=True)
async def del_welcome(event):
    if not add_welcome_setting(event.chat_id):
        return await eor(event, get_string("grt_4"), time=5)
    rm_welcome_setting(event.chat_id)
    await eor(event, get_string("grt_5"), time=5)


@jmthon.ar_cmd(pattern="الترحيبات ميديا$", groups_only=True)
async def show_welcome(event):
    wel = get_current_welcome_settings(event.chat_id)
    if not wel:
        return await eor(event, get_string("grt_4"), time=5)
    msgg = wel["welcome"]
    med = wel["media"]
    if wel.get("button"):
        btn = create_tl_btn(wel["button"])
        return await something(event, msgg, med, btn)
    await event.reply(f"**Welcome Note in this chat**\n\n`{msgg}`", file=med)
    await event.delete()
