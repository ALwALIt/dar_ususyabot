# اذا تخمط اذكر الحقوق رجـاءا  - 
# كتابة وتعديل وترتيب  ~ @RR9R7
# For ~ @Jmthon

import asyncio
import base64
import os
import random
import re
import shutil
import time
import urllib
from datetime import datetime

import requests
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions
from urlextract import URLExtract

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.global_list import (
    add_to_list,
    get_collection_list,
    is_in_list,
    rm_from_list,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    _catutils,
    jmthon,
    edit_delete,
    logging,
)

plugin_category = "tools"

LOGS = logging.getLogger(__name__)

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/63a826d5e5f0003e006a0.jpg"


async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        roz = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9QYXliQWNrLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(roz, 65)
        drawn_text.text((300, 400), current_time, font=fnt, fill=(280, 280, 280))
        img.save(autophoto_path)
        file = await jmthon.upload_file(autophoto_path)
        try:
            if i > 0:
                await jmthon(
                    functions.photos.DeletePhotosRequest(
                        await jmthon.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await jmthon(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


@jmthon.ar_cmd(
    pattern="الصورة الوقتية$",
    command=("الصورة الوقتية", plugin_category),)
async def _(event):
    "To set random colour pic with time to profile pic"
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "**الصـورة الـوقتية شغـالة بالأصـل 🧸♥**")
    addgvar("digitalpic", True)
    await edit_delete(event, "**تم تفـعيل الصـورة الـوقتية بنجـاح ✅**")
    await digitalpicloop()



jmthon.loop.create_task(digitalpicloop())
