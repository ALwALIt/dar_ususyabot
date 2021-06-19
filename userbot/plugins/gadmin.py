import asyncio
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

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


@catub.cat_cmd(
    pattern="حظر(?: |$)(.*)",
    command=("حظر", plugin_category),
    info={
        "header": "To ban user in every group where you are admin.",
        "description": "Will ban the person in every group where you are admin only.",
        "usage": "{tr}gban <username/reply/userid> <reason (optional)>",
    },
)
async def catgban(event):  # sourcery no-metrics
    "To ban user in every group where you are admin."
    cate = await edit_or_reply(event, "**جـار الــحظر.......**")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == catub.uid:
        return await edit_delete(cate, "**لا استـطيع حـظر نفسي 🌿⚕**")
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"هذا [المستخدم](tg://user?id={user.id}) موجود بالفعل في قائمة الحظر ✅"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "**أنت لست مدير مجموعة واحدة على الأقل 😕💗**")
    await cate.edit(
        f"يتم حظر [المستخدم](tg://user?id={user.id}) في {len(san)} من المجموعات"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"ليس لديك صلاحيات في  :\n**المجموعة :** {event.chat.title}(`{event.chat_id}`)\nلتقوم بالحظر ⚕️💘",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) تم حـظره بنجاح في {count} من المجموعات في {cattaken} من الثواني !!\n**السبب :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) تم حـظره بنجاح في {count} من المجموعات في {cattaken} من الثواني !!"
        )
    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الحـظر\
                \nالحظـر\
                \n**المستخدم : **[{user.first_name}](tg://user?id={user.id})\
                \n**الايدي : **`{user.id}`\
                \n**السبب :** `{reason}`\
                \nالحظر في  {count} من المجموعات\
                \n**الوقت المستغرق : **`{cattaken} من الثواني`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#الحـظر\
                \nالحظـر\
                \n**المستخدم : **[{user.first_name}](tg://user?id={user.id})\
                \n**الايدي : **`{user.id}`\
                \nالحظر في  {count} من المجموعات\
                \n**الوقت المستغرق : **`{cattaken} من الثواني`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@catub.cat_cmd(
    pattern="الغاء حظر(?: |$)(.*)",
    command=("الغاء حظر", plugin_category),
    info={
        "header": "To unban the person from every group where you are admin.",
        "description": "will unban and also remove from your gbanned list.",
        "usage": "{tr}ungban <username/reply/userid>",
    },
)
async def catgban(event):
    "To unban the person from every group where you are admin."
    cate = await edit_or_reply(event, "**يتم الغاء الحظر ⚕️🤍**")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        return await edit_delete(
            cate, f"هذا [المستخدم](tg://user?id={user.id}) لم يتم حظره بالاصل ❕"
        )
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "أنت لست مدير مجموعة واحدة على الأقل ")
    await cate.edit(
        f"يتم الغاء حظر  [المستخدم](tg://user?id={user.id}) في `{len(san)}` من المجموعات "
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**ليس لديك صلاحيات في** :\n**الدردشة : **{event.chat.title}(`{event.chat_id}`)\n - لتقوم بالغاء حظره ⚕️❕",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) تم الغاء حظره بنجاح في {count} من المجموعات في {cattaken} من الثواني !!\n**السبب :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) تم الغاء حـظره بنجاح في {count} من المجموعات في {cattaken} من الثواني"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#تم_الغاء_حظرهم\
                \nالغير محـظورين\
                \n**المعـرف : **[{user.first_name}](tg://user?id={user.id})\
                \n**الايدي : **`{user.id}`\
                \n**الـسبب :** `{reason}`\
                \n__تم الغاء حظره في {count} من المجموعات__\
                \n**الوقت المستغرق : **`{cattaken} من الثواني`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#تم_الغاء_حظرهم\
                \nالغير محـظورين\
                \n**المعـرف : **[{user.first_name}](tg://user?id={user.id})\
                \n**الايدي : **`{user.id}`\
                \n__تم الغاء حظره في {count} من المجموعات__\
                \n**الوقت المستغرق : **`{cattaken} من الثواني`",
            )


@catub.cat_cmd(
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
        GBANNED_LIST = "لا يوجد مستخدمين محظورين ⚕️🌿"
    await edit_or_reply(event, GBANNED_LIST)


@catub.cat_cmd(
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
        await event.edit("قد تحدث مشاكل او اخطاء غير متوقعة ")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "**- عذرا لايمكنني كتم نفسي 📍**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "اسف انا غير قادر ع حظـر او كتم المستخدم ⚕️❤")
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} ` مكتوم بالفعل ✅`",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطـا**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} تم كتـم المستخدم بنجاح ✅\n **الـسبب :** `{reason}`",
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


@catub.cat_cmd(
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
        if user.id == catub.uid:
            return await edit_or_reply(event, "**عذرا لا يمكنني كتم نفسي 📍**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "**آسف أنا غير قادر على حظـر المستخدم 📍**")

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
                f"{_format.mentionuser(user.first_name ,user.id)} **تم الغاء كتم المستخدم بنجاح 👨‍💻",
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


@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()
