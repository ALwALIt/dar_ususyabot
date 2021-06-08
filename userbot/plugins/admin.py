from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**الصورة صغيرة جدًا** ."
PP_ERROR = "**فشل أثناء معالجة الصورة** ."
NO_ADMIN = "**أنا لست مشرف هنا!!** ."
NO_PERM = "**ليس لدي أذونات كافية!** ."
CHAT_PP_CHANGED = "**تغيرت صورة الدردشة** ⌁."
INVALID_MEDIA = "**ملحق غير صالح** ."

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

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

plugin_category = "admin"
# ================================================


@catub.cat_cmd(
    pattern="ضع( صورة| -d)$",
    command=("gpic", plugin_category),
    info={
        "header": "لوضع صوره للمجموعه ",
        "description": "قم بالرد على الصوره المراد وضعها",
        "flags": {
            "ضع صوره": "لوضع صوره للمجموعة ",
            "-d": "To delete group pic",
        },
        "usage": [
            "{tr}ضع صوره <بالرد على الصوره>",
            "{tr}gpic -d",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**Error : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**خطأ : **`{str(e)}`")
        process = "deleted"
        await edit_delete(event, "**تـم حذف الـصورة بنـجاح ✅")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#صوره_المجموعة\n"
            f"صورة المجموعه {process} بنجاح "
            f"الدردشه: {event.chat.title}(`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="رفع مشرف(?: |$)(.*)",
    command=("رفع مشرف", plugin_category),
    info={
        "الامر": "لرفع الشخص مشرف مع صلاحيات",
        "الشرح": "لرفع الشخص مشرف بالمجموعه قم بالرد على الشخص\
            \nNote : You need proper rights for this",
        "الاستخدام": [
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه>",
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "لرف الشخص مشرف بالمجموعه"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin"
    if not user:
        return
    catevent = await edit_or_reply(event, "**يـتم الرفـع**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**تم رفعه مشرف بالمجموعه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PROMOTE\
            \nUSER: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {event.chat.title} (`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="تك(?: |$)(.*)",
    command=("تك", plugin_category),
    info={
        "الامر": "لتنزيل الشخص كن الاشراف",
        "الشرح": "يقوم هذا الامر بحذف جميع صلاحيات المشرف\
            \nملاحظه :**لازم تكون انت الشخص الي رفعه او تكون مالك المجموعه حتى تنزله**",
        "الاستخدام": [
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "لتنزيل الشخص من رتبة الادمن"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**يـتم التنزيل من الاشراف**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("**-  تـم تنزيله من قائمه الادمنيه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تنزيل_مشرف\
            \nالمعرف: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشه: {event.chat.title}(`{event.chat_id}`)",
        )

#جميع الحقوق محفوظه لقناه جـ مـ ثـ و نـ @ J M T H O N
@catub.cat_cmd(
    pattern="حظر(?: |$)(.*)",
    command=("حظر", plugin_category),
    info={
        "header": "Will ban the guy in the group where you used this command.",
        "description": "Permanently will remove him from this group and he can't join back\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}ban <userid/username/reply>",
            "{tr}ban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "To ban a person in group"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "__لا يمكنك حظر نفسك 💞🌿__")
    catevent = await edit_or_reply(event, "** اتمنالك الخير ☹️🤍**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "**- ليس لدي صلاحيات كامله لكنه لا يزال محظور 🌿💘**"
        )
    if reason:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} **تم حظـره بنـجاح ✅ !!**\n**الـسبب : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} **تم حظـره بنـجاح ✅ !!**"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#حظـر\
                \nالمـستخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالدردشـه: {event.chat.title}(`{event.chat_id}`)\
                \nالسـبب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nالمـستخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالدردشـه: {event.chat.title}(`{event.chat_id}`)",
            )

#جميع الحقوق محفوظه لمحمد الزهيري @R R R D 7
@catub.cat_cmd(
    pattern="الغاء حظر(?: |$)(.*)",
    command=("الغاء حظر", plugin_category),
    info={
        "header": "Will unban the guy in the group where you used this command.",
        "description": "Removes the user account from the banned list of the group\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}unban <userid/username/reply>",
            "{tr}unban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "To unban a person"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**- جاري الغاء الحظر انتظر رجاءا 🌿💕**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} **- تم الغاء الحظر بنجاح يمكنه الرجوع الان ✅**"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الـغاء_الحـظر\n"
                f"المـستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الدردشـه: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("**عذرا تم الغاء عمليه الحظر !**")
    except Exception as e:
        await catevent.edit(f"**خطأ :**\n`{e}`")


@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@catub.cat_cmd(
    pattern="كتم(?: |$)(.*)",
    command=("كتم", plugin_category),
    info={
        "header": "To stop sending messages from that user",
        "description": "If is is not admin then changes his permission in group,\
            if he is admin or if you try in personal chat then his messages will be deleted\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}mute <userid/username/reply>",
            "{tr}mute <userid/username/reply> <reason>",
        ],
    },  # sourcery no-metrics
)
async def startmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        await event.edit("**قد تحدث مشاكل غير متوقعة أو أخطاء 🙁🌿**")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**- تم كتم المستخدم بنجاح سيتم حذف جميع رسائله** ✅"
            )
        if event.chat_id == catub.uid:
            return await edit_delete(event, "- عذرا لا يمكن كتم هذا الشخص 😐💞**")
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**حدث خطا **\n`{str(e)}`")
        else:
            await event.edit("**¦ تم كتم هذا الشخص بنجاح لا يمكنه التكلم هنا 💞🌿**")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#المستخدمين_المكتومين\n"
                f"**المستخدم :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await edit_or_reply(
                event, "**- لا يمكنك كتم هذا الشخص بدون صلاحيات الحذف 🌿**"
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "**- عذرا لا يمكنني كتم نفسي اسف 💕🤍**")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "**- تم كتم هذا الشخص بنجاح لا يمكنه التكلم هنا 💞🌿**"
            )
        result = await event.client(
            functions.channels.GetParticipantRequest(event.chat_id, user.id)
        )
        try:
            if result.participant.banned_rights.send_messages:
                return await edit_or_reply(
                    event,
                    "**- هذا الشخص مكتوم بالفعل في هذه الدردشه ✅**",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await edit_or_reply(event, f"**حدث خطا : **`{str(e)}`", 10)
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "**- لا يمكنك كتم هذا الشخص بدون صلاحيات الحذف 🌿**",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "**- لا يمكنك كتم هذا الشخص بدون صلاحيات الحذف 🌿**"
                )
            mute(user.id, event.chat_id)
        except Exception as e:
            return await edit_or_reply(event, f"**حدث خطا : **`{str(e)}`", 10)
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} **تم كتمه في {event.chat.title}**\n"
                f"**الـسبب**:{reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} **تم كتمه في {event.chat.title}**\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الـكتم\n"
                f"**المستخدم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الدردشه :** {event.chat.title}(`{event.chat_id}`)",
            )


@catub.cat_cmd(
    pattern="الغاء كتم(?: |$)(.*)",
    command=("الغاء كتم", plugin_category),
    info={
        "header": "To allow user to send messages again",
        "description": "Will change user permissions ingroup to send messages again.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}unmute <userid/username/reply>",
            "{tr}unmute <userid/username/reply> <reason>",
        ],
    },
)
async def endmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        await event.edit("**- قد تحدث مشاكل غير متوقعة أو أخطاء 🙁🌿**")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**- هذا الشخص غير مكتوم اصلا في هذه الدردشه ✅**"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**خطأ **\n`{str(e)}`")
        else:
            await event.edit(
                "**- تم كتم المستخدم بنجاح سيتم حذف جميع رسائله** ✅"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#المستخدمين_غير_المحظورين\n"
                f"**المستخدمين :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client(
                    functions.channels.GetParticipantRequest(
                        channel=event.chat_id, user_id=user.id
                    )
                )
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await edit_or_reply(
                event,
                "**- لا توجد اي قيود على هذا الشخص 🍯🤍**",
            )
        except Exception as e:
            return await edit_or_reply(event, f"**خطأ : **`{str(e)}`")
        await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} **تم الغاء كتمه في {event.chat.title}",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#المستخدمين_غير_المكتومين\n"
                f"**المستخدمين :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الدردشه :** {event.chat.title}(`{event.chat_id}`)",
            )


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
    "use this to kick a user from chat"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**- جار طرد هذا الشخص من المجموعة 💘⚕️**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"**تم طرد [{user.first_name}](tg://user?id={user.id}) بنجاح ✅**n\السـبب: {reason}"
        )
    else:
        await catevent.edit(f"**تم طرد [{user.first_name}](tg://user?id={user.id}) بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#المطرودين\n"
            f"المستخدمين: [{user.first_name}](tg://user?id={user.id})\n"
            f"الدردشة: {event.chat.title}(`{event.chat_id}`)\n",
        )


@catub.cat_cmd(
    pattern="تثبيت( بالاشعار|$)",
    command=("pin", plugin_category),
    info={
        "header": "For pining messages in chat",
        "description": "reply to a message to pin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"loud": "To notify everyone without this.it will pin silently"},
        "usage": [
            "{tr}pin <reply>",
            "{tr}pin loud <reply>",
        ],
    },
)
async def pin(event):
    "To pin a message in chat"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "**- يرجى الرد على الرسالة التي تريد تثبيتها ⚕️**", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**- تم تثبيت الرسالة بنجاح في هذه الدردشة ✅**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PIN\
                \n__Succesfully pinned a message in chat__\
                \nCHAT: {event.chat.title}(`{event.chat_id}`)\
                \nLOUD: {is_silent}",
        )


@catub.cat_cmd(
    pattern="الغاء التثبيت( للكل|$)",
    command=("الغاء التثبيت", plugin_category),
    info={
        "header": "For unpining messages in chat",
        "description": "reply to a message to unpin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"all": "To unpin all messages in the chat"},
        "usage": [
            "{tr}unpin <reply>",
            "{tr}unpin all",
        ],
    },
)
async def pin(event):
    "To unpin message(s) in the group"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edit_delete(
            event,
            "يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`__ لالغاء تثبيت جميع الرسائل__ ⚕️",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event, "يرجى الرد على الرسالة التي تريد تثبيتها او استخدم `.الغاء التثبيت للكل`__ لالغاء تثبيت جميع الرسائل__ ⚕️", 5
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**- تم الغاء التثبيت بنجاح ✅**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#UNPIN\
                \n__Succesfully unpinned message(s) in chat__\
                \nCHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="الاحداث( -ر)?(?: |$)(\d*)?",
    command=("الاحداث", plugin_category),
    info={
        "header": "To get recent deleted messages in group",
        "description": "To check recent deleted messages in group, by default will show 5. you can get 1 to 15 messages.",
        "flags": {
            "u": "use this flag to upload media to chat else will just show as media."
        },
        "usage": [
            "{tr}undlt <count>",
            "{tr}undlt -u <count>",
        ],
        "examples": [
            "{tr}undlt 7",
            "{tr}undlt -u 7 (this will reply all 7 messages to this message",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "To check recent deleted messages in group"
    catevent = await edit_or_reply(event, "**- يتم البحث عن اخر الاحداث انتظر ⚕️**")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**اخر {lim} رسائل محذوفة في هذه المجموعة :**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(catevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(catevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )