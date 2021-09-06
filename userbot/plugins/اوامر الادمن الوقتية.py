from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from userbot import jmthon

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from . import BOTLOG, BOTLOG_CHATID, extract_time, get_user_from_event

plugin_category = "admin"

# =================== CONSTANT ===================
NO_ADMIN = "**⌯︙ عذرا انا لست مشرف في المجموعة ❕**"
NO_PERM = "**⌯︙يبـدو انه ليس لديك صلاحيات كافية هذا حزين جدا 🥱♥**"


@jmthon.ar_cmd(
    pattern="كتم_مؤقت(?:\s|$)([\s\S]*)",
    command=("كتم_مؤقت", plugin_category),
    info={
        "header": "To stop sending messages permission for that user",
        "description": "Temporary mutes the user for given time.",
        "Time units": {
            "s": "seconds",
            "m": "minutes",
            "h": "Hours",
            "d": "days",
            "w": "weeks",
        },
        "usage": [
            "{tr}tmute <userid/username/reply> <time>",
            "{tr}tmute <userid/username/reply> <time> <reason>",
        ],
        "examples": ["{tr}tmute 2d to test muting for 2 days"],
    },
    groups_only=True,
    require_admin=True,
)
async def tmuter(event):  # sourcery no-metrics
    "لكـتم شخص لمدة معينة"
    catevent = await edit_or_reply(event, "⌯︙يـتم  الـكتم أنتـظر 🧸♥")
    user, reason = await get_user_from_event(event, catevent)
    if not user:
        return
    if not reason:
        return await catevent.edit("⌯︙انـت لم تقـم بـوضـع وقـت مع الامـر")
    reason = reason.split(" ", 1)
    hmm = len(reason)
    cattime = reason[0].strip()
    reason = "".join(reason[1:]) if hmm > 1 else None
    ctime = await extract_time(catevent, cattime)
    if not ctime:
        return
    if user.id == event.client.uid:
        return await catevent.edit(f"⌯︙عـذرا لا يمـكننـي حـظر نفـسي ")
    try:
        await catevent.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await catevent.edit(
                f"⌯︙الـمستخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌯︙تـم كتمه بنجـاح ✅\n"
                f"⌯︙مـدة الـكتم : {cattime}\n"
                f"⌯︙الـسبب : {reason}"
            )
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الكتـم المؤقـت\n"
                    f"**المستخدم : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**الدردشـه : **{event.chat.title}(`{event.chat_id}`)\n"
                    f"**مدة الـكتم : **`{cattime}`\n"
                    f"**السـبب : **`{reason}``",
                )
        else:
            await catevent.edit(
                f"** الـمستخدم {_format.mentionuser(user.first_name ,user.id)}** \n **تم كـتمه بنجاح ✅**\n"
                f"**مدة الكتم** {cattime}\n"
            )
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#الـكتم المـؤقت\n"
                    f"**المستخدم : **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**الدردشه : **{event.chat.title}(`{event.chat_id}`)\n"
                    f"** مـدة الكتـم : **`{cattime}`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await catevent.edit("**يبدو ان كتم الشخص تم الغائه**")
    except UserAdminInvalidError:
        return await catevent.edit(
            "** يبـدو أنك لسـت مشرف في المجموعة او تحاول كتم مشـرف هنا**"
        )
    except Exception as e:
        return await catevent.edit(f"`{str(e)}`")


@jmthon.ar_cmd(
    pattern="حظر_مؤقت(?:\s|$)([\s\S]*)",
    command=("حظر_مؤقت", plugin_category),
    info={
        "header": "To remove a user from the group for specified time.",
        "description": "Temporary bans the user for given time.",
        "Time units": {
            "s": "seconds",
            "m": "minutes",
            "h": "Hours",
            "d": "days",
            "w": "weeks",
        },
        "usage": [
            "{tr}tban <userid/username/reply> <time>",
            "{tr}tban <userid/username/reply> <time> <reason>",
        ],
        "examples": ["{tr}tban 2d to test baning for 2 days"],
    },
    groups_only=True,
    require_admin=True,
)
async def tban(event):  # sourcery no-metrics
    "لحـظر شخص مع وقـت معيـن"
    catevent = await edit_or_reply(event, "⌯︙يتـم  الـحظر مؤقـتا أنتـظر **")
    user, reason = await get_user_from_event(event, catevent)
    if not user:
        return
    if not reason:
        return await catevent.edit("⌯︙يبدو انك لم تقم بوضع وقت مع الامر **")
    reason = reason.split(" ", 1)
    hmm = len(reason)
    cattime = reason[0].strip()
    reason = "".join(reason[1:]) if hmm > 1 else None
    ctime = await extract_time(catevent, cattime)
    if not ctime:
        return
    if user.id == event.client.uid:
        return await catevent.edit(f"⌯︙عذرا لا يمكنني كتم نفسـي")
    await catevent.edit("⌯︙تـم حـظره مـؤقـتا")
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await catevent.edit(
            "⌯︙** يبـدو أنك لسـت مشرف في المجموعة او تحاول كتم مشـرف هنا**"
        )
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "⌯︙** لـيس لدي صلاحيـات الحذف لكن سيبقى محظور ❕**"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await catevent.edit(
            f"**المستخدم {_format.mentionuser(user.first_name ,user.id)}** /n **تـم حظره بنـجاح ✅**\n"
            f"مـدة الحـظر {cattime}\n"
            f"السـبب:`{reason}`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الـحظر المـؤقت\n"
                f"**المستخدم : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**الدردشـه : **{event.chat.title}(`{event.chat_id}`)\n"
                f"**مـدة الحـظر : **`{cattime}`\n"
                f"**السـبب : **__{reason}__",
            )
    else:
        await catevent.edit(
            f"** الـمستخدم {_format.mentionuser(user.first_name ,user.id)} \n **تـم حظره بنـجاح ✅** \n"
            f"**مـدة الحـظر** {cattime}\n"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الـحظر المـؤقت\n"
                f"**المستخدم : **[{user.first_name}](tg://user?id={user.id})\n"
                f"**المستخدم : **{event.chat.title}(`{event.chat_id}`)\n"
                f"**مـدة الحـظر : **`{cattime}`",
            )
