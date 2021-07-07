import sys
from asyncio.exceptions import CancelledError
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
        await event.client.send_message(BOTLOG_CHATID, "#اعـادة الشتغيل \n" "يتم اعادة التشغيل")
    sandy = await edit_or_reply(
        event,
        "تم اعادة التشغيل ارسـل `.بنك` أو `.فحص` لـرؤية البوت اذا اشتغل, غالبا ستأخذ 2-5 دقائق وسيتم تبلغيك بعد التشغيل",
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
        delgvar("ipaddress")
        await catub.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@catub.cat_cmd(
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
        await event.client.send_message(BOTLOG_CHATID, "#الأيقاف \n" "تم تعطيل البوت")
    await edit_or_reply(event, "** تم ايقاف تشغيل البوت 🧸♥\n اذا تريد تفعل فعل من جديد يدويا**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)

# For Catuserbot
# Arabic Translate By  :  @RRRD7
