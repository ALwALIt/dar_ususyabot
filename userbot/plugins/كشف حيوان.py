# This File for zed® written by ~ @ZlZZl77
#الملف كتابتي وحقوقي + متعوب عليه
#فلا تصير مطور براسي - اذا تريد تخمط اذكر المصدر حبي

import os
import random

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

# حقوق زد ثــون -- زلـزال_الهيبـه -- @ZeDThoN

hhh = [
    "جلب شوارع 🐕‍🦺",
    "مطي زربه 🦓",
    "قرد لزكـه 🐒",
    "طلي ابو البعرور الوصخ 🐑",
    "صخل محترم 🐐",
    "بزون ابوخالد 🐈",
    "الزاحف ابو بريص 🦎",
    "جريذي ابو المجاري 🐀",
    "هايشه دنماركيه 🐄🇩🇰",
]

jjj = [
    "100% مو حيوان غنبله 😱😂.",
    "90% مو حيوان ضيم 😱😂👆",
    "80%  ٴ😱😂",
    "70%  ٴ😱😂",
    "60% براسه 60 حظ 👌😂",
    "50% حيوان هجين👍😂",
    "( 40% ) خوش حيوان 👌😂",
    "30% ٴ😒😂",
    "20% ٴ😒😂",
    "10% ٴ😒😂",
    "0% ٴ😢😂",
]


@bot.on(admin_cmd(pattern="كشف(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="كشف(?: |$)(.*)", allow_sudo=True))
async def who(event):
    ics = await eor(event, "ٴ⇌")
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await eor(ics, "لايمكنني العثور ع الحيوان")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
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
        await ics.delete()
    except TypeError:
        await ics.edit(caption, parse_mode="html")


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
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "الحيوان مامخلي صورة بروفايل"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except:
        pass
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    fof = random.choice(hhh)
    yoy = random.choice(jjj)
    replied_user.user.bot
    replied_user.user.restricted
    replied_user.user.verified
    photo = await event.client.download_profile_photo(
        user_id, TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا الحيوان ليس له اسم أول")
    )
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    username = "@{}".format(username) if username else ("لايوجد معرف")
    caption = f"<b>  ╮•🦦 الحيوان ⇦ </b> {first_name} {last_name} \n"
    caption += f"<b> ٴ╼──────────────────╾ </b>\n"
    caption += f"<b> • 🌚 | معـرفه  ⇦ </b> {username}\n"
    caption += f"<b> • 🌚 | ايـديه   ⇦ </b> <code>{user_id}</code>\n"
    caption += f"<b> • 🌚 | صـوره  ⇦ </b> {replied_user_profile_photos_count} </b>\n"
    caption += f"<b> • 🌚 | نــوعه   ⇦  {fof} </b>\n"
    caption += f"<b> • 🌚 | نسبتـه  ⇦  {yoy} </b>\n\n\n"
    caption += f"<b> 𓆩 𝙎𝙊𝙐𝙍𝘾𝞝 𝙕𝞝𝘿 𓆪 </b> - @ZedThon "
    return photo, caption

CMD_HELP.update(
    {
        "الحيوان": "**Plugin : **`الحيوان`\n\n"
        "**⌔∮ الامر : `.كشف`\n**"
        "**⌔∮ الشرح :** امر تحشيش كشف الحيوان يكشف ع الشخص بالرد والمعرف والايدي والصورة"
    }
)
