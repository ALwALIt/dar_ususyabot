# ----------------------------------------- #
#  @JMTHON  @RR7PP   #
# ----------------------------------------- #

import asyncio
import glob
import io
import os
import re
from pathlib import Path
from time import time

import ujson
from telethon import Button, types
from telethon.errors import BotResponseTimeoutError
from telethon.events import CallbackQuery
from telethon.utils import get_attributes
from wget import download

from userbot import jmthon

from ..Config import Config
from ..core import check_owner, pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import post_to_telegraph, progress, reply_id
from ..helpers.functions.utube import (
    _mp3Dl,
    _tubeDl,
    download_button,
    get_choice_by_id,
    get_ytthumb,
    yt_search_btns,
)
from ..plugins import BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./userbot/cache/ytsearch.json"
plugin_category = "bot"


@jmthon.ar_cmd(
    pattern="تنزيل(?:\s|$)([\s\S]*)",
    command=("تنزيل", plugin_category),
    info={
        "header": "ytdl with inline buttons.",
        "description": "To search and download youtube videos by inline buttons.",
        "usage": "{tr}iytdl [URL / Text] or [Reply to URL / Text]",
    },
)
async def iytdl_inline(event):
    "ytdl with inline buttons."
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    input_url = None
    if input_str:
        input_url = (input_str).strip()
    elif reply and reply.text:
        input_url = (reply.text).strip()
    if not input_url:
        return await edit_delete(event, " ⌯︙يجـب وضـع اسـم المـوضوع او بالـرد عـلـى الـرابـط")
    catevent = await edit_or_reply(event, f"🔎 يتـم البـحث في اليـوتيـوب عـن : `'{input_url}'`")
    flag = True
    cout = 0
    results = None
    while flag:
        try:
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, f"تنزيل {input_url}"
            )
            flag = False
        except BotResponseTimeoutError:
            await asyncio.sleep(2)
        cout += 1
        if cout > 5:
            flag = False
    if results:
        await catevent.delete()
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    else:
        await catevent.edit("**⌯︙عـذرا لـم استـطيع ايـجاد اي نتـيـجة**")


@jmthon.tgbot.on(
    CallbackQuery(
        data=re.compile(b"^ytdl_download_(.*)_([\d]+|mkv|mp4|mp3)(?:_(a|v))?")
    )
)
@check_owner
async def ytdl_download_callback(c_q: CallbackQuery):  # sourcery no-metrics
    yt_code = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    choice_id = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    downtype = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    if str(choice_id).isdigit():
        choice_id = int(choice_id)
        if choice_id == 0:
            await c_q.answer(" ⌯︙يتـم الـمعـالجـة 🔄  ", alert=False)
            await c_q.edit(buttons=(await download_button(yt_code)))
            return
    startTime = time()
    choice_str, disp_str = get_choice_by_id(choice_id, downtype)
    media_type = "الفيديـو" if downtype == "v" else "المقـطع صـوتـي"
    callback_continue = f" ⌯︙يتـم تـحـميـل  {media_type} الــرجاء الانتـظار"
    callback_continue += f"\n\nFormat Code : {disp_str}"
    await c_q.answer(callback_continue, alert=True)
    upload_msg = await c_q.client.send_message(BOTLOG_CHATID, "Uploading...")
    yt_url = BASE_YT_URL + yt_code
    await c_q.edit(
        f"<b>⬇️ يتـم تـحـميـل {media_type} ....</b>\n\n🔗  <a href={yt_url}> <b>الـرابـط</b></a>\n🆔  <b>صـيغة الـتنـزيل</b> : {disp_str}",
        parse_mode="html",
    )
    if downtype == "v":
        retcode = await _tubeDl(url=yt_url, starttime=startTime, uid=choice_str)
    else:
        retcode = await _mp3Dl(url=yt_url, starttime=startTime, uid=choice_str)
    if retcode != 0:
        return await upload_msg.edit(str(retcode))
    _fpath = ""
    thumb_pic = None
    for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
        if _path.lower().endswith((".jpg", ".png", ".webp")):
            thumb_pic = _path
        else:
            _fpath = _path
    if not _fpath:
        await edit_delete(upload_msg, "** ⌯︙لم يتـم الـعثـور عـلى اي شيئ !")
        return
    if not thumb_pic and downtype == "v":
        thumb_pic = str(await pool.run_in_thread(download)(await get_ytthumb(yt_code)))
    attributes, mime_type = get_attributes(str(_fpath))
    ul = io.open(Path(_fpath), "rb")
    uploaded = await c_q.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(
                d,
                t,
                c_q,
                startTime,
                "trying to upload",
                file_name=os.path.basename(Path(_fpath)),
            )
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        force_file=False,
        thumb=await c_q.client.upload_file(thumb_pic) if thumb_pic else None,
    )
    uploaded_media = await c_q.client.send_file(
        BOTLOG_CHATID,
        file=media,
        caption=f"<b>File Name : </b><code>{os.path.basename(Path(_fpath))}</code>",
        parse_mode="html",
    )
    await upload_msg.delete()
    await c_q.edit(
        text=f"📹  <a href={yt_url}><b>{os.path.basename(Path(_fpath))}</b></a>",
        file=uploaded_media.media,
        parse_mode="html",
    )


@jmthon.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_(listall|back|next|detail)_([a-z0-9]+)_(.*)"))
)
@check_owner
async def ytdl_callback(c_q: CallbackQuery):
    choosen_btn = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    data_key = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    page = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    if not os.path.exists(PATH):
        return await c_q.answer(
            "Search data doesn't exists anymore, please perform search again ...",
            alert=True,
        )
    with open(PATH) as f:
        view_data = ujson.load(f)
    search_data = view_data.get(data_key)
    total = len(search_data)
    if choosen_btn == "back":
        index = int(page) - 1
        del_back = index == 1
        await c_q.answer()
        back_vid = search_data.get(str(index))
        await c_q.edit(
            text=back_vid.get("message"),
            file=await get_ytthumb(back_vid.get("video_id")),
            buttons=yt_search_btns(
                del_back=del_back,
                data_key=data_key,
                page=index,
                vid=back_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "next":
        index = int(page) + 1
        if index > total:
            return await c_q.answer("هـذا كـل شـي !", alert=True)
        await c_q.answer()
        front_vid = search_data.get(str(index))
        await c_q.edit(
            text=front_vid.get("message"),
            file=await get_ytthumb(front_vid.get("video_id")),
            buttons=yt_search_btns(
                data_key=data_key,
                page=index,
                vid=front_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "listall":
        await c_q.answer("المشـاهـدات تغيـرت لـ:  📜  قائمـة", alert=False)
        list_res = "".join(
            search_data.get(vid_s).get("list_view") for vid_s in search_data
        )

        telegraph = await post_to_telegraph(
            f"Showing {total} youtube video results for the given query ...",
            list_res,
        )
        await c_q.edit(
            file=await get_ytthumb(search_data.get("1").get("video_id")),
            buttons=[
                (
                    Button.url(
                        "↗️  اضـغـط للـرؤيـة",
                        url=telegraph,
                    )
                ),
                (
                    Button.inline(
                        "📰  عـرض مـفصـل",
                        data=f"ytdl_detail_{data_key}_{page}",
                    )
                ),
            ],
        )
    else:  # Detailed
        index = 1
        await c_q.answer("المشـاهـدات تغيـرت لـ:  📰  مفـصل ", alert=False)
        first = search_data.get(str(index))
        await c_q.edit(
            text=first.get("message"),
            file=await get_ytthumb(first.get("video_id")),
            buttons=yt_search_btns(
                del_back=True,
                data_key=data_key,
                page=index,
                vid=first.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
