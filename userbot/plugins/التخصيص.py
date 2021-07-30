from urlextract import URLExtract
from validators.url import url

from userbot import jmthon
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER

extractor = URLExtract()
vlist = [
    "ALIVE_PIC",
    "ALIVE_EMOJI",
    "ALIVE_TEXT",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "MAX_FLOOD_IN_PMS",
    "START_TEXT",
    "CUSTOM_STICKER_PACKNAME",
    "- BY  @JMTHON  ",
]
#ملف التخصيص لسورس جمثون
oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}


@jmthon.ar_cmd(
    pattern="(اضف_|معلومات_|حذف_)فار(?: |$)([\s\S]*)",
    command=("فار", plugin_category),
    info={
        "header": "Set vars in database or Check or Delete",
        "description": "Set , Fetch or Delete values or vars directly in database without restart or heroku vars.\n\nYou can set multiple pics by giving space after links in alive, ialive, pm permit.",
        "flags": {
            "set": "To set new var in database or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
        },
        "var name": "[list of vars](https://catuserbot.gitbook.io/catuserbot/data-vars-setup)",
        "usage": [
            "{tr}setdv <var name> <var value>",
            "{tr}getdv <var name>",
            "{tr}deldv <var name>",
        ],
        "examples": [
            "{tr}setdv ALIVE_PIC <pic link>",
            "{tr}setdv ALIVE_PIC <pic link 1> <pic link 2>",
            "{tr}getdv ALIVE_PIC",
            "{tr}deldv ALIVE_PIC",
        ],
    },
)
async def bad(event):  # sourcery no-metrics
    "To manage vars in database"
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edit_delete(
            event, f"**📑 يجب وضع اسم المتغير الصحيح من هذه القائمه :\n\n**{vnlist}", time=60
        )
    vinfo = None
    if " " in vname:
        vname, vinfo = vname.split(" ", 1)
    reply = await event.get_reply_message()
    if not vinfo and reply:
        vinfo = reply.text
    if vname in vlist:
        if vname in oldvars:
            vname = oldvars[vname]
        if cmd == "اضف_":
            if not vinfo:
                return await edit_delete(
                    event, f"** يجب وضع اسم المتغير اولا لاستخدامه لـ **{vname}**"
                )
            check = vinfo.split(" ")
            for i in check:
                if (("PIC" in vname) or ("pic" in vname)) and not url(i):
                    return await edit_delete(event, "**قم بوضع رابط صحيح او وضع رابط تلكراف**")
            addgvar(vname, vinfo)
            await edit_delete(
                event, f"📑 القيـمة لـ **{vname}** \n تـم تغييـرها لـ :- `{vinfo}`", time=20
            )
        if cmd == "معلومات_":
            var_data = gvarstatus(vname)
            await edit_delete(
                event, f"📑 قيـمة الـ **{vname}** \n هي  `{var_data}`", time=20
            )
        elif cmd == "حذف_":
            delgvar(vname)
            await edit_delete(
                event,
                f"📑 قيـمة الـ **{vname}** \n تم حذفها ووضع القيمه الاصلية لها",
                time=20,
            )
    else:
        await edit_delete(
            event, f"**📑 يـجب وضع المتغير الصحـيح من هذه الـقائمة :\n\n**{vnlist}", time=60
        )
#ملف التخصيص لسورس جمثون 

@jmthon.ar_cmd(
    pattern="تخصيص (pmpermit|pmpic|pmblock|startmsg)$",
    command=("تخصيص", plugin_category),
    info={
        "header": "To customize your CatUserbot.",
        "options": {
            "pmpermit": "To customize pmpermit text. ",
            "pmblock": "To customize pmpermit block message.",
            "startmsg": "To customize startmsg of bot when some one started it.",
            "pmpic": "To customize pmpermit pic. Reply to media url or text containing media.",
        },
        "custom": {
            "{mention}": "mention user",
            "{first}": "first name of user",
            "{last}": "last name of user",
            "{fullname}": "fullname of user",
            "{username}": "username of user",
            "{userid}": "userid of user",
            "{my_first}": "your first name",
            "{my_last}": "your last name ",
            "{my_fullname}": "your fullname",
            "{my_username}": "your username",
            "{my_mention}": "your mention",
            "{totalwarns}": "totalwarns",
            "{warns}": "warns",
            "{remwarns}": "remaining warns",
        },
        "usage": [
            "{tr}custom <option> reply",
        ],
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_catuserbot(event):
    "To customize your CatUserbot."
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.text
    if not reply and text:
        return await edit_delete(event, "⌔︙ قم بالرد على الكتابة او الرابط اولا ")
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        addgvar("pmpermit_txt", text)
    if input_str == "pmblock":
        addgvar("pmblock", text)
    if input_str == "startmsg":
        addgvar("START_TEXT", text)
    if input_str == "pmpic":
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(event, "⌔︙ الرابط المـرسل غيـر مدعـوم ❕", 5)
        addgvar("pmpermit_pic", urls)
    await edit_or_reply(event, f"⌔︙ تم تحـديث التخصـيص الخاص بنك بـنجاح ✅ ")


@jmthon.ar_cmd(
    pattern="ازالة تخصيص (pmpermit|pmpic|pmblock|startmsg)$",
    command=("ازالة تخصيص", plugin_category),
    info={
        "header": "To delete costomization of your CatUserbot.",
        "options": {
            "pmpermit": "To delete custom pmpermit text",
            "pmblock": "To delete custom pmpermit block message",
            "pmpic": "To delete custom pmpermit pic.",
            "startmsg": "To delete custom start message of bot when some one started it.",
        },
        "usage": [
            "{tr}delcustom <option>",
        ],
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_catuserbot(event):
    "To delete costomization of your CatUserbot."
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(event, "⌔︙ انت لم تقم بتخصيص رسالة التحذير")
        delgvar("pmpermit_txt")
    if input_str == "pmblock":
        if gvarstatus("pmblock") is None:
            return await edit_delete(event, "⌔︙ انت لم تقم بخصيص رسالة الحظر ❕")
        delgvar("pmblock")
    if input_str == "pmpic":
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(event, "⌔︙ انت لم تقم بتخصيص صورة الحماية ❕")
        delgvar("pmpermit_pic")
    if input_str == "startmsg":
        if gvarstatus("START_TEXT") is None:
            return await edit_delete(
                event, "⌔︙ انت لم تقم بخصيص رسالة بدء بـوتك ❕"
            )
        delgvar("START_TEXT")
    await edit_or_reply(
        event, f"⌔︙  تم بنجاح ازالة هذا التخصيص ✅"
    )
