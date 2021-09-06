import sys
from asyncio.exceptions import CancelledError
from time import sleep

from userbot import jmthon

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


@jmthon.ar_cmd(
    pattern="اعادة تشغيل$",
    command=("اعادة تشغيل", plugin_category),
    info={
        "header": "Restarts the bot !!",
        "usage": "{tr}restart",
    },
    disable_errors=True,
)
async def _(event):
    "Restarts the bot !!"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌔︙إعـادة التشغيـل ↻** \n" "**⌯︙تم إعـادة تشغيـل البـوت ↻**")
    RR7PP = await edit_or_reply(
        event,
        "**⌯︙جـاري إعـادة التشغيـل، قـد يستغـرق الأمـر 2-3 دقائـق لاتقم باعـادة التشغيـل مرة اخـرى مـره اخـرى انتـظـر ⏱**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [RR7PP.chat_id, RR7PP.id])
    except Exception as e:
        LOGS.error(e)
    try:
        delgvar("ipaddress")
        await jmthon.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@jmthon.ar_cmd(
    pattern="اطفاء$",
    command=("اطفاء", plugin_category),
    info={
        "header": "Shutdowns the bot !!",
        "description": "To turn off the dyno of heroku. you cant turn on by bot you need to got to heroku and turn on or use @hk_heroku_bot",
        "usage": "{tr}shutdown",
    },
)
async def _(event):
    "Shutdowns the bot"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**⌯︙إيقاف التشغيـل ✕ **\n" "**⌯︙تـم إيقـاف تشغيـل البـوت بنجـاح ✓**")
    await edit_or_reply(event, "**⌯︙جـاري إيقـاف تشغيـل البـوت الآن ..**\n⌯︙ **أعـد تشغيـلي يدويـاً لاحقـاً عـبر هيـروڪو ..**\n⌔︙**سيبقى البـوت متوقفـاً عن العمـل**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)

@jmthon.ar_cmd(
    pattern="التحديثات (تشغيل|ايقاف)$",
    command=("التحديثات", plugin_category),
    info={
        "header": "⌯︙لتحديـث الدردشـة بعـد إعـادة التشغيـل  أو إعـادة التحميـل  ",
        "description": "⌔︙سيتـم إرسـال بنـك cmds ڪـرد على الرسالـة السابقـة الأخيـرة لـ (إعادة تشغيل/إعادة تحميل/تحديث cmds) 💡.",
        "usage": [
            "{tr}التحديثات <تشغيل/ايقاف",
        ],
    },
)
async def set_pmlog(event):
    "⌯︙لتحديـث الدردشـة بعـد إعـادة التشغيـل  أو إعـادة التحميـل  "
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "**⌯︙تـم تعطيـل التـحديـثات بالفعـل ❗️**")
        delgvar("restartupdate")
        return await edit_or_reply(event, "**⌔︙تـم تعطيـل التـحديـثات بنجـاح ✓**")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "**⌔︙تـم تشغيل التـحديـثات بنجـاح ✓**")
    await edit_delete(event, "**⌯︙تـم تشغيل التـحديـثات بالفعـل ❗️**")
