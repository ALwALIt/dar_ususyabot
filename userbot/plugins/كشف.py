import html
import os

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location
from ..sql_helper.globals import gvarstatus

from userbot import jmthon
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch

JEP_EM = Config.ID_EM or " •❃ "
ID_EDIT = gvarstatus("ID_ET") or "ايدي"

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
async def fetch_info(replied_user, event):
    """Get details from the User object."""
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "⌯︙هذا المستخدم لم يضع اي صورة"
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
        dc_id = "تعـذر جلـب ايدي الـديسي"
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
        else ("⌯︙هذا المستخدم ليس لديه اسم اول")
    )
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    rotbat = ".「  مطـور السورس 𓄂𓆃 」." if user_id == 705475246 else (".「  العضـو 𓅫  」.") 
    rotbat = ".「 مـالك الحساب 𓀫 」." if user_id == (await event.client.get_me()).id and user_id != 705475246 else rotbat
    username = "@{}".format(username) if username else ("⌯︙هـذا الشخص ليس لديـه معـرف ")
    user_bio = "⌯︙هذا المستخدم ليس لديه اي نبـذة" if not user_bio else user_bio
    caption = "✛━━━━━━━━━━━━━✛ \n"
    caption += f"<b>{JEP_EM} الاسـم ›</b> {first_name} {last_name}\n"
    caption += f"<b>{JEP_EM} المـعـرف ›</b> {username}\n"
    caption += f"<b>{JEP_EM} الايـدي  ›</b> <code>{user_id}</code>\n"
    caption += f"<b>{JEP_EM} عـدد الصـورة ›</b> {replied_user_profile_photos_count}\n"
    caption += f"<b>{JEP_EM} الرتبـــه  ⇦ {rotbat} </b>\n"
    caption += f"<b>{JEP_EM} الـنبـذه ›</b> \n<code>{user_bio}</code>\n\n"
    caption += f"<b>{JEP_EM} الـمجموعات المشتـركة ›</b> {common_chat}\n"
    caption += f"<b>{JEP_EM} رابط حسـابه ›</b> "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>\n'
    caption += f"✛━━━━━━━━━━━━━✛"
    return photo, caption


@jmthon.ar_cmd(
    pattern="كشف(?:\s|$)([\s\S]*)",
    command=("كشف", plugin_category),
    info={
        "header": "Gets information of an user such as restrictions ban by spamwatch or cas.",
        "description": "That is like whether he banned is spamwatch or cas and small info like groups in common, dc ..etc.",
        "usage": "{tr}userinfo <username/userid/reply>",
    },
)
async def _(event):
    "Gets information of an user such as restrictions ban by spamwatch or cas"
    replied_user, error_i_a = await get_user_from_event(event)
    if not replied_user:
        return
    catevent = await edit_or_reply(event, "⌯︙جار إحضار معلومات المستخدم اننظر قليلا ⚒️")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_id = replied_user.user.id
    # some people have weird HTML in their names
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
    caption = """**معلومات المسـتخدم[{}](tg://user?id={}):
   ⌔︙⚕️ الايدي: **`{}`
   ⌔︙👥**المجموعات المشتركه : **`{}`
   ⌔︙🌏**رقم قاعده البيانات : **`{}`
   ⌔︙🔏**هل هو حساب موثق  : **`{}`
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


@jmthon.on(admin_cmd(pattern=f"{ID_EDIT}(?:\s|$)([\s\S]*)"))
async def who(event):
    "Gets info of an user"
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user, reason = await get_user_from_event(event)
    if not replied_user:
        return
    cat = await edit_or_reply(event, "**⌯︙يتم استخراج معلومات المستخدم **")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        return await edit_or_reply(cat, "**⌯︙لم يتم العثور على معلومات لهذا المستخدم **")
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
#كـتابة  @RR7PP
#تعديل وترتيب  @SBB_B
@jmthon.ar_cmd(
    pattern="رابط الحساب(?:\s|$)([\s\S]*)",
    command=("رابط الحساب", plugin_category),
    info={
        "header": "Generates a link to the user's PM .",
        "usage": "{tr}link <username/userid/reply>",
    },
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙[{tag}](tg://user?id={user.id})")

@jmthon.ar_cmd(
    pattern="(الايدي|id)(?:\s|$)([\s\S]*)",
    command=("الايدي", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get id of the group or user."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{str(e)}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"⌯︙ايدي المستخدم : `{input_str}` هو `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"⌯︙ايدي الدردشة/القناة `{p.title}` هو `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "⌯︙يـجب كـتابة مـعرف الشـخص او الـرد عـليه")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"⌯︙ايدي الدردشه: `{str(event.chat_id)}` \n⌯︙ايدي المستخدم: `{str(r_msg.sender_id)}` \n⌯︙ايدي الميديا: `{bot_api_file_id}`",
            )
        else:
            await edit_or_reply(
                event,
               f"⌯︙ايدي الدردشه : `{str(event.chat_id)}` \n⌯︙ايدي المستخدم: `{str(r_msg.sender_id)}` ",
            )
    else:
        await edit_or_reply(event, f"⌯︙الـدردشـة الـحالية : `{str(event.chat_id)}`")
