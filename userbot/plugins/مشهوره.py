#𝙕𝙚𝙙𝙏𝙝𝙤𝙣 ®
#الملـف حقـوق وكتابـة زلـزال الهيبـه ⤶ @zzzzl1l خاص بسـورس ⤶ 𝙕𝙚𝙙𝙏𝙝𝙤𝙣
#الملـف متعـوب عليه تخمـط اذكر المصـدر

import os
import random
from asyncio import sleep

from ..core.managers import edit_delete, edit_or_reply

from userbot import jmthon
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from . import *
from . import mention

TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

FANAN = "<b> 𓆩 𝗦𝗢𝗨𝗥𝗖𝗘 𝗝𝗘𝗣 - 💞👰🏻‍♀💞 𓆪 </b>"
VANAN = "<b> ⋄︙افيشش 🥺💘 </b>"
sts_fanan = "https://telegra.ph/file/1f79aad6235f08ea76166.jpg"
sts_fanan2 = "https://telegra.ph/file/e04b22171d7bb524e7f44.jpg" 
sts_fanan3 = "https://telegra.ph/file/4502e1268a73117d9abac.jpg"
sts_fanan4 = "https://telegra.ph/file/5221a638913c64749760b.jpg"
sts_fanan5 = "https://telegra.ph/file/9c070eb80b621cbe0333c.jpg"
sts_fanan6 = "https://telegra.ph/file/6f34aa7f98fb6cfec3b57.jpg"
sts_fanan7 = "https://telegra.ph/file/9f0de560d7e7fc2752437.jpg"
sts_fanan8 = "https://telegra.ph/file/434d739dd887df9a40ae1.jpg"
sts_fanan9 = "https://telegra.ph/file/ac11888f2eca8529387de.jpg"
sts_fanan10 = "https://telegra.ph/file/4d999ac0dddd3964979a4.jpg"
sts_fanan11 = "https://telegra.ph/file/07d59b7a9a9b37c46d64f.jpg"
sts_fanan12 = "https://telegra.ph/file/788aab2a68a5a6f19f8c1.jpg"
sts_fanan13 = "https://telegra.ph/file/6c18a61f0f3d9e5b51576.jpg"
sts_fanan14 = "https://telegra.ph/file/974240259ba3d35a0507d.jpg"
sts_fanan15 = "https://telegra.ph/file/a5d73c57e8eea74937093.jpg"
sts_fanan16 = "https://telegra.ph/file/e6fd5618dc186ae286e9c.jpg"
sts_fanan17 = "https://telegra.ph/file/d40c3f57c3b1c2fceaef0.jpg"
sts_fanan18 = "https://telegra.ph/file/650f99255eb90e8f95061.jpg"

ZEED_IMG = sts_fanan or sts_fanan2 or sts_fanan3 or sts_fanan4 or sts_fanan5

@jmthon.on(admin_cmd(pattern="مشهوره(?: |$)(.*)"))
@jmthon.on(sudo_cmd(pattern="مشهوره(?: |$)(.*)", allow_sudo=True))
async def who(event):
    zed = await edit_or_reply(event, "⇆")
    replied_user = await get_user(event)
    try:
        ZEED_IMG, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await edit_or_reply(zed, "..")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await event.client.send_file(
            event.chat_id,
            ZEED_IMG,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
    except TypeError:
        await zed.edit(caption, parse_mode="html")


async def get_user(event):
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return replied_user


async def fetch_info(replied_user, event):
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    replied_user.user.bot
    replied_user.user.restricted
    replied_user.user.verified
    ZEED_IMG
    x = random.randrange(1, 18)
    if x == 1:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن بيرين سات 🥺💘. </b>"
       return sts_fanan, caption
    if x == 2:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن إسـراء الاصيـل 🥺💘. </b>"
       return sts_fanan2, caption
    if x == 3:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن رحمـة ريـاض 🥺💘. </b>"
       return sts_fanan3, caption
    if x == 4:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن تـوبا بويوكـوستن 🥺💘. </b>"
       return sts_fanan4, caption
    if x == 5:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن هـازال كـايا 🥺💘. </b>"
       return sts_fanan5, caption
    if x == 6:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن هـاندا ارتشـل 🥺💘. </b>"
       return sts_fanan6, caption
    if x == 7:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن هيفـاء وهبـي 🥺💘. </b>"
       return sts_fanan7, caption
    if x == 8:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن نانسـي عجـرم 🥺💘. </b>"
       return sts_fanan8, caption
    if x == 9:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن شيـرين عبد الوهـاب 🥺💘. </b>"
       return sts_fanan9, caption
    if x == 10:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن احـلام 🥺💘. </b>"
       return sts_fanan10, caption
    if x == 11:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن حـلا تـرك 🥺💘. </b>"
       return sts_fanan11, caption
    if x == 12:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن نجـوى كـرم 🥺💘. </b>"
       return sts_fanan12, caption
    if x == 13:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن هـاندا ارتشـل 🥺💘. </b>"
       return sts_fanan13, caption
    if x == 14:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن آيشـه افيخـاي 🥺💘. </b>"
       return sts_fanan14, caption
    if x == 15:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن burcu ozberk 🥺💘. </b>"
       return sts_fanan15, caption
    if x == 16:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن شيمـاء سيـف 😂💘. </b>"
       return sts_fanan16, caption
    if x == 17:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن نيهـان اتاغـول 🥺💘. </b>"
       return sts_fanan17, caption
    if x == 18:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجك مِـن ميليسـا بامـوك 🥺💘. </b>"
       return sts_fanan18, caption


CMD_HELP.update(
    {
        "مشهوره": """**اسم الاضافـه : **`مشهوره`
**╮•❐ الامـر ⦂**
  •  `.مشهوره` بالرد / المعرف / الايدي
**•  الشـرح •• **__امـر تسليـة زوجنـي مـن مشهـور__"""
    }
)
