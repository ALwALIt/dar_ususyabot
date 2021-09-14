import asyncio

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

from userbot import jmthon

from ..core.managers import edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, get_user_from_event

plugin_category = "admin"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


# ARABIC CAT BY  @RRRD7  -  @UUNZZ


@jmthon.ar_cmd(
    pattern="المحظورين$",
    command=("المحظورين", plugin_category),
    info={
        "header": "Shows you the list of all gbanned users by you.",
        "usage": "{tr}listgban",
    },
)
async def gablist(event):
    "Shows you the list of all gbanned users by you."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "الـمستخدمين الـمحظورين\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) لـ {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) بـدون سبب\n"
                )
    else:
        GBANNED_LIST = "⌔︙ لا يوجد مستخدمين محظورين ⚠️"
    await edit_or_reply(event, GBANNED_LIST)


@jmthon.ar_cmd(
    pattern="كتم(?: |$)(.*)",
    command=("كتم", plugin_category),
    info={
        "header": "To mute a person in all groups where you are admin.",
        "description": "It doesnt change user permissions but will delete all messages sent by him in the groups where you are admin including in private messages.",
        "usage": "{tr}gmute username/reply> <reason (optional)>",
    },
)
async def startgmute(event):
    "To mute a person in all groups where you are admin."
    if event.is_private:
        await event.edit("⌔︙ قد تحدث مشاكل او اخطاء غير متوقعة ")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "**⌔︙- عذرا لايمكنني كتم نفسي ⚠️**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "⌔︙ اسف انا غير قادر ع حظـر او كتم المستخدم ⚠️"
        )
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)}  مكتوم بالفعل ✅",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطـا**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} تم كتـم المستخدم بنجاح ✅\n**الـسبب :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} تم كتـم المستخدم بنجاح ✅",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكـتم\n"
                f"**المستخدم 👱‍♂ :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**سبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكـتم\n"
                f"**المستخدم 👱‍♂ :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@jmthon.ar_cmd(
    pattern="الغاء كتم(?: |$)(.*)",
    command=("الغاء كتم", plugin_category),
    info={
        "header": "To unmute the person in all groups where you were admin.",
        "description": "This will work only if you mute that person by your gmute command.",
        "usage": "{tr}ungmute <username/reply>",
    },
)
async def endgmute(event):
    "To remove gmute on that person."
    if event.is_private:
        await event.edit("قد تحدث مشاكل او اخطاء غير متوقعة !")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "**⌔︙ عذرا لا يمكنني كتم نفسي ⚠️**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**⌔︙ آسف أنا غير قادر على حظـر المستخدم ⚠️**"
        )

    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"{_format.mentionuser(user.first_name ,user.id)} غير مكتوم 🔱"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خـطـا**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} تم الغاء كتم المستخدم بنجاح ✅\n**الـسبب  :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} **تم الغاء كتم المستخدم بنجاح 👨‍💻**",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الـغاء_الـكتم\n"
                f"**المستخدم 👨‍💻 :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**سبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الـغاء_الـكتم\n"
                f"**المستخدم 👨‍💻 :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@jmthon.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()
