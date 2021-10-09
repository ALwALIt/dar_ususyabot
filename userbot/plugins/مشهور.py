#𝙕𝙚𝙙𝙏𝙝𝙤𝙣 ®
#الملـف حقـوق وكتابـة زلـزال الهيبـه ⤶ @zzzzl1l خاص بسـورس ⤶ 𝙕𝙚𝙙𝙏𝙝𝙤𝙣
#الملـف متعـوب عليه تخمـط اذكر المصـدر
#تعـديل بنيـتي 𝙈

import os
import random
from asyncio import sleep

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from . import *
from . import mention

TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

FANAN = "<b> 𓆩 𝗦𝗢𝗨𝗥𝗖𝗘 𝙕𝞝𝘿 - 💞🤵💞 𓆪 </b>"
VANAN = "<b> ⋄︙افيشش 🥺💘 </b>"
sts_fanan = "https://telegra.ph/file/50caf0efa9a2453985364.jpg"
sts_fanan2 = "https://telegra.ph/file/dda7dd09f7d697fe92ff6.jpg" 
sts_fanan3 = "https://telegra.ph/file/007f130ef1028d15c3596.jpg"
sts_fanan4 = "https://telegra.ph/file/593c7e83d4eb25f7b0e55.jpg"
sts_fanan5 = "https://telegra.ph/file/48f567da3417c581446dc.jpg"
sts_fanan6 = "https://telegra.ph/file/165c9405bddc89cf818be.jpg"
sts_fanan7 = "https://telegra.ph/file/7217fc9ebe7c92b1e42c3.jpg"
sts_fanan8 = "hhttps://telegra.ph/file/de70edbf7e01440c6e7bd.jpg"
sts_fanan9 = "https://telegra.ph/file/63e1b87537e92c05da46d.jpg"
sts_fanan10 = "https://telegra.ph/file/d58d68c118d862437f66a.jpg"
sts_fanan11 = "https://telegra.ph/file/28c209102abe082b97e99.jpg"
sts_fanan12 = "https://telegra.ph/file/53f4c117abcfc24934337.jpg"
sts_fanan13 = "https://telegra.ph/file/739a13b944c62412e908b.jpg"
sts_fanan14 = "https://telegra.ph/file/291a667b5bc7e7f15895d.jpg"
sts_fanan15 = "https://telegra.ph/file/e83874718d4eb829fc0e7.jpg"
sts_fanan16 = "https://telegra.ph/file/f2683a9c2f6aec9f16850.jpg"
sts_fanan17 = "https://telegra.ph/file/8775bf7b8edde56243897.jpg"
sts_fanan18 = "https://telegra.ph/file/b544499b6853568ce475f.jpg"

ZEED_IMG = sts_fanan or sts_fanan2 or sts_fanan3 or sts_fanan4 or sts_fanan5

@bot.on(admin_cmd(pattern="مشهور(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="مشهور(?: |$)(.*)", allow_sudo=True))
async def who(event):
    zed = await eor(event, "⇆")
    replied_user = await get_user(event)
    try:
        ZEED_IMG, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await eor(zed, "..")
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
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن إنجين أكيوريك 🥺💘. </b>"
       return sts_fanan, caption
    if x == 2:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن كيفانش تاتليتوغ 🥺💘. </b>"
       return sts_fanan2, caption
    if x == 3:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن شاتاي أولسوي 🥺💘. </b>"
       return sts_fanan3, caption
    if x == 4:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن إنجين ألتان دوزياتان 🥺💘. </b>"
       return sts_fanan4, caption
    if x == 5:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن بوراك أوزجيفت 🥺💘. </b>"
       return sts_fanan5, caption
    if x == 6:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن أراس بولوت إيناملي 🥺💘. </b>"
       return sts_fanan6, caption
    if x == 7:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن گريستيانو رونالدو 🥺💘. </b>"
       return sts_fanan7, caption
    if x == 8:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن سيركان شاي أوغلو 🥺💘. </b>"
       return sts_fanan8, caption
    if x == 9:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن كرم بورسين🥺💘. </b>"
       return sts_fanan9, caption
    if x == 10:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن توم گــروز🥺💘. </b>"
       return sts_fanan10, caption
    if x == 11:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن شاهـد گــابور🥺💘. </b>"
       return sts_fanan11, caption
    if x == 12:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن ليـو ميسـي🥺💘. </b>"
       return sts_fanan12, caption
    if x == 13:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن محمد حماقي🥺💘. </b>"
       return sts_fanan13, caption
    if x == 14:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن شَاروخــان🥺💘. </b>"
       return sts_fanan14, caption
    if x == 15:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن سيـف نبيل🥺💘. </b>"
       return sts_fanan15, caption
    if x == 16:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن ليوناردو گـابريو 🥺💘. </b>"
       return sts_fanan16, caption
    if x == 17:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن محمد رمـضان🥺💘. </b>"
       return sts_fanan17, caption
    if x == 18:
       caption = f"<b> {FANAN} </b>\n\n\n"
       caption += f"<b> {VANAN} </b>"
       caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
       caption += f"\n\n<b> ⋄︙مبࢪوڪ زواجج مِـن سعــد المجرد 🥺💘. </b>"
       return sts_fanan18, caption


CMD_HELP.update(
    {
        "مشهور": """**اسم الاضافـه : **`مشهور`
**╮•❐ الامـر ⦂**
  •  `.مشهور` بالرد / المعرف / الايدي
**•  الشـرح •• **__امـر تسليـة زوجنـي مـن مشهـور__"""
    }
)
