#Copyright  By  @JepThon  © 2021
#WRITE BY  @RR9R7 - @GGGNE

import asyncio
import base64
import io
import logging
import os
import time
from datetime import datetime
from io import BytesIO
from shutil import copyfile

import fitz
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pymediainfo import MediaInfo
from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.messages import SendMediaRequest
from telethon.utils import get_attributes

from userbot import jmthon

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, progress, thumb_from_audio
from ..helpers.functions import (
    convert_toimage,
    convert_tosticker,
    invert_frames,
    l_frames,
    r_frames,
    spin_frames,
    ud_frames,
    vid_to_gif,
)
from ..helpers.utils import _cattools, _catutils, _format, parse_pre, reply_id
from . import make_gif

plugin_category = "misc"


if not os.path.isdir("./temp"):
    os.makedirs("./temp")


LOGS = logging.getLogger(__name__)
PATH = os.path.join("./temp", "temp_vid.mp4")

thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

#Copyright  By  @JepThon  © 2021
#WRITE BY  @RR7PP  

@jmthon.ar_cmd(
    pattern="تحويل صورة$",
    command=("تحويل صورة", plugin_category),
    info={
        "header": "Reply this command to a sticker to get image.",
        "description": "This also converts every media to image. that is if video then extracts image from that video.if audio then extracts thumb.",
        "usage": "{tr}stoi",
    },
)
async def _(event):
    "Sticker to image Conversion."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event, "⌯︙يجـب عليـك الرد عـلى الملصق لتحويـله الـى صورة ⚠️"
        )
    output = await _cattools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "⌯︙غـير قـادر على تحويل الملصق إلى صورة من هـذا الـرد ⚠️"
        )
    meme_file = convert_toimage(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()


@jmthon.ar_cmd(
    pattern="تحويل ملصق$",
    command=("تحويل ملصق", plugin_category),
    info={
        "header": "Reply this command to image to get sticker.",
        "description": "This also converts every media to sticker. that is if video then extracts image from that video. if audio then extracts thumb.",
        "usage": "{tr}itos",
    },
)
async def _(event):
    "Image to Sticker Conversion."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event, "⌯︙يجـب عليـك الرد عـلى الصـورة لتحويـلها الـى مـلصق ⚠️"
        )
    output = await _cattools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "⌯︙غـير قـادر على استـخراج الـملصق من هـذا الـرد ⚠️"
        )
    meme_file = convert_tosticker(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()

@jmthon.ar_cmd(
    pattern="تحويل (mp3|voice)$",
    command=("تحويل", plugin_category),
    info={
        "header": "Converts the required media file to voice or mp3 file.",
        "usage": [
            "{tr}تحويل بصمة",
            "{tr}تحويل بصمة",
        ],
    },
)
async def _(event):
    "Converts the required media file to voice or mp3 file."
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "**⌯︙يـجب الـرد على اي مـلف اولا ⚠️**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "**⌯︙يـجب الـرد على اي مـلف اولا ⚠️**")
        return
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "⌯︙يتـم التـحويل انتـظر قليـلا ⏱")
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "⌯︙التحـميل الى `{}` في {} من الثواني ⏱".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "voice_" + str(round(time.time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "mp3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("⌯︙غـير مدعوم ❕")
            os.remove(downloaded_file_name)
            return
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()
            
#Copyright  By  @JepThon  © 2021
#WRITE BY  @RR7PP

@jmthon.ar_cmd(
    pattern="تحويل متحركة ?([0-9.]+)?$",
    command=("تحويل متحركة", plugin_category),
    info={
        "header": "Reply this command to a video to convert it to gif.",
        "description": "By default speed will be 1x",
        "usage": "{tr}vtog <speed>",
    },
)
async def _(event):
    "Reply this command to a video to convert it to gif."
    reply = await event.get_reply_message()
    mediatype = media_type(event)
    if mediatype and mediatype != "video":
        return await edit_delete(event, "⌯︙يجـب عليك الـرد على فيديو اولا لتحـويله ⚠️")
    args = event.pattern_match.group(1)
    if not args:
        args = 2.0
    else:
        try:
            args = float(args)
        except ValueError:
            args = 2.0
    catevent = await edit_or_reply(event, "**⌯︙يتـم التحويل الى متـحركه انتـظر ⏱**")
    inputfile = await reply.download_media()
    outputfile = os.path.join(Config.TEMP_DIR, "vidtogif.gif")
    result = await vid_to_gif(inputfile, outputfile, speed=args)
    if result is None:
        return await edit_delete(event, "**⌯︙عـذرا لا يمكـنني تحويل هذا الى متـحركة ⚠️**")
    jasme = await event.client.send_file(event.chat_id, result, reply_to=reply)
    await _catutils.unsavegif(event, jasme)
    await catevent.delete()
    for i in [inputfile, outputfile]:
        if os.path.exists(i):
            os.remove(i)
