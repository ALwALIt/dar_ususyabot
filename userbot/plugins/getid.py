from telethon.utils import pack_bot_file_id

from userbot import catub
from userbot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

LOGS = logging.getLogger(__name__)


@catub.cat_cmd(
    pattern="(get_id|هوية شخصية)(?: |$)(.*)",
    command=("هوية شخصية", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "إذا تم إدخال إدخال ثم يعرض معرف تلك الدردشة / القناة / مستخدم آخر إذا قمت بالرد على المستخدم ثم يعرض معرف المستخدم الذي تم الرد عليه
    مع معرف الدردشة الحالي وإذا لم يتم الرد على المستخدم أو إدخال إدخال معين ، فما عليك سوى إظهار معرف الدردشة حيث استخدمت الأمر",
        "usage": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get id of the group or user."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{str(e)}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"The id of the user `{input_str}` is `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"The id of the chat/channel `{p.title}` is `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "`أدخل إما اسم مستخدم أو الرد على المستخدم`")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**معرف الدردشة الحالي : **`{str(event.chat_id)}`\n**من معرف المستخدم : **`{str(r_msg.sender_id)}`\n**ميديا فايل ID: **`{bot_api_file_id}`",
            )
        else:
            await edit_or_reply(
                event,
                f"**معرف الدردشة الحالي : **`{str(event.chat_id)}`\n**من معرف المستخدم : **`{str(r_msg.sender_id)}`",
            )
    else:
        await edit_or_reply(event, f"**معرف الدردشة الحالي : **`{str(event.chat_id)}`")
