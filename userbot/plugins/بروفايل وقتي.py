# Copyright (C) 2021 JMTHON TEAM
# FILES WRITTEN BY  @RRRD7

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

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import (
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    _catutils,
    jmthon,
    edit_delete,
    logging,
)
DEFAULTUSERBIO = DEFAULT_BIO or "أستغفر اللّه"
CHANGE_TIME = Config.CHANGE_TIME
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC
RRRD7 = gvarstatus("TIME_JM") or " "
#كتابة فريق جمثون  على التليكرام

@bot.on(admin_cmd(pattern="الحدث ?(.*)"))
async def autopic(event):
    if event.fwd_from:
        return
    if Config.DEFAULT_PIC is None:
        return await edit_delete(
            event,
            "⌔︙ عـذرا هنـاك خطـ\n وظيفة الصورة التـلقائيـة تحتاج إلى ضبط فار DEFAULT PIC  في هيـروكو",
            parse_mode=parse_pre,
        )
    downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:  
            input_str = int(input_str)
        except ValueError:
            input_str = 60
    else:
        if gvarstatus("autopic_counter") is None:
            addgvar("autopic_counter", 30)
    if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
        return await edit_delete(event, f"⌔︙ الـصورة الـوقتيـة مفـعلة بالأصل")
    addgvar("autopic", True)
    if input_str:
        addgvar("autopic_counter", input_str)
    await edit_delete(event, f"⌔︙ تـم  تفـعيل الصـورة الوقتيـة بنجـاح ✅♥")
    await autopicloop()


@bot.on(admin_cmd(pattern="الصورة الوقتية$"))
async def main(event):
    if event.fwd_from:
        return
    if Config.DIGITAL_PIC is None:
        return await edit_delete(
            event,
            "⌔︙ عـذرا هنـاك خطـأ\n وظيفة الصورة التـلقائيـة تحتاج إلى ضبط DIGITAL_PIC var في Heroku vars",
            parse_mode=parse_pre,
        )
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, f"⌔︙ الـصورة الـوقتيـة مفـعلة بالأص")
    addgvar("digitalpic", True)
    await edit_delete(event, f"⌔︙ تـم  تفـعيل الصـورة الوقتيـة بنجـاح ✅")
    await digitalpicloop()


@bot.on(admin_cmd(pattern="اسم وقتي$"))
async def _(event):
    if event.fwd_from:
        return
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_delete(event, f"⌔︙ الاسم الوقتي بالفعل مفعل ❕")
    addgvar("autoname", True)
    await edit_delete(event, "⌔︙ تم تفعيل الاسم الوقتي بنجاح ✅")
    await autoname_loop()


@bot.on(admin_cmd(pattern="بايو وقتي$"))
async def _(event):
    if event.fwd_from:
        return
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, f"⌔︙  البايو الوقتي بالفعل مُمكـن ❕")
    addgvar("autobio", True)
    await edit_delete(event, "⌔︙   تم تفعيل البايو الوقتي بنـجاح ✅")
    await autobio_loop()


@bot.on(admin_cmd(pattern="انهاء (.*)"))
async def _(event):  # sourcery no-metrics
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "الحدث":
        if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
            delgvar("autopic")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "**- **")
        return await edit_delete(event, "** - **")
    if input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await jmthon.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "⌔︙  تم ايقاف الصـورة الوقـتيـة بنـجاح ✅")
        return await edit_delete(event, "⌔︙  لم يتم تمكين  الصـورة الوقـتيـة")
    if input_str == "bloom":
        if gvarstatus("bloom") is not None and gvarstatus("bloom") == "true":
            delgvar("bloom")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "`Bloom has been stopped now`")
        return await edit_delete(event, "`Bloom haven't enabled`")
    if input_str == "اسم وقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "⌔︙ تم ايقاف  الاسم الوقتي بنـجاح ✅")
        return await edit_delete(event, "⌔︙ لم يتم تفعيل الاسم الوقتي بالأصل")
    if input_str == "بايو وقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "⌔︙  تم ايقاف الباية الوقـتي بنـجاح ✅")
        return await edit_delete(event, "⌔︙  لم يتم تفعيل البايو الوقتي ")


async def autopicloop():
    AUTOPICSTART = gvarstatus("autopic") == "true"
    if AUTOPICSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await jmthon.send_message(
                BOTLOG_CHATID,
                "⌔︙ خطأ  \ n` لتفعيل autopic ، تحتاج إلى تعيين DEFAULT_PIC var في Heroku vars`",
            )
        return
    if gvarstatus("autopic") is not None:
        try:
            counter = int(gvarstatus("autopic_counter"))
        except Exception as e:
            LOGS.warn(str(e))
    while AUTOPICSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(autopic_path, autophoto_path)
        im = Image.open(autophoto_path)
        current_time = datetime.now().strftime("  %I:%M ")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 70)
        drawn_text.text((300, 400), current_time, font=fnt, fill=(450, 350, 0))
        img.save(autophoto_path)
        file = await jmthon.upload_file(autophoto_path)
        try:
            await jmthon(functions.photos.DeletePhotosRequest(await jmthon.get_profile_photos("me", limit=1)))
            await jmthon(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            counter += counter
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        AUTOPICSTART = gvarstatus("autopic") == "true"


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
        current_time = datetime.now().strftime("  %I:%M ")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        cat = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9QYXliQWNrLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(cat, 70)
        drawn_text.text((300, 400), current_time, font=fnt, fill=(450, 350, 0))
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
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def bloom_pfploop():
    BLOOMSTART = gvarstatus("bloom") == "true"
    if BLOOMSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await jmthon.send_message(
                BOTLOG_CHATID,
                "⌔︙ Error\n`For functing of bloom you need to set DEFAULT_PIC var in Heroku vars`",
            )
        return
    while BLOOMSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        # RIP Danger zone Here no editing here plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        shutil.copy(autopic_path, autophoto_path)
        image = Image.open(autophoto_path)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(autophoto_path)
        current_time = datetime.now().strftime("\n   %I:%M:%S")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), " ", font=ofnt, fill=(FR, FG, FB))
        img.save(autophoto_path)
        file = await jmthon.upload_file(autophoto_path)
        try:
            await jmthon(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        BLOOMSTART = gvarstatus("bloom") == "true"


async def autoname_loop():
    AUTONAMESTART = gvarstatus("autoname") == "true"
    while AUTONAMESTART:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%I:%M")
        name = f"{RRRD7} {HM} "
        LOGS.info(name)
        try:
            await jmthon(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        DMY = time.strftime("%Y.%m.%d")
        HM = time.strftime("%I:%M")
        bio = f" {DEFAULTUSERBIO} 𓆩{HM}𓆪"
        LOGS.info(bio)
        try:
            await jmthon(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


bot.loop.create_task(autopicloop())
bot.loop.create_task(digitalpicloop())
bot.loop.create_task(bloom_pfploop())
bot.loop.create_task(autoname_loop())
bot.loop.create_task(autobio_loop())
