import asyncio
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from userbot import jmthon

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


@jmthon.ar_cmd(
    pattern="عام حظر(?:\s|$)([\s\S]*)",
    command=("عام حظر", plugin_category),
    info={
        "header": "To ban user in every group where you are admin.",
        "description": "Will ban the person in every group where you are admin only.",
        "usage": "{tr}gban <username/reply/userid> <reason (optional)>",
    },
)
async def catgban(event):  # sourcery no-metrics
    "To ban user in every group where you are admin."
    cate = await edit_or_reply(event, "**⌔︙يـتم الـحظر أنتـظر قليـلا")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == jmthon.uid:
        return await edit_delete(cate, "⌔︙ لا استـطيع حـظر نـفسي")
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"⌔︙ هـذا [المسـتخدم](tg://user?id={user.id})` مـوجود بالفعـل في قائمة العام "
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = await admin_groups(event.client)
    count = 0
    jasme = len(san)
    if jasme == 0:
        return await edit_delete(cate, "**⌔︙ انت لـست ادمـن في مجـموعه واحـدة على الاقل**")
    await cate.edit(
        f"**⌔︙ يـتم حـظر [المـستخدم](tg://user?id={user.id}) فـي {len(san)} من المجمـوعات**"
    )
    for i in range(jasme):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ ليس لديـك صلاحيـات في :`\n**الـدردشة :** {get_display_name(achat)}(`{achat.id}`)\n⌔︙ لحـظر الشخـص",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"⌔︙ [{user.first_name}](tg://user?id={user.id}) تم حـظره بنجاح في {count} من المجموعات في {cattaken} من الثواني !!\n**السبب :** `{reason}`"
        )
    else:
        await cate.edit(
            f"⌔︙ [{user.first_name}](tg://user?id={user.id}) تم حـظره بنجاح في {count} من المجموعات في {cattaken} من الثواني !!"
        )
    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ تم الغاء حظرهم\
                \n⌔︙ الغير محـظورين\
                \n**⌔︙ المعـرف : **[{user.first_name}](tg://user?id={user.id})\
                \n**⌔︙ الايدي : **`{user.id}`\
                \n**⌔︙ الـسبب :** `{reason}`\
                \n⌔︙ تم الغاء حظره في {count} من المجموعات\
                \n**⌔︙ الوقت المستغرق : **`{cattaken} من الثواني`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ تم الغاء حظرهم\
                \n⌔︙ الغير محـظورين\
                \n**⌔︙ المعـرف : **[{user.first_name}](tg://user?id={user.id})\
                \n**⌔︙ الايدي : **`{user.id}`\
                \n⌔︙تم الغاء حظره في {count} من المجموعات\
                \n**⌔︙ الوقت المستغرق : **`{cattaken} من الثواني`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@jmthon.ar_cmd(
    pattern="الغاء عام حظر(?:\s|$)([\s\S]*)",
    command=("الغاء عام حظر", plugin_category),
    info={
        "header": "To unban the person from every group where you are admin.",
        "description": "will unban and also remove from your gbanned list.",
        "usage": "{tr}ungban <username/reply/userid>",
    },
)
async def catgban(event):
    "To unban the person from every group where you are admin."
    cate = await edit_or_reply(event, "⌔︙ يتـم الغـاء الحـظر العام أنتـظر")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        return await edit_delete(
            cate, f"هـذا [الشخص](tg://user?id={user.id}) \n ⌔︙ ليس في قائمة العـام اصلا "
        )
    san = await admin_groups(event.client)
    count = 0
    jasme = len(san)
    if jasme == 0:
        return await edit_delete(cate, "`you are not even admin of atleast one group `")
    await cate.edit(
        f"⌔︙ يتـم الغاء حـظر [المستخدم](tg://user?id={user.id}) في `{len(san)}` من الـكروبات"
    )
    for i in range(jasme):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ ليس لديـك صلاحـيات الـحظر في :`\n**⌔︙ الدردشة :** {get_display_name(achat)}(`{achat.id}`)\n⌔︙ لألـغاء الحـظر هنا",
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
                f"⌔︙ تم الغاء حظرهم\
                \n⌔︙ الغير محـظورين\
                \n**⌔︙ المعـرف : **[{user.first_name}](tg://user?id={user.id})\
                \n**⌔︙ الايدي : **`{user.id}`\
                \n**⌔︙ الـسبب :** `{reason}`\
                \n⌔︙تم الغاء حظره في {count} من المجموعات\
                \n**⌔︙ الوقت المستغرق : **{cattaken} من الثواني",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ تم الغاء حظرهم\
                \n⌔︙الغير محـظورين\
                \n**المعـرف⌔︙ : **[{user.first_name}](tg://user?id={user.id})\
                \n**الايدي⌔︙ : **`{user.id}`\
                \nتم⌔︙ الغاء حظره في {count} من المجموعات\
                \n**الوقت⌔︙ المستغرق : **{cattaken} من الثواني",
            )


@jmthon.ar_cmd(
    pattern="قائمه العام$",
    command=("قائمه العام", plugin_category),
    info={
        "header": "Shows you the list of all gbanned users by you.",
        "usage": "{tr}listgban",
    },
)
async def gablist(event):
    "Shows you the list of all gbanned users by you."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "⌔︙ الـمستخدمين المحـظورين عـام: \n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"⌔︙ [{a_user.chat_id}](tg://user?id={a_user.chat_id}) \n⌔︙بسبب {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"⌔︙ [{a_user.chat_id}](tg://user?id={a_user.chat_id}) بـدون سبـب\n"
                )
    else:
        GBANNED_LIST = "⌔︙ لا يـوجد مسـتخدم مـحظور حـاليا"
    await edit_or_reply(event, GBANNED_LIST)


@jmthon.ar_cmd(
    pattern="عام كتم(?:\s|$)([\s\S]*)",
    command=("عام كتم", plugin_category),
    info={
        "header": "To mute a person in all groups where you are admin.",
        "description": "It doesnt change user permissions but will delete all messages sent by him in the groups where you are admin including in private messages.",
        "usage": "{tr}gmute username/reply> <reason (optional)>",
    },
)
async def startgmute(event):
    "To mute a person in all groups where you are admin."
    if event.is_private:
        await event.edit("**⌔︙ قـد تـحدث اخـطاء غيـر متـوقعة**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "⌔︙ لا استـطيع كـتم نفـسي")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "⌔︙ عـذرا لم يتـم العـثور على معلـومات الشخص")
    if is_muted(userid, "عام كتم"):
        return await edit_or_reply(
            event,
            f"⌔︙ المستـخدم {_format.mentionuser(user.first_name ,user.id)} \n⌔︙ هـو بالفـعل مكـتوم",
        )
    try:
        mute(userid, "عام كتم")
    except Exception as e:
        await edit_or_reply(event, f"**خـطأ**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"⌔︙ المستـخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم كتـمه عـام بنـجاح\n**⌔︙ السبـب* `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"⌔︙ المستـخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم كتـمه عـام بنـجاح",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـكتم العـام \n"
                f"**⌔︙ المستـخدم  :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**⌔︙ السبـب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـكتم العـام \n"
                f"**⌔︙ المستـخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@jmthon.ar_cmd(
    pattern="الغاء كتم عام(?:\s|$)([\s\S]*)",
    command=("الغاء كتم عام", plugin_category),
    info={
        "header": "To unmute the person in all groups where you were admin.",
        "description": "This will work only if you mute that person by your gmute command.",
        "usage": "{tr}ungmute <username/reply>",
    },
)
async def endgmute(event):
    "To remove gmute on that person."
    if event.is_private:
        await event.edit("⌔︙ لا استـطيع حـظر نفـسي")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "⌔︙ لا استـطيع كـتم نفـسي")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "⌔︙ عـذرا لم يتـم العـثور على معلـومات الشخص ")
    if not is_muted(userid, "الغاء كتم عام"):
        return await edit_or_reply(
            event, f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n⌔︙ ليـس مكـتوم"
        )
    try:
        unmute(userid, "الغاء كتم عام")
    except Exception as e:
        await edit_or_reply(event, f"**خـطأ**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الغـاء الكتـم العام\n**⌔︙ السبـب :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الغـاء الكتـم العام",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**Reason :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@jmthon.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "الغاء كتم عام"):
        await event.delete()


@jmthon.ar_cmd(
    pattern="عام طرد(?:\s|$)([\s\S]*)",
    command=("عام طرد", plugin_category),
    info={
        "header": "kicks the person in all groups where you are admin.",
        "usage": "{tr}gkick <username/reply/userid> <reason (optional)>",
    },
)
async def catgkick(event):  # sourcery no-metrics
    "kicks the person in all groups where you are admin"
    cate = await edit_or_reply(event, "⌔︙** يـتم طـرده عـام من الكـروبات")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == jmthon.uid:
        return await edit_delete(cate, "⌔︙ لا استـطيع طـرد نفـسي")
    san = await admin_groups(event.client)
    count = 0
    jasme = len(san)
    if jasme == 0:
        return await edit_delete(cate, "⌔︙ ليـس لـدي صلاحيـات الأشـراف")
    await cate.edit(
        f"⌔︙ يتـم طـرد `[المستـخدم](tg://user?id={user.id}) فـي {len(san)} من الـكروبات"
    )
    for i in range(jasme):
        try:
            await event.client.kick_participant(san[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ لـيس لديـك الصلاحيـات المـطلوبة فـي :\n⌔︙ **الـدردشة :** {get_display_name(achat)}(`{achat.id}`)\n⌔︙ لـطرد المستخدم",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"⌔︙ المسـتخدم [{user.first_name}](tg://user?id={user.id}) \n ⌔︙ تـم طرده بنـجاح\n⌔︙ فـي {count} من الـكروبات \n⌔︙ الوقت المستغرق {cattaken} من الثواني!!\n**السبـب :** `{reason}`"
        )
    else:
        await cate.edit(
            f"⌔︙ المسـتخدم [{user.first_name}](tg://user?id={user.id})  ⌔︙ تـم طرده بنـجاح\n⌔︙ فـي {count} من الـكروبات \n ⌔︙ الوقت المستغرق {cattaken} من الثواني!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)
