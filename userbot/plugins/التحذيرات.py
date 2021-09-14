import html

from userbot import jmthon

from ..core.managers import edit_or_reply
from ..sql_helper import warns_sql as sql

plugin_category = "admin"

# Copyright (C) 2021 JepThon TEAM
# FILES WRITTEN BY  @RR7PP

@jmthon.ar_cmd(
    pattern="تحذير(?:\s|$)([\s\S]*)",
    command=("تحذير", plugin_category),
    info={
        "header": "To warn a user.",
        "description": "will warn the replied user.",
        "usage": "{tr}warn <reason>",
    },
)
async def _(event):
    "To warn a user"
    warn_reason = event.pattern_match.group(1)
    if not warn_reason:
        warn_reason = "بـدون سبـب"
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.sender_id, event.chat_id, warn_reason
    )
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: ban user")
            reply = "⌔︙{} التحـذيرات, [المستخـدم](tg://user?id={}) \n ⌯︙تـم طـرده بنـجاح ✅".format(
                limit, reply_message.sender_id
            )
        else:
            logger.info("TODO: ban user")
            reply = "⌯︙{} التحـذيرات [المستخـدم](tg://user?id={})\n ⌯︙تـم حظـره بنـجاح ✅!".format(
                limit, reply_message.sender_id
            )
    else:
        reply = "⌯︙[المـستخدم](tg://user?id={}) لـديه {}/{} من التحذيـرات ".format(
            reply_message.sender_id, num_warns, limit
        )
        if warn_reason:
            reply += "\nسبـب أخـر تحـذير:\n{}".format(html.escape(warn_reason))
    await edit_or_reply(event, reply)
#ملف التحذيرات بواسطه جـيبثون

@jmthon.ar_cmd(
    pattern="التحذيرات",
    command=("التحذيرات", plugin_category),
    info={
        "header": "To get users warns list.",
        "usage": "{tr}warns <reply>",
    },
)
async def _(event):
    "To get users warns list"
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if not result or result[0] == 0:
        return await edit_or_reply(event, "⌯︙هذا الشخص ليس لديه اي تحذيرات")
    num_warns, reasons = result
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    if not reasons:
        return await edit_or_reply(
            event,
            "⌯︙هـذا الـمستخدم {} / {} من الـتحذيرات و بـدون اي سبب ".format(
                num_warns, limit
            ),
        )

    text = "⌯︙هـذا الـمستخدم {}/{} من الـتحذيرات, للأسـباب التاليـة:".format(
        num_warns, limit
    )
    text += "\r\n"
    text += reasons
    await event.edit(text)


@jmthon.ar_cmd(
    pattern="حذف التحذيرات$",
    command=("حذف التحذيرات", plugin_category),
    info={
        "header": "To reset warns of the replied user",
        "usage": [
            "{tr}rwarns",
            "{tr}resetwarns",
        ],
    },
)
async def _(event):
    "To reset warns"
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await edit_or_reply(event, "⌯︙تـم حـذف الـتحذيرات بـنجـاح")
