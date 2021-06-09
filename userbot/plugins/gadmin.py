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
    pattern="حظر عام(?: |$)(.*)",
    command=("حظر عام", plugin_category),
    info={
        "header": "To ban user in every group where you are admin.",
        "description": "Will ban the person in every group where you are admin only.",
        "usage": "{tr}gban <username/reply/userid> <reason (optional)>",
    },
)
async def catgban(event):  # sourcery no-metrics
    "To ban user in every group where you are admin."
    cate = await edit_or_reply(event, "`جار حظر المستخدم ♻️`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == catub.uid:
        return await edit_delete(cate, "`لماذا احظر نفسي ?`")
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"`هو `[user](tg://user?id={user.id})`موجود بالفعل في قائمة المحظورين ⌁`"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "`لايمكنك حظر المستخدم الى مشرف في مجموعة واحده ع الاقل ⌁` ")
    await cate.edit(
        f"`بدء حظر `[user](tg://user?id={user.id}) `في {len(san)} الكروبات`"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`ليس لديك الإذن المطلوب في ¦ `\n**الدردشة :** {event.chat.title}(`{event.chat_id}`)\n`الحظر هنا`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `تم حظره في {count} في المجموعات {cattaken} ثواني`!!\n**سبب :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `تم حظره في {count} في المجموعات {cattaken} ثواني`!!"
        )
    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#حظر\
                \nحظر عالمي\
                \n**المستخدم : **[{user.first_name}](tg://user?id={user.id})\
                \n**ايدي : **`{user.id}`\
                \n**سبب :** `{reason}`\
                \n__محظور في {count} groups__\
                \n**الوقت المستغرق : **`{cattaken} ثواني`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#حظر\
                \nحظر عالمي\
                \n**المستخدم ¦  **[{user.first_name}](tg://user?id={user.id})\
                \n**ايدي ¦  **`{user.id}`\
                \n__محظور في {count} groups__\
                \n**الوقت المستغرق : **`{cattaken} ثواني`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@catub.cat_cmd(
    pattern="الغاء حظر العام(?: |$)(.*)",
    command=("الغاء حظر العام", plugin_category),
    info={
        "header": "To unban the person from every group where you are admin.",
        "description": "will unban and also remove from your gbanned list.",
        "usage": "{tr}ungban <username/reply/userid>",
    },
)
async def catgban(event):
    "To unban the person from every group where you are admin."
    cate = await edit_or_reply(event, "`جار الغاء حظر المستخدم في المجموعات ♻️ .`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        return await edit_delete(
            cate, f"هو [user](tg://user?id={user.id}) `ليس موجود في قائمة المحظورين`"
        )
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "`أنت لست مشرفًا حتى على مجموعة واحدة على الأقل `")
    await cate.edit(
        f"بدء الغاء الحظر [user](tg://user?id={user.id}) في `{len(san)}` المجموعات"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`ليس لدي الاذن المطلوب  ¦ `\n**المجموعة : **{event.chat.title}(`{event.chat_id}`)\n`للغاء الحظر`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}`) كان غير محظور في {count} الكروبات {cattaken} ثواني`!!\n**سبب :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `كان غير محظور في {count} الكروبات {cattaken} ثواني`!!"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**المستخدم : **[{user.first_name}](tg://user?id={user.id})\
                \n**ايدي : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__الغاء حظر في {count} الكروبات__\
                \n**الوقت المستغرق : **`{cattaken} ثواني`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**المستخدم : **[{user.first_name}](tg://user?id={user.id})\
                \n**ايدي : **`{user.id}`\
                \n__الغاء حظر {count} groups__\
                \n**الوقت المستغرق : **`{cattaken} ثواني`",
            )


@catub.cat_cmd(
    pattern="المحظورين عام$",
    command=("المحظورين عام", plugin_category),
    info={
        "header": "Shows you the list of all gbanned users by you.",
        "usage": "{tr}listgban",
    },
)
async def gablist(event):
    "Shows you the list of all gbanned users by you."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
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
        await event.edit("`قد تحدث مشاكل او اخطاء غير متوقعة !`")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "`عذرا لايمكنني كتم نفسي 📍`")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "`اسف انا غير قادر ع احضار او كتم المستخدم ⌁`")
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
                f"{_format.mentionuser(user.first_name ,user.id)} ▫️ ¦  تم كتم المستخدم \n**سبب :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} ▫️ ¦  تم كتم المستخدم ",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**المستخدم 👱‍♂ :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**سبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
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
        await event.edit("`قد تحدث مشاكل او اخطاء غير متوقعة !`")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "`عذرا لا يمكنني كتم نفسي 📍`")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "`آسف أنا غير قادر على إحضار المستخدم 📍`")

    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"{_format.mentionuser(user.first_name ,user.id)} `غير مكتوم 🔱`"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خـطـا**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `▫️ ¦  تم الغاء كتم من هنا`\n**سبب  :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `▫️ ¦  تم الغاء كتم من هنا`",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**المستخدم 👨‍💻 :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**سبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**المستخدم 👨‍💻 :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()
        
@catub.cat_cmd(
    pattern="طرد(?: |$)(.*)",
    command=("طرد", plugin_category),
    info={
        "header": "To kick a person from the group",
        "description": "Will kick the user from the group so he can join back.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}kick <userid/username/reply>",
            "{tr}kick <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "استخدم هذا لطرد المستخدم من الدردشة"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "`جار طرد المستخدم ♻️`")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"`مطرود` [{user.first_name}](tg://user?id={user.id})`!`\nسبب : {reason}"
        )
    else:
        await catevent.edit(f"`مطرود` [{user.first_name}](tg://user?id={user.id})`!`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الطرد\n"
            f"المستخدم ¦  [{user.first_name}](tg://user?id={user.id})\n"
            f"الدردشة ¦  {event.chat.title}(`{event.chat_id}`)\n",
        )
