import asyncio
import random
import re
import shutil
import urllib
import base64
import requests
import time
import os
import html
import telethon.password as pwd_mod
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.events import CallbackQuery
from telethon.errors import FloodWaitError
from telethon.tl import functions
from urlextract import URLExtract
from requests import get
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id, get_input_location
from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.utils import get_display_name
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User
from userbot import jmthon
from userbot.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from . import ALIVE_NAME, AUTONAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO, get_user_from_event
from ..helpers import get_user_from_event, reply_id
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..sql_helper.global_list import add_to_list, get_collection_list, is_in_list, rm_from_list
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import AUTONAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO, _catutils, edit_delete, jmthon, logging, spamwatch
    
def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"{full_name}"

def user_full_name(user):
    names = [user.first_name]
    names = [i for i in list(names) if i]
    return " ".join(names)

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = (
    str(DEFAULT_BIO)
    if DEFAULT_BIO
    else "الحمد الله على كل شئ  ⌔︙ @jepthon"
)

STAT_INDICATION = "**⌔︙ جـاري جـمـع الإحصـائيـات ، انتـظـر 🔄**"
CHANNELS_STR = "**⌔︙ قائمة القنوات التي أنت فيها موجودة هنا\n\n"
CHANNELS_ADMINSTR = "**⌔︙قائمة القنوات التي تديرها هنا **\n\n"
CHANNELS_OWNERSTR = "**⌔︙قائمة القنوات التي تمتلك فيها هنا **\n\n"
GROUPS_STR = "**⌔︙قائمة المجموعات التي أنت فيها موجود هنا **\n\n"
GROUPS_ADMINSTR = "**⌔︙قائمة المجموعات التي تكون مسؤولاً فيها هنا **\n\n"
GROUPS_OWNERSTR = "**⌔︙قائمة المجموعات التي تمتلك فيها هنا **\n\n"
INVALID_MEDIA = "**⌔︙إمتداد هذه الصورة غير صالح  ❌**"
PP_CHANGED = "**⌔︙تم تغير صورة حسابك بنجاح  ✅**"
PP_TOO_SMOL = "**⌔︙هذه الصورة صغيرة جدًا قم بإختيار صورة أخرى  ⚠️**"
PP_ERROR = "**⌔︙حدث خطأ أثناء معالجة الصورة  ⚠️**"
BIO_SUCCESS = "**⌔︙تم تغيير بايو حسابك بنجاح  ✅**"
FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")
JEPTHON = Config.TIME_JP or "•"
digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/6b5db91f38e919e386168.jpg"
NAME_OK = "**⌔︙تم تغيير اسم حسابك بنجاح  ✅**"
USERNAME_SUCCESS = "**⌔︙تم تغيير معرّف حسابك بنجاح  ✅**"
USERNAME_TAKEN = "**⌔︙هذا المعرّف مستخدم  ❌**"
plugin_category = "tools"
DEFAULTUSERBIO = DEFAULT_BIO or "الحـمـد الله دائـمآ وأبـدآ"
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)
COLLECTION_STRINGS = {
    "batmanpfp_strings": [
        "awesome-batman-wallpapers",
        "batman-arkham-knight-4k-wallpaper",
        "batman-hd-wallpapers-1080p",
        "the-joker-hd-wallpaper",
        "dark-knight-joker-wallpaper",
    ],
    "thorpfp_strings": [
        "thor-wallpapers",
        "thor-wallpaper",
        "thor-iphone-wallpaper",
        "thor-wallpaper-hd",
    ],
}

@jmthon.on(admin_cmd(pattern="احصائيات حسابي(?: |$)(.*)"))
async def stats(event):  # sourcery no-metrics
    "To get statistics of your telegram account."
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"📌 **• ⚜️ |  احصائيات حسـابك العـامة لـ {full_name} 📊** \n"
    response += f"**⌔︙الدردشات الخاصة 🏷️  :** {private_chats} \n"
    response += f"**⌔︙ الاشـخاص 🚹 : {private_chats - bots}` \n"
    response += f"**⌔︙ الـبوتـات 🤖 : {bots}` **\n"
    response += f"**⌔︙ عـدد المجـموعـات 🚻 :** `{groups}` \n"
    response += f"**⌔︙ عـدد القنـوات  🚻 :** `{broadcast_channels}` \n"
    response += f"**⌔︙ عـدد المجـموعات التـي تكـون فيها ادمـن  🛂 :** `{admin_in_groups}` \n"
    response += f"**⌔︙ عـدد المجموعات التـي أنـشأتـها  🛃** : `{creator_in_groups}` \n"
    response += f"**⌔︙ عـدد القنوات التـي تكـون فيها ادمـن 📶 : `{admin_in_broadcast_channels}` **\n"
    response += (
        f"**⌔︙ حقوق المسؤول في القنوات  🛂 : `{admin_in_broadcast_channels - creator_in_channels}` **\n"
    )
    response += f"**عـدد المحـادثـات الغيـر مقـروء 📄 :** {unread} \n"
    response += f"**عـدد الـتاكـات الغيـر مقـروء 📌 :** {unread_mentions} \n"
    response += f"**⌔︙ استغرق الأمر  🔍  :** `{stop_time:.02f}` ثانيه \n"
    await cat.edit(response)

@jmthon.on(admin_cmd(pattern="قائمه (جميع القنوات|قنوات اديرها|قنوات امتلكها)$"))
async def stats(event):  
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    if catcmd == "جميع القنوات":
        output = CHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_STR
    elif catcmd == "قنوات اديرها":
        output = CHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_ADMINSTR
    elif catcmd == "قنوات امتلكها":
        output = CHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**استغرق حساب القنوات : ** {stop_time:.02f} ثانيه"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )


@jmthon.on(admin_cmd(pattern="قائمه (جميع المجموعات|مجموعات اديرها|مجموعات امتلكها)$"))
async def stats(event):  # sourcery no-metrics
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if catcmd == "جميع المجموعات":
        output = GROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_STR
    elif catcmd == "مجموعات اديرها":
        output = GROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_ADMINSTR
    elif catcmd == "مجموعات امتلكها":
        output = GROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**استغرق حساب المجموعات : ** {stop_time:.02f} ثانيه"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )

@jmthon.on(admin_cmd(pattern="(الايدي|id)(?: |$)(.*)"))
async def _(event):
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{str(e)}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"**⌔︙ آيـدي المُستخدم 💠 :** `{input_str}` هـو `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"**⌔︙ آيـدي الدردشــــة 💠 :** `{p.title}` هـو `{p.id}` "
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⌔︙ قُم بإدخال أسم مُستخدم أو الرد على المُستخدم ⚜️**")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**⌔︙ آيـدي الدردشــــة  💠 : **`{str(event.chat_id)}` \n**⌔︙ آيـدي المُستخدم  💠 : **`{str(r_msg.sender_id)}` \n**⌔︙آيـدي الميديـا  🆔 : **`{bot_api_file_id}`",
            )
        else:
            await edit_or_reply(
                event,
                f"**⌔︙ آيـدي الدردشــــة  💠 : **`{str(event.chat_id)}` 𖥻\n**⌔︙ آيـدي المُستخدم  💠 : **`{str(r_msg.sender_id)}` ",
            )

@jmthon.on(admin_cmd(pattern="وضع بايو(?: |$)(.*)"))
async def _(event):
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await edit_delete(event, "**⌔︙تم تغيير البايو بنجاح  ✅**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")


@jmthon.on(admin_cmd(pattern="وضع اسم(?: |$)(.*)"))
async def _(event):
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split("|", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await edit_delete(event, "**⌔︙تم تغيير الاسم بنجاح  ✅**")
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")

@jmthon.on(admin_cmd(pattern="وضع صوره(?: |$)(.*)"))
async def _(event):
    reply_message = await event.get_reply_message()
    catevent = await edit_or_reply(
        event, "**...**"
    )
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await catevent.edit(str(e))
    else:
        if photo:
            await catevent.edit("**⌔︙ أشترك @IQTHON **")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = os.stat(photo).st_size
                if size > 2097152:
                    await catevent.edit("**⌔︙ يجب ان يكون الحجم اقل من 2 ميغا ✅**")
                    os.remove(photo)
                    return
                catpic = None
                catvideo = await event.client.upload_file(photo)
            else:
                catpic = await event.client.upload_file(photo)
                catvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=catpic, video=catvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await catevent.edit(f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")
            else:
                await edit_or_reply(
                    catevent, "**⌔︙ تم تغيير الصورة بنجاح ✅**"
                )
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.info(str(e))
async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("تجديد الصوره") == "true"
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
        cat = str(base64.b64decode("dXNlcmJvdC9zcWxfaGVscGVyL0lRVEhPTklNT0dFLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(cat, 60)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await iqthon.upload_file(autophoto_path)
        try:
            if i > 0:
                await jmthon(
                    functions.photos.DeletePhotosRequest(
                        await jmthon.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await iqthon(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("تجديد الصوره") == "true"
@jmthon.on(admin_cmd(pattern="وضع معرف(?: |$)(.*)"))
async def update_username(username):
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await edit_delete(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await edit_or_reply(event, USERNAME_TAKEN)
    except Exception as e:
        await edit_or_reply(event, f"**⌔︙خطأ  ⚠️ :**\n`{str(e)}`")

@jmthon.on(admin_cmd(pattern="معرفاتي(?: |$)(.*)"))
async def _(event):
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "**⌔︙جميع القنوات والمجموعات التي قمت بإنشائها  💠  :**\n"
    output_str += "".join(f"⌔︙  - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats)
    await edit_or_reply(event, output_str)

@jmthon.on(admin_cmd(pattern="تحويل ملكيه ([\s\S]*)"))
async def _(event):
    user_name = event.pattern_match.group(1)
    try:
        pwd = await event.client(functions.account.GetPasswordRequest())
        my_srp_password = pwd_mod.compute_check(pwd, Config.TG_2STEP_VERIFICATION_CODE)
        await event.client(
            functions.channels.EditCreatorRequest(
                channel=event.chat_id, user_id=user_name, password=my_srp_password
            )
        )
    except Exception as e:
        await event.edit(f"**⌔︙حـدث خـطأ ✕ :**\n`{str(e)}`")
    else:
        await event.edit("**⌔︙تم نقل ملكيه ✓**")

@jmthon.on(admin_cmd(pattern="انتحال(?: |$)(.*)"))
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await event.client.upload_file(profile_pic)
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await edit_delete(event, "**⌔︙ تـم إنتحـال الحسـاب بنجـاح  ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**⌔︙الإنتحـال 🃏 :** \n **✓ تـم إنتحـال الحسـاب بنجـاح :**  [{first_name}](tg://user?id={user_id })",
        )
async def autobio_loop():
    AUTOBIOSTART = gvarstatus("نبذه وقتيه") == "true"
    while AUTOBIOSTART:
        HM = time.strftime("%I:%M")
        go = requests.get(f"https://telethon.ml/DontTag.php?text={HM}").json()['newText']
        bio = f"{EMOJI_TELETHON} {DEFAULTUSERBIO}  - {go}"
        LOGS.info(bio)
        try:
            await iqthon(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("نبذه وقتيه") == "true"
@jmthon.on(admin_cmd(pattern="الغاء الانتحال(?: |$)(.*)"))
async def _(event):
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=blank))
    await edit_delete(event, "**⌔︙تمّـت إعـادة حسـابك بنجـاح ✓**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"⌔︙ **الأعـادة ♲ :**\n**⌔︙ تـم إعـادة ضبـط حسـابك إلـى وضعـه الطبيـعي بـنجاح ✓**"
        )

async def fetch_info(replied_user, event):
    """jmthon"""
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "`لم يقم المستخدم بتعيين صورة الملف الشخصي`"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "`تعذر جلب معرف DC`"
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(
        user_id,
        Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
        download_big=True,
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("`هذا المستخدم ليس له اسم`")
    )
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    username = "@{}".format(username) if username else ("`هذا الشخص لايوجد لديه معرف`")
    user_bio = "`هذا الشخص لايوجد لديه نــبــذة`" if not user_bio else user_bio
    caption = "<b>• ⚜️ | مــعــلــومــات الــمــســتــخــدم :</b>\n"
    caption += f"<b>• ⚜️ | الاســم  :  </b> `{first_name} {last_name}`\n"
    caption += f"<b>• ⚜️ | الــمــ؏ــࢪفہ  : </b> {username}\n"
    caption += f"<b>• ⚜️ | الايــديہ  :  </b> <code>{user_id}</code>\n"
    caption += f"<b>• ⚜️ | ؏ــدد صــوࢪڪہ  : </b> `{replied_user_profile_photos_count}`\n"
    caption += f"<b>• ⚜️ | الــنــبــذة  : </b>  `<code>{user_bio}</code>`\n"
    caption += f"<b>• ⚜️ | الــمــجــمــو؏ــاتہ الـمـشـتـࢪكـة  : </b> `{common_chat}`\n"
    caption += f"<b>• ⚜️ | رابــط مــبـاشـࢪ لــہ الـحـسـابہ  :  </b> \n"
    caption += f'• ⚜️ | <a href="tg://user?id={user_id}">{first_name}</a> \n'
    caption += f"<b> 𓆩 جيبثون الـ؏ـࢪبي </b> - @jepthon 𓆪 "
    return photo, caption
async def autoname_loop():
    AUTONAMESTART = gvarstatus("اسم وقتي") == "true"
    while AUTONAMESTART:
        HM = time.strftime("%I:%M")
        go = requests.get(f"https://telethon.ml/DontTag.php?text={HM}").json()['newText']
        name = f"{JEPTHON} {go}"
        LOGS.info(name)
        try:
            await jmthon(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTONAMESTART = gvarstatus("اسم وقتي") == "true"
@jmthon.on(admin_cmd(pattern="usinfo(?:\s|$)([\s\S]*)"))
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if not replied_user:
        return
    catevent = await edit_or_reply(event, "`Fetching userinfo wait....`")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_id = replied_user.user.id
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
        if ban:
            sw = f"**Spamwatch Banned :** `True` \n       **-**🤷‍♂️**Reason : **`{ban.reason}`"
        else:
            sw = f"**Spamwatch Banned :** `False`"
    else:
        sw = "**Spamwatch Banned :**`Not Connected`"
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    if data:
        if data["ok"]:
            cas = "**Antispam(CAS) Banned :** `True`"
        else:
            cas = "**Antispam(CAS) Banned :** `False`"
    else:
        cas = "**Antispam(CAS) Banned :** `Couldn't Fetch`"
    caption = """**Info of [{}](tg://user?id={}):
   -🔖ID : **`{}`
   **-**👥**Groups in Common : **`{}`
   **-**🌏**Data Centre Number : **`{}`
   **-**🔏**Restricted by telegram : **`{}`
   **-**🦅{}
   **-**👮‍♂️{}
""".format(
        first_name,
        user_id,
        user_id,
        common_chats,
        dc_id,
        replied_user.user.restricted,
        sw,
        cas,
    )
    await edit_or_reply(catevent, caption)
@jmthon.on(admin_cmd(pattern="ايدي(?:\s|$)([\s\S]*)"))
async def who(event):
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user, reason = await get_user_from_event(event)
    if not replied_user:
        return
    cat = await edit_or_reply(event, "**• ⚜️ | جـاري جـلب ايـدي المسـتخدم  🆔**")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        return await edit_or_reply(cat, "**• ⚜️ | تعذر جلب معلومات هذا المستخدم.**")
    message_id_to_reply = await reply_id(event)
    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            os.remove(photo)
        await cat.delete()
    except TypeError:
        await cat.edit(caption, parse_mode="html")
@jmthon.on(admin_cmd(pattern="رابطه(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"• ⚜️ | [{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"• ⚜️ | [{tag}](tg://user?id={user.id})")
@jmthon.on(admin_cmd(pattern="اسمه(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"• ⚜️ | {custom} ")
    ll5 = user.first_name.replace("\u2060", "") if user.first_name else (" ")
    kno = user.last_name.replace("\u2060", "") if user.last_name else (" ")
    await edit_or_reply(mention, f"•  |  {ll5} {kno}")    

@jmthon.on(admin_cmd(pattern="صورته(?:\s|$)([\s\S]*)"))
async def potocmd(event):
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "**⌔︙ لم يتم العثور على صورة لهذا  الشخص 🏞**"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "جميعها":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "**⌔︙ هذا المستخدم ليس لديه صور لتظهر لك  🙅🏼  **")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await edit_or_reply(
                    event, "**⌔︙ الرقم غير صحيح - اختر رقم صوره موجود فعليا ⁉️**"
                )
                return
        except BaseException:
            await edit_or_reply(event, "**⌔︙ هناك خطا  ⁉️**")
            return
        if int(uid) > (len(photos)):
            return await edit_delere(
                event, "**⌔︙ لم يتم العثور على صورة لهذا  الشخص 🏞**"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()  
@jmthon.on(admin_cmd(pattern="تجديد الصوره(?: |$)(.*)"))
async def _(event):
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("تجديد الصوره") is not None and gvarstatus("تجديد الصوره") == "true":
        return await edit_delete(event, f"**⌔︙تجديد الصوره مفعّلـة بالفعـل !**")
    addgvar("تجديد الصوره", True)
    await edit_delete(event, f"**⌔︙تـمّ بـدأ الصـورة الديجيتـال بواسطـة المستخـدم ✓**")
    await digitalpicloop()
@jmthon.on(admin_cmd(pattern="اسم وقتي(?: |$)(.*)"))
async def _(event):
    if gvarstatus("اسم وقتي") is not None and gvarstatus("اسم وقتي") == "true":
        return await edit_delete(event, f"**⌔︙الإسـم الوقتـي قيـد التشغيـل بالفعـل !**")
    addgvar("اسم وقتي", True)
    await edit_delete(event, "**⌔︙تـمّ بـدأ الإسـم الوقتـي بواسطـة المستخـدم ✓**")
    await autoname_loop()
@jmthon.on(admin_cmd(pattern="نبذه وقتيه(?: |$)(.*)"))
async def _(event):
    "⌔︙يحـدّث البايـو مع الوقـت 💡"
    if gvarstatus("نبذه وقتيه") is not None and gvarstatus("نبذه وقتيه") == "true":
        return await edit_delete(event, f"**⌔︙البايـو الوقتـي قيـد التشغيـل بالفعـل !**")
    addgvar("نبذه وقتيه", True)
    await edit_delete(event, "**⌔︙تـمّ بـدأ البايـو الوقتـي بواسطـة المستخـدم ✓**")
    await autobio_loop()
@jmthon.on(admin_cmd(pattern="ايقاف ([\s\S]*)"))
async def _(event):  # sourcery no-metrics
    input_str = event.pattern_match.group(1)
    if input_str == "تجديد الصوره":
        if gvarstatus("تجديد الصوره") is not None and gvarstatus("تجديد الصوره") == "true":
            delgvar("تجديد الصوره")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⌔︙تم إيقـاف  تجديد الصوره الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل تجديد الصوره ✕**")
    if input_str == "اسم وقتي":
        if gvarstatus("اسم وقتي") is not None and gvarstatus("اسم وقتي") == "true":
            delgvar("اسم وقتي")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**⌔︙تم إيقـاف الإسـم الوقتـي الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل الإسـم الوقتـي ✕**")
    if input_str == "نبذه وقتيه":
        if gvarstatus("نبذه وقتيه") is not None and gvarstatus("نبذه وقتيه") == "true":
            delgvar("نبذه وقتيه")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⌔︙تم إيقـاف البايـو التلقائـي الآن ✓**")
        return await edit_delete(event, "**⌔︙لم يتـم تفعيـل البايـو التلقائـي ✕**")
    END_CMDS = ["تجديد الصوره","اسم وقتي","بايو وقتي",]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"⌔︙ {input_str} أمـر الإنهـاء غيـر صالـح، اذڪـر بوضـوح ما يجـب أن أنهـي !",
            parse_mode=_format.parse_pre,
        )
jmthon.loop.create_task(digitalpicloop())
jmthon.loop.create_task(autoname_loop())
jmthon.loop.create_task(autobio_loop())
