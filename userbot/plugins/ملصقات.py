import asyncio
import base64
import io
import math
import random
import re
import string
import urllib.request
from os import remove

import cloudscraper
import emoji as catemoji
from bs4 import BeautifulSoup as bs
from PIL import Image
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from userbot import jmthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import crop_and_divide
from ..helpers.tools import media_type
from ..helpers.utils import _cattools
from ..sql_helper.globals import gvarstatus

plugin_category = "fun"

# modified and developed by @jmthon


combot_stickers_url = "https://combot.org/telegram/stickers?q="

EMOJI_SEN = [
    "Можно отправить несколько смайлов в одном сообщении, однако мы рекомендуем использовать не больше одного или двух на каждый стикер.",
    "You can list several emoji in one message, but I recommend using no more than two per sticker",
    "Du kannst auch mehrere Emoji eingeben, ich empfehle dir aber nicht mehr als zwei pro Sticker zu benutzen.",
    "Você pode listar vários emojis em uma mensagem, mas recomendo não usar mais do que dois por cada sticker.",
    "Puoi elencare diverse emoji in un singolo messaggio, ma ti consiglio di non usarne più di due per sticker.",
    "emoji",
]

KANGING_STR = [
    "**⌯︙انتظر يتم صنع الملصق*",
]

def verify_cond(catarray, text):
    return any(i in text for i in catarray)


def pack_name(userid, pack, is_anim):
    if is_anim:
        return f"JMTHONBOT_{userid}_{pack}_anim"
    return f"JMTHON_{userid}_{pack}"


def char_is_emoji(character):
    return character in catemoji.UNICODE_EMOJI["en"]


def pack_nick(username, pack, is_anim):
    if gvarstatus("CUSTOM_STICKER_PACKNAME"):
        if is_anim:
            packnick = f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack} (Animated)"
        else:
            packnick = f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack}"
    elif is_anim:
        packnick = f"@{username} Vol.{pack} (Animated)"
    else:
        packnick = f"@{username} Vol.{pack}"
    return packnick


async def resize_photo(photo):
    """Resize the given photo to 512x512"""
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


async def newpacksticker(
    catevent,
    conv,
    cmd,
    args,
    pack,
    packnick,
    stfile,
    emoji,
    packname,
    is_anim,
    otherpack=False,
    pkang=False,
):
    await conv.send_message(cmd)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packnick)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await catevent.edit(
            f"فشل اضافة الملصق ، استخدم بوت الملصقات @Stickers لأضافة الملصق يدويا.\n**خطأ :**{rsp}"
        )
        return
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/publish")
    if is_anim:
        await conv.get_response()
        await conv.send_message(f"<{packnick}>")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("/skip")
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message(packname)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return otherpack, packname, emoji
    return pack, packname


async def add_to_pack(
    catevent,
    conv,
    args,
    packname,
    pack,
    userid,
    username,
    is_anim,
    stfile,
    emoji,
    cmd,
    pkang=False,
):
    await conv.send_message("/addsticker")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    x = await conv.get_response()
    while ("50" in x.text) or ("120" in x.text):
        try:
            val = int(pack)
            pack = val + 1
        except ValueError:
            pack = 1
        packname = pack_name(userid, pack, is_anim)
        packnick = pack_nick(username, pack, is_anim)
        await catevent.edit(
            f"** تبديل الحـزمة الى {str(pack)} بسبب امتلاء الحزمة"
        )
        await conv.send_message(packname)
        x = await conv.get_response()
        if x.text == "**الحـزمة المحددة غير صحيحة**":
            return await newpacksticker(
                catevent,
                conv,
                cmd,
                args,
                pack,
                packnick,
                stfile,
                emoji,
                packname,
                is_anim,
                otherpack=True,
                pkang=pkang,
            )
    if is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await catevent.edit(
            f"⌯︙فشل اضافة الملصق ، استخدم بوت الملصقات @Stickers لأضافة الملصق يدويا.\n**خطأ :**{rsp}"
        )
        return
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/done")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return packname, emoji
    return pack, packname


@jmthon.ar_cmd(
    pattern="ملصق(?:\s|$)([\s\S]*)",
    command=("ملصق", plugin_category),
    info={
        "header": "To kang a sticker.",
        "description": "Kang's the sticker/image to the specified pack and uses the emoji('s) you picked",
        "usage": "{tr}kang [emoji('s)] [number]",
    },
)
async def kang(args):  # sourcery no-metrics
    "To kang a sticker."
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None
    message = await args.get_reply_message()
    user = await args.client.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"cat_{user.id}"
    else:
        username = user.username
    userid = user.id
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await args.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await args.client.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            await args.client.download_file(
                message.media.document, "AnimatedSticker.tgs"
            )

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await edit_delete(args, "⌯︙الملف غير مدعوم")
            return
    else:
        await edit_delete(args, "⌯︙لايمكنني اخذ هاذا")
        return
    if photo:
        splat = ("".join(args.text.split(maxsplit=1)[1:])).split()
        emoji = emoji if emojibypass else "♥"
        pack = 1
        if len(splat) == 2:
            if char_is_emoji(splat[0][0]):
                if char_is_emoji(splat[1][0]):
                    return await catevent.edit("-")
                pack = splat[1]  # User sent both
                emoji = splat[0]
            elif char_is_emoji(splat[1][0]):
                pack = splat[0]  # User sent both
                emoji = splat[1]
            else:
                return await catevent.edit("-")
        elif len(splat) == 1:
            if char_is_emoji(splat[0][0]):
                emoji = splat[0]
            else:
                pack = splat[0]
        packnick = pack_nick(username, pack, is_anim)
        packname = pack_name(userid, pack, is_anim)
        cmd = "/newpack"
        stfile = io.BytesIO()
        if is_anim:
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            stfile.name = "sticker.png"
            image.save(stfile, "PNG")
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with args.client.conversation("Stickers") as conv:
                packname, emoji = await add_to_pack(
                    catevent,
                    conv,
                    args,
                    packname,
                    pack,
                    userid,
                    username,
                    is_anim,
                    stfile,
                    emoji,
                    cmd,
                )
            await edit_delete(
                catevent,
                f"تـم اخذ الملصق بنـجاح\
                    \n ⌯︙حزمة ملصقاتك هنا  [اضغط هنا](t.me/addstickers/{packname}) *",
                parse_mode="md",
                time=10,
            )
        else:
            await catevent.edit("**- يتم احضار حزمة جديدة ⌔︙**")
            async with args.client.conversation("Stickers") as conv:
                otherpack, packname, emoji = await newpacksticker(
                    catevent,
                    conv,
                    cmd,
                    args,
                    pack,
                    packnick,
                    stfile,
                    emoji,
                    packname,
                    is_anim,
                )
            if otherpack:
                await edit_delete(
                    catevent,
                    f"⌯︙تم صنع الملصق لحزمه مختلفه !\
                    \n⌯︙والحزمة التي تم إنشاؤها حديثًا هي` [اضغط هنا](t.me/addstickers/{packname}) `  استخدم  {emoji}` للعثور على الملصقات المصنوعه",
                    parse_mode="md",
                    time=10,
                )
            else:
                await edit_delete(
                    catevent,
                    f"** تم اخذ الملصق بنجاح ♥!\
                    \nالحزمة الخاص بك هي [اضغط هنا](t.me/addstickers/{packname})  السمايل المستخدم هو {emoji}`",
                    parse_mode="md",
                    time=10,
                )


@jmthon.ar_cmd(
    pattern="حزمة(?:\s|$)([\s\S]*)",
    command=("حزمة", plugin_category),
    info={
        "header": "To kang entire sticker sticker.",
        "description": "Kang's the entire sticker pack of replied sticker to the specified pack",
        "usage": "{tr}pkang [number]",
    },
)
async def pack_kang(event):  # sourcery no-metrics
    "To kang entire sticker sticker."
    user = await event.client.get_me()
    if user.username:
        username = user.username
    else:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"cat_{user.id}"
    photo = None
    userid = user.id
    is_anim = False
    emoji = None
    reply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await edit_delete(
            event, "**⌯︙يجب الرد على الملصق لإرسال جميع الملصقات في تلك الحزمة**"
        )
    try:
        stickerset_attr = reply.document.attributes[1]
        catevent = await edit_or_reply(
            event, "**يتم إحضار تفاصيل حزمة الملصقات ، انتظر**"
        )
    except BaseException:
        return await edit_delete(
            event, "هاذا ليس ملصق قم بالرد ع الملصق ⌔︙", 5
        )
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await edit_delete(
            catevent,
            "أعتقد أن هذا الملصق ليس من أي حزمة. لذا ، لا أستطيع أخذ هذا الملصق الى",
        )
    kangst = 1
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    noofst = get_stickerset.set.count
    blablapacks = []
    blablapacknames = []
    pack = None
    for message in reqd_sticker_set.documents:
        if "image" in message.mime_type.split("/"):
            await edit_or_reply(
                catevent,
                f"**جاري اخذ حزمة الملصقات هذه . عملية الاستنساخ هي** : {kangst}/{noofst}",
            )
            photo = io.BytesIO()
            await event.client.download_file(message, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.attributes
            ):
                emoji = message.attributes[1].alt
        elif "tgsticker" in message.mime_type:
            await edit_or_reply(
                catevent,
                f"**جاري اخذ حزمة الملصقات هذه . عملية الاستنساخ هي** : {kangst}/{noofst}",
            )
            await event.client.download_file(message, "AnimatedSticker.tgs")
            attributes = message.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            is_anim = True
            photo = 1
        else:
            await edit_delete(catevent, "** الملف غير مدعوم**")
            return
        if photo:
            splat = ("".join(event.text.split(maxsplit=1)[1:])).split()
            emoji = emoji or "🖤"
            if pack is None:
                pack = 1
                if len(splat) == 1:
                    pack = splat[0]
                elif len(splat) > 1:
                    return await edit_delete(
                        catevent,
                        "**𖥻 عذرا لا يمكن استخدام الاسم المعطى للحزمة أو لا توجد حزمة بهذا الاسم**",
                    )
            try:
                cat = Get(cat)
                await event.client(cat)
            except BaseException:
                pass
            packnick = pack_nick(username, pack, is_anim)
            packname = pack_name(userid, pack, is_anim)
            cmd = "/newpack"
            stfile = io.BytesIO()
            if is_anim:
                cmd = "/newanimated"
            else:
                image = await resize_photo(photo)
                stfile.name = "sticker.png"
                image.save(stfile, "PNG")
            response = urllib.request.urlopen(
                urllib.request.Request(f"http://t.me/addstickers/{packname}")
            )
            htmlstr = response.read().decode("utf8").split("\n")
            if (
                "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
                in htmlstr
            ):
                async with event.client.conversation("Stickers") as conv:
                    pack, catpackname = await newpacksticker(
                        catevent,
                        conv,
                        cmd,
                        event,
                        pack,
                        packnick,
                        stfile,
                        emoji,
                        packname,
                        is_anim,
                        pkang=True,
                    )
            else:
                async with event.client.conversation("Stickers") as conv:
                    pack, catpackname = await add_to_pack(
                        catevent,
                        conv,
                        event,
                        packname,
                        pack,
                        userid,
                        username,
                        is_anim,
                        stfile,
                        emoji,
                        cmd,
                        pkang=True,
                    )
            if catpackname not in blablapacks:
                blablapacks.append(catpackname)
                blablapacknames.append(pack)
        kangst += 1
        await asyncio.sleep(2)
    result = "** حزمة هذا الملصق تم اخذها لحزمت ملصقاتك التالية **:`\n"
    for i in enumerate(blablapacks):
        result += (
            f"  •  [pack {blablapacknames[i[0]]}](t.me/addstickers/{blablapacks[i[0]]})"
        )
    await catevent.edit(result)

@jmthon.ar_cmd(
    pattern="معلومات_الملصق$",
    command=("معلومات_الملصق", plugin_category),
    info={
        "header": "To get information about a sticker pick.",
        "description": "Gets info about the sticker packk",
        "usage": "{tr}stkrinfo",
    },
)
async def get_pack_info(event):
    "To get information about a sticker pick."
    if not event.is_reply:
        return await edit_delete(
            event, "`لا أستطيع إحضار المعلومات من لا شيء ، هل يمكنني ذلك ؟!`", 5
        )
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await edit_delete(
            event, "**⌯︙هاذا ليس ملصق يجب الرد على الملصق اولا**", 5
        )
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        catevent = await edit_or_reply(
            event, "**⌯︙إحضار تفاصيل حزمة الملصقات ، يُرجى الانتظار**`"
        )
    except BaseException:
        return await edit_delete(
            event, "**⌯︙هذا ليس ملصق يجب الرد على الملصق اولا**", 5
        )     
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await catevent.edit("**⌯︙هذا ليس ملصق يجب الرد على الملصق اولا.**")
    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = (
        f"**⌯︙عنوان الملصق:** `{get_stickerset.set.title}\n`"
        f"**⌯︙الاسم القصير للملصق:** `{get_stickerset.set.short_name}`\n"
        f"**⌯︙المـسؤل:** `{get_stickerset.set.official}`\n"
        f"**⌯︙الارشيف:** `{get_stickerset.set.archived}`\n"
        f"**⌯︙حزمة الملصق:** `{get_stickerset.set.count}`\n"
        f"**⌯︙الايموجي المستخدم:**\n{' '.join(pack_emojis)}"
    )
    await catevent.edit(OUTPUT)
