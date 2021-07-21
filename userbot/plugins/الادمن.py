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

from userbot import jmthon

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**⌔︙ الصورة صغيرة جدًا** "
PP_ERROR = "**⌔︙ فشل أثناء معالجة الصورة** "
NO_ADMIN = "**⌔︙ أنا لست مشرف هنا!!** "
NO_PERM = "**⌔︙ ليس لدي أذونات كافية!** "
CHAT_PP_CHANGED = "**⌔︙ تم تغيير صورة الدردشة بنجاح ✅**"
INVALID_MEDIA = "**⌔︙ ملحق غير صالح** "

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
#admin plugin for  jmthon
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

plugin_category = "اوامر الادمن"
# ================================================


@jmthon.ar_cmd(
    pattern="الصورة( -وضع| -حذف)$",
    command=("الصورة", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "For changing group display pic or deleting display pic",
        "⌔︙ الشـرح": "Reply to Image for changing display picture",
        "flags": {
            "-s": "To set group pic",
            "-d": "To delete group pic",
        },
        "⌔︙ الأمـر": [
            "{tr}الصورة -وضع <reply to image>",
            "{tr}gpic -حذف",
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
                return await edit_delete(event, f"**خـطأ : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**خـطأ : **`{str(e)}`")
        process = "deleted"
        await edit_delete(event, "**⌔︙ تـم حذف الـصورة بنـجاح ✅")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#صوره_المجموعة\n"
            f"صورة المجموعه {process} بنجاح "
            f"الدردشه: {event.chat.title}(`{event.chat_id}`)",
        )


@jmthon.ar_cmd(
    pattern="رفع مشرف(?:\s|$)([\s\S]*)",
    command=("رفع مشرف", plugin_category),
    info={
        "الامر": "⌔︙ لرفع الشخص مشرف مع صلاحيات",
        "الشرح": "⌔︙ لرفع الشخص مشرف بالمجموعه قم بالرد على الشخص\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر",
        "الاستخدام": [
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه>",
            "{tr}رفع مشرف <ايدي/معرف/بالرد عليه> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)#admin plugin for  jmthon
async def promote(event):
    "⌔︙ لـرفع مستـخدم مشـرف في الـكروب"
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
            f"#الـرفـع\
            \nالـمستخـدم: [{user.first_name}](tg://user?id={user.id})\
            \nالـدردشـة: {event.chat.title} (`{event.chat_id}`)",
        )


@jmthon.ar_cmd(
    pattern="تك(?:\s|$)([\s\S]*)",
    command=("تك", plugin_category),
    info={
        "الامر": "⌔︙ لتنزيل الشخص كن الاشراف",
        "الشرح": "⌔︙ يقوم هذا الامر بحذف جميع صلاحيات المشرف\
            \n⌔︙ ملاحظه :**لازم تكون انت الشخص الي رفعه او تكون مالك المجموعه حتى تنزله**",
        "الاستخدام": [
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
            "{tr}تك <الايدي/المعرف/بالرد عليه>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "⌔︙ لـتنزيـل شـخص من الأشـراف"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "**⌔︙ يـتم التنزيل من الاشراف**")
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
    await catevent.edit("**⌔︙ تـم تنزيله من قائمه الادمنيه بنجاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تنزيل_مشرف\
            \nالمعرف: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشه: {event.chat.title}(`{event.chat_id}`)",
        )


@jmthon.ar_cmd(
    pattern="حظر(?:\s|$)([\s\S]*)",
    command=("حظر", plugin_category),
    info={
        "⌔︙ الاستخدام": "يقـوم بـحظر شخـص في الـكروب الءي اسـتخدمت فيـه الامر.",
        "⌔︙ الشرح": "لحـظر شخـص من الكـروب ومـنعه من الأنـضمام مجـددا\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الامر": [
            "{tr}حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}حظر <الايدي/المعرف/بالرد عليه> <السبب>",
        ],
    },
    groups_only=True,
    require_admin=True,
) #admin plugin for  jmthon
async def _ban_person(event):
    "⌔︙ لحـظر شخص في كـروب مـعين"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "⌔︙ عـذرا لا تسـتطيع حـظر شـخص")
    catevent = await edit_or_reply(event, "⌔︙ تـم حـظره بـنجاح")
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
            "⌔︙ ليـس لـدي جـميع الصـلاحيـات لكـن سيـبقى محـظور"
        )
    if reason:
        await catevent.edit(
            f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم حـظره بنـجاح !!\n**⌔︙السبب : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"⌔︙ المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n ⌔︙ تـم حـظره بنـجاح ✅"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \nايدي الكروب(`{event.chat_id}`)\
                \nالسبـب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙ الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \n ايـدي الكـروب: (`{event.chat_id}`)",
            )


@jmthon.ar_cmd(
    pattern="الغاء حظر(?:\s|$)([\s\S]*)",
    command=("الغاء حظر", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "يقـوم بـالغاء حـظر الشـخص في الـكروب الذي اسـتخدمت فيـه الامر.",
        "⌔︙ الشرح": "لألـغاء حـظر شخـص من الكـروب والسـماح له من الأنـضمام مجـددا\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه>",
            "{tr}الغاء حظر <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "⌔︙ لألـغاء الـحظر لـشخص في كـروب مـعين"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "⌔︙ جـار الـغاء الـحظر أنتـظر")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"⌔︙ الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الـغاء حـظره بنـجاح "
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـغاء الـحظر \n"
                f"الـمستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الـدردشـة: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("⌔︙ يـبدو أن هذه الـعمليـة تم إلغاؤهـا")
    except Exception as e:
        await catevent.edit(f"**خـطأ :**\n`{e}`")


@jmthon.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))

#admin plugin for  jmthon
@jmthon.ar_cmd(
    pattern="كتم(?:\s|$)([\s\S]*)",
    command=("كتم", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "To stop sending messages from that user",
        "⌔︙ الشـرح": "If is is not admin then changes his permission in group,\
            if he is admin or if you try in personal chat then his messages will be deleted\
            \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}كتم <الايدي/المعرف/بالرد عليه>",
            "{tr}كتم <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },  # sourcery no-metrics
)
async def startmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        await event.edit("⌔︙ قـد تـكون هـنالك بـعض المـشاكل والأخطـاء")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "⌔︙ هـذا الـشخص بالـفعـل مكـتوم"
            )
        if event.chat_id == jmthon.uid:
            return await edit_delete(event, "⌔︙ لا يـمكنك حـظر نـفسك")
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**خـطأ **\n`{str(e)}`")
        else:
            await event.edit("⌔︙ تـم كـتم الـمستـخدم بـنجاح ✅")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـكتم \n"
                f"**المسـتخدم :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await edit_or_reply(
                event, "⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر"
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "⌔︙ لا يـمكنك حـظر نـفسك")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "⌔︙ هـذا الـشخص بالـفعـل مكـتوم"
            )
        result = await event.client(
            functions.channels.GetParticipantRequest(event.chat_id, user.id)
        )
        try:
            if result.participant.banned_rights.send_messages:
                return await edit_or_reply(
                    event,
                    "⌔︙ هـذا الـشخص بالـفعـل مكـتوم",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await edit_or_reply(event, f"**خـطأ : **`{str(e)}`", 10)
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "⌔︙ تـحتاج صـلاحـيات الـحذف لـهذا الأمـر",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر "
                )
            mute(user.id, event.chat_id)
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{str(e)}`", 10)
        if reason:
            await edit_or_reply(
                event,
                f"⌔︙ الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم كتمه بنـجاح\n ⌔︙ الدردشـة {event.chat.title}\n"
                f"⌔︙ السـبب: {reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"⌔︙ الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم كتمه بنـجاح ✅\n ⌔︙ الدردشـة {event.chat.title}"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـكتم\n"
                f"**الـمستخدم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الـدردشـة :** {event.chat.title}\n"
                f"**ايدي الكروب:** (`{event.chat_id}`)",
            )

#admin plugin for  jmthon
@jmthon.ar_cmd(
    pattern="الغاء كتم(?:\s|$)([\s\S]*)",
    command=("الغاء كتم", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "لألـغاء كتـم الشـخص ",
        "⌔︙ الشـرح": "لألـغاء كتـم الشـخص في الـمجموعة الذي تـرسل الأمر بهـا.\
        \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}الغاء كتم <الايدي/المعرف/بالرد عليه>",
            "{tr}الغاء كتم <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
)
async def endmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        await event.edit("⌔︙ قـد تـحدث بعـض الأخـطاء")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "⌔︙ هـذا الـمستخدم لـيس مكـتوم"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**خـطأ **\n`{str(e)}`")
        else:
            await event.edit(
                "⌔︙ تـم الـغاء كـتم الـمستـخدم بـنجاح"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـغاء الكـتم\n"
                f"**الـمستخدم :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
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
                    functions.channels.GetParticipantRequest(event.chat_id, user.id)
                )
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await edit_or_reply(
                event,
                "⌔︙ هـذا الـمستخدم يسـتطيع الـتحدث بِـحريـة هـنا",
            )
        except Exception as e:
            return await edit_or_reply(event, f"**خـطأ : **`{str(e)}`")
        await edit_or_reply(
            event,
            f"**⌔︙ الـمستخدم** {_format.mentionuser(user.first_name ,user.id)}\n ⌔︙ تـم الـغاء كتـمه\n **⌔︙ الدردشة** {event.chat.title}",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "⌔︙ الـغاء الكـتم\n"
                f"**المـستخدم :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**الـدردشـة :** {event.chat.title}(`{event.chat_id}`)",
            )
#admin plugin for  jmthon

@jmthon.ar_cmd(
    pattern="طرد(?:\s|$)([\s\S]*)",
    command=("طرد", plugin_category),
    info={
        "⌔︙ الأسـتخدام": "لـطرد شـخض من الـكروب",
        "⌔︙ الشـرح": "لـطرد شخص من المـجموعة يستطيع الأنضـمام مرة اخـرى.\
        \n⌔︙ تـحتاج الصلاحـيات لـهذا الأمـر.",
        "⌔︙ الأمـر": [
            "{tr}طرد <الايدي/المعرف/بالرد عليه>",
            "{tr}طرد <الايدي/المعرف/بالرد عليه> <السبب> ",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "لـطرد شـخض من الـكروب"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "⌔︙ يـتم طـرد الـمستخدم أنتـظر")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{str(e)}")
    if reason:
        await catevent.edit(
            f"⌔︙ الـمستخدم [{user.first_name}](tg://user?id={user.id})\n ⌔︙ تـم طرده بنجاح ✅ \n⌔︙ السـبب : {reason}"
        )
    else:
        await catevent.edit(f"⌔︙ الـمستخدم [{user.first_name}](tg://user?id={user.id})\n ⌔︙ تـم طرده بنجاح ✅ ")
