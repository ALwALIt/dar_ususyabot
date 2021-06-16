import asyncio
from random import choice, randint

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="وهمية(?: |$)(.*)",
    command=("وهمية", plugin_category),
    info={
        "header": "To show fake actions for a paticular period of time",
        "description": "if time is not mentioned then it may choose random time 5 or 6 mintues for mentioning time use in seconds",
        "usage": [
            "{tr}scam <action> <time(in seconds)>",
            "{tr}scam <action>",
            "{tr}scam",
        ],
        "examples": "{tr}scam photo 300",
        "actions": [
            "كتابة",
            "جهة",
            "لعبة",
            "موقع",
            "صوتية",
            "جولة",
            "فيديو",
            "صورة",
            "ملف",
        ],
    },
)
async def _(event):
    options = [
        "كتابة",
        "جهة",
        "لعبة",
        "موقع",
        "صوتية",
        "جولة",
        "فيديو",
        "صورة",
        "ملف",
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(300, 360)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(300, 360)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await edit_delete(event, "`Invalid Syntax !!`")
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await asyncio.sleep(scam_time)
    except BaseException:
        return


@catub.cat_cmd(
    pattern="لقب(?: |$)(.*)",
    command=("لقب", plugin_category),
    info={
        "header": "To promote a person without admin rights",
        "note": "You need proper rights for this",
        "usage": [
            "{tr}prankpromote <userid/username/reply>",
            "{tr}لقب <الايدي/المعرف/بالرد عليه> <اللقب>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To promote a person without admin rights"
    new_rights = ChatAdminRights(post_messages=True)
    catevent = await edit_or_reply(event, "**- يتم اعطاء اللقب**")
    user, rank = await get_user_from_event(event, catevent)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    except Exception as e:
        return await edit_delete(catevent, f"__{str(e)}__", time=10)
    await catevent.edit("**- تم وضع اللقب بنجاح**")


@catub.cat_cmd(
    pattern="ارفع",
    command=("ارفع", plugin_category),
    info={
        "header": "Fun animation for faking user promotion",
        "description": "An animation that shows enabling all permissions to him that he is admin(fake promotion)",
        "usage": "{tr}padmin",
    },
    groups_only=True,
)
async def _(event):
    "Fun animation for faking user promotion."
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "`promoting.......`")
    animation_chars = [
        "**جـاري رفع مشرف...**",
        "**تمكين كافة أذونات المستخدم ...**",
        "**(1) إرسل رسائل: ☑️**",
        "**(1) إرسل رسائل: ✅**",
        "**(2) إرسال الوسائط: ☑️**",
        "**(2) إرسال الوسائط: ✅**",
        "**(3) إرسال ملصقات وصور GIF: ☑️**",
        "**(3) إرسال ملصقات وصور GIF: ✅**",
        "**(4) إرسال استطلاعات الرأي: ☑️**",
        "**(4) إرسال استطلاعات الرأي: ✅**",
        "**(5) روابط التضمين: ☑️**",
        "**(5) روابط التضمين: ✅**",
        "**(6) أضف مستخدمين: ☑️**",
        "**(6) أضف مستخدمين: ✅**",
        "**(7) تثبيت الرسائل: ☑️**",
        "**(7) تثبيت الرسائل: ✅**",
        "**(8) تغيير معلومات الدردشة: ☑️**",
        "**(8) تغيير معلومات الدردشة: ✅**",
        "**تم منح الإذن بنجاح**",
        f"**امتيازات عامة : {DEFAULTUSER}**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 20])