"""
credits to @Jmthon
dont edit credits
"""
#  Copyright (C) 2020  sandeep.n(π.$)

import asyncio
import base64
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

import userbot.plugins.sql_helper.gban_sql_helper as gban_sql

from . import BOTLOG, BOTLOG_CHATID, CAT_ID, admin_groups, get_user_from_event
from .sql_helper.mute_sql import is_muted, mute, unmute

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


@bot.on(admin_cmd(pattern=r"حظر(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"حظر(?: |$)(.*)", allow_sudo=True))
async def catgban(event):
    if event.fwd_from:
        return
    cate = await edit_or_reply(event, "جار الحظر")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await cate.edit("ياغبي ماكدر احظر روحي 🤷😂")
        return
    if user.id in CAT_ID:
        await cate.edit("لا يمكنك حظر مطوري ♥️")
        return
    try:
        hmm = base64.b64decode("aHR0cHM6Ly93d3cudC5tZS9VVU5aWg==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) موجود بالفعل في قائمة الحظر بأي طريقة تحقق مرة أخرى"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("أنت لست مدير مجموعة واحدة على الأقل ")
        return
    await cate.edit(f"بدء حظر ↠ [{user.first_name}](tg://user?id={user.id})")
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {event.chat.title}(`{event.chat_id}`)\n`For banning here`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"⌁  المستخدم » [{user.first_name}](tg://user?id={user.id})\n  ⌁ تم حـظره "
        )
    else:
        await cate.edit(
            f"⌁  المستخدم » [{user.first_name}](tg://user?id={user.id})\n  ⌁ تم حـظره "
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@bot.on(admin_cmd(pattern=r"الغاء حظر(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"الغاء حظر(?: |$)(.*)", allow_sudo=True))
async def catgban(event):
    if event.fwd_from:
        return
    cate = await edit_or_reply(event, "جـار الـغاء الحـظر ⌁")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) لـيس موجـود في قـائمه الحـظر"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("أنت لست مسؤولًا حتى عن مجموعة واحدة على الأقل ")
        return
    await cate.edit(f"بدء الغاء حظر ↠ [{user.first_name}](tg://user?id={user.id})")
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat : **{event.chat.title}(`{event.chat_id}`)\n`For unbaning here`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}`) was ungbanned in {count} groups in {cattaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await cate.edit(
            f"❃∫ العضو » [{user.first_name}](tg://user?id={user.id}) \n ❃∫ تم الغاء حظره"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )


@bot.on(admin_cmd(pattern="المحظورين$"))
@bot.on(sudo_cmd(pattern=r"المحظورين$", allow_sudo=True))
async def gablist(event):
    if event.fwd_from:
        return
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
        GBANNED_LIST = "لايوجد مඋظوࢪين حتتى الان"
    await edit_or_reply(event, GBANNED_LIST)


@bot.on(admin_cmd(outgoing=True, pattern=r"كتم(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"كتم(?: |$)(.*)", allow_sudo=True))
async def startgmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("قد تحدث مشاكل غير متوقعة أو أخطاء !")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, "لا استطيع كتم نفسي ؟")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "يرجى الرد على مستخدم أو إضافته إلى الأمر لكتمه."
        )
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"هذًا الـمستخدم مـكتوم بالـفعل ⌁",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**Error**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"▪️︙المستخدم تم كتمه من هنا",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} ▪️︙ تم كتمه من هنا",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**Reason :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@bot.on(admin_cmd(outgoing=True, pattern=r"الغاء كتم(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"الغاء كتم(?: |$)(.*)", allow_sudo=True))
async def endgmute(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("قد تحدث مشاكل غير متوقعة أو أخطاء !")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, "لا استطيع كتم نفسي؟")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event,
            "يرجى الرد على مستخدم أو إضافة اسم المستخدم الخاص به إلى الأمر لإلغاء كتمه",
        )

    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"هـذا المستخدم لـيس مكـتوم هنـا ⌁"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**Error**\n`{str(e)}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"▪️︙المستخدم تم الغاء كتمه من هنا",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} ▪️︙ تم الغاء كتمه من هنا",
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


@bot.on(admin_cmd(incoming=True))
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@bot.on(admin_cmd(pattern=r"طرد(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"طرد(?: |$)(.*)", allow_sudo=True))
async def catgkick(event):
    if event.fwd_from:
        return
    cate = await edit_or_reply(event, "يـتم الـطرد ⌁")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await cate.edit("لـماذا اطـرد نـفسي ⌁")
        return
    if user.id in CAT_ID:
        await cate.edit("لـماذا اطـرد مـطوري ⌁")
        return
    try:
        hmm = base64.b64decode("aHR0cHM6Ly93d3cudC5tZS9VVU5aWg==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    san = []
    san = await admin_groups(event)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cate.edit("`you are not admin of atleast one group` ")
        return
    await cate.edit(
        f"`initiating gkick of the `[user](tg://user?id={user.id}) `in {len(san)} groups`"
    )
    for i in range(sandy):
        try:
            await event.client.kick_participant(san[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {event.chat.title}(`{event.chat_id}`)\n`For kicking there`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {cattaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was gkicked in {count} groups in {cattaken} seconds`!!"
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


CMD_HELP.update(
    {
        "gadmin": "**Plugin : **`gadmin`\
        \n\n•  **Syntax : **`.gban <username/reply/userid> <reason (optional)>`\
        \n•  **Function : **__Bans the person in all groups where you are admin .__\
        \n\n•  **Syntax : **`.ungban <username/reply/userid>`\
        \n•  **Function : **__Reply someone's message with .ungban to remove them from the gbanned list.__\
        \n\n•  **Syntax : **`.listgban`\
        \n•  **Function : **__Shows you the gbanned list and reason for their gban.__\
        \n\n•  **Syntax : **`.gmute <username/reply> <reason (optional)>`\
        \n•  **Function : **__Mutes the person in all groups you have in common with them.__\
        \n\n•  **Syntax : **`.ungmute <username/reply>`\
        \n•  **Function : **__Reply someone's message with .ungmute to remove them from the gmuted list.__\
        \n\n•  **Syntax : **`.gkick <username/reply/userid> <reason (optional)>`\
        \n•  **Function : **__kicks the person in all groups where you are admin .__\
        "
    }
)
