# ported from paperplaneExtended by avinashreddy3108 for media support
import re

from userbot import catub

from ..core.managers import edit_or_reply
from ..sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"


@catub.cat_cmd(incoming=True)
async def filter_incoming_handler(handler):
    try:
        if (
            not (await handler.get_sender()).bot
            and (handler.sender_id) != handler.client.uid
        ):
            name = handler.raw_text
            filters = get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    if trigger.f_mesg_id:
                        msg_o = await handler.client.get_messages(
                            entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                        )
                        await handler.reply(msg_o.message, file=msg_o.media)
                    elif trigger.reply:
                        await handler.reply(trigger.reply)
    except AttributeError:
        pass


@catub.cat_cmd(
    pattern="اضف رد (.*)",
    command=("اضف رد", plugin_category),
    info={
        "header": "To save filter for the given keyword.",
        "description": "If any user sends that filter then your bot will reply.",
        "note": "For saving media/stickers as filters you need to set PRIVATE_GROUP_BOT_API_ID.",
        "usage": "{tr}filter <keyword>",
    },
)
async def add_new_filter(new_handler):
    "To save the filter"
    keyword = new_handler.pattern_match.group(1)
    string = new_handler.text.partition(keyword)[2]
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await new_handler.client.send_message(
                BOTLOG_CHATID,
                f"#الــرد\
            \nايدي الدردشه: {new_handler.chat_id}\
            \nTRIGGER: {keyword}\
            \n\nالرسالة التليه حفظت كرد ارسل معلومات الرد لرؤية الرد  ،  لاتقم بحذف ارسالة !!",
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                new_handler,
                "يتطلب حفظ الوسائط كرد على عامل التصفية تعيين PRIVATE_GROUP_BOT_API_ID\n قـم بعمل مجموعه وقم باخذ ايدي المجموعه عبر اي بوت بعدها ارسل\n .set var PRIVATE_GROUP_BOT_API_ID + ايدي المجموعة ",
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "الـرد **{}** {} تـم اضـافتة بنـجـاح ✅"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "added"))
    remove_filter(str(new_handler.chat_id), keyword)
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "Updated"))
    await edit_or_reply(new_handler, f"خطـأ اثنـاء تعيـن الـرد {keyword}"  ⚠️")


@catub.cat_cmd(
    pattern="الردود$",
    command=("الردود", plugin_category),
    info={
        "header": "To list all filters in that chat.",
        "description": "Lists all active (of your userbot) filters in a chat.",
        "usage": "{tr}filters",
    },
)
async def on_snip_list(event):
    "To list all filters in that chat."
    OUT_STR = "**لا توجد ردود مضافة في هذه الدردشه  🔍**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "لا توجد ردود مضافة في هذه الدردشه  🔍":
            OUT_STR = "الردود التي تم اضافتها في هذه الدردش :\n"
        OUT_STR += "👉 `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="Available Filters in the Current Chat",
        file_name="filters.text",
    )


@catub.cat_cmd(
    pattern="حذف رد (.*)",
    command=("حذف رد", plugin_category),
    info={
        "header": "To delete that filter . so if user send that keyword bot will not reply",
        "usage": "{tr}stop <keyword>",
    },
)
async def remove_a_filter(r_handler):
    "Stops the specified keyword."
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("الـرد` {} `غير موجود.  🙁🤍 .".format(filt))
    else:
        await r_handler.edit("**الـرد `{} `تـم حـذفة بنـجـاح  ✅**".format(filt))


@catub.cat_cmd(
    pattern="حذف الردود$",
    command=("حذف الردود", plugin_category),
    info={
        "header": "To delete all filters in that group.",
        "usage": "{tr}rmfilters",
    },
)
async def on_all_snip_delete(event):
    "To delete all filters in that group."
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, f"**تم حذف الردود في الدردشة الحالية بنجاح  ✅**")
    else:
        await edit_or_reply(event, f"**لا توجد ردود في هذه المجموعة  🙃🤍**")
