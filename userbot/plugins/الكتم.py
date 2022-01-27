import base64
import asyncio
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

from userbot import jmthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

plugin_category = "admin"

#=================== الكـــــــــــــــتم  ===================  #

@jmthon.ar_cmd(
    pattern="كتم(?:\s|$)([\s\S]*)",
    command=("كتم", plugin_category),
)
async def startgmute(event):
    "To mute a person in all groups where you are admin."
    if event.is_private:
        await event.edit("**𖡛... قـد تحـدث بعـض المـشاكـل أو الأخـطاء ...𖡛**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == 705475246:
            return await edit_delete(event, "**- لا يمڪنني كتم مطـوري يافرخ دي لك**")
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "**𖡛... . لمـاذا تࢪيـد كتم نفسـك؟  ...𖡛**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "**𖡛... غيـر قـادر عـلى جـلب مـعلومات الـشخص ...𖡛**")
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**𖡛... هـذا الشـخص مكـتوم بـنجاح ...𖡛**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خـطأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"** تـم كـتم الـمستخـدم بـنجاح  ،🔕 **",
            )
        else:
            await edit_or_reply(
                event,
                f"** تـم كـتم الـمستخـدم بـنجاح  ،🔕 **",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                " الـكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                " الـكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)

#=================== الغـــــــــــــاء الكـــــــــــــــتم  ===================  #

@jmthon.ar_cmd(
    pattern="الغاء كتم(?:\s|$)([\s\S]*)",
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
        await event.edit("**𖡛... قـد تحـدث بعـض المـشاكـل أو الأخـطاء ...𖡛**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "**𖡛... لمـاذا تࢪيـد كتم نفسـك؟ ...𖡛**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "**𖡛... غيـࢪ قـادࢪ عـلى جـلب مـعلومات الـشخص ...𖡛**")
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"**𖡛... هـذا الشـخص غيـࢪ مكـتوم اصلا  ...𖡛**"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطـأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"** تـم الغـاء كـتم الـمستخـدم بـنجاح  🔔، **",
            )
        else:
            await edit_or_reply(
                event,
                f"** تـم الـغاء كتـم  الـمستخـدم بـنجاح  🔔، **",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "، الغـاء الـكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                " الغـاء الـكتم \n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )

# ===================================== # 

@jmthon.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()

#=====================================  #
