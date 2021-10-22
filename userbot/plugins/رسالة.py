import base64
from asyncio import sleep

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from .. import jmthon
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper import broadcast_sql as sql
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "tools"

LOGS = logging.getLogger(__name__)

@jmthon.ar_cmd(
    pattern="رسالة(?:\s|$)([\s\S]*)",
    command=("رسالة", plugin_category),
    },
)
async def catbroadcast_add(event):
    "To message to person or to a chat."
    user, reason = await get_user_from_event(event)
    reply = await event.get_reply_message()
    if not user:
        return
    if not reason and not reply:
        return await edit_delete(
            event, "• ماذا تريدني ان ارسل للشخص ؟ اكتب معرف الشخص ومن قم الرسالة الذي تريدها •"
        )
    if reply and reason and user.id != reply.sender_id:
        if BOTLOG:
            msg = await event.client.send_message(BOTLOG_CHATID, reason)
            await event.client.send_message(
                BOTLOG_CHATID,
                "• فشل في ارسال رسالتك الى الشخص ❌ •",
                reply_to=msg.id,
            )
        msglink = await event.clienr.get_msg_link(msg)
        return await edit_or_reply(
            event,
            f"• حدث خطأ في الارسال عد المحاولة •",
        )
    if reason:
        msg = await event.client.send_message(user.id, reason)
    else:
        msg = await event.client.send_message(user.id, reply)
    await edit_delete(event, "• تـم ارسال رسالتك بنجاح ✅ •")
