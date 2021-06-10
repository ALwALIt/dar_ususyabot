import sys
from time import sleep

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP

LOGS = logging.getLogger(__name__)
plugin_category = "tools"


@catub.cat_cmd(
    pattern="اعاده تشغيل$",
    command=("اعاده تشغيل", plugin_category),
    info={
        "header": "Restarts the bot !!",
        "usage": "{tr}restart",
    },
)
async def _(event):
    "Restarts the bot !!"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    sandy = await edit_or_reply(
        event,
        "للتحقق مما إذا كنت متصلاً بالإنترنت ، يستغرق الأمر في الواقع 1-2 دقيقة لإعادة التشغيل",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    try:
        await catub.disconnect()
    except Exception as e:
        LOGS.error(e)

@catub.cat_cmd(
    pattern="سليب( [0-9]+)?$",
    command=("سليب", plugin_category),
    info={
        "header": "سوف يتوقف Userbot عن العمل في الوقت المذكور",
        "usage": "{tr}sleep <seconds>",
        "examples": "{tr}sleep 60",
    },
)
async def _(event):
    "To sleep the userbot"
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "بناء الجملة: وقت .سليب`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "لقد وضعت الروبوت في وضع السكون  " + str(counter) + " ثواني",
        )
    event = await edit_or_reply(event, f"`اوك, دعني أنام لأجل {counter} ثواني`")
    sleep(counter)
    await event.edit("`حسنًا ، أنا مستيقظ الآن.`")


@catub.cat_cmd(
    pattern="notify (on|off)$",
    command=("notify", plugin_category),
    info={
        "header": "To update the your chat after restart or reload .",
        "description": "Will send the ping cmd as reply to the previous last msg of (restart/reload/update cmds).",
        "usage": [
            "{tr}notify <on/off>",
        ],
    },
)
async def set_pmlog(event):
    "To update the your chat after restart or reload ."
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "__Notify was already disabled__")
        delgvar("restartupdate")
        return await edit_or_reply(event, "__Notify was disabled succesfully.__")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "__Notify was enabled succesfully.__")
    await edit_delete(event, "__Notify was already enabled.__")
