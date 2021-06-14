from urlextract import URLExtract

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER
extractor = URLExtract()


@catub.cat_cmd(
    pattern="تخصيص (pmpermit|pmblock|pmpic)$",
    command=("تخصيص", plugin_category),
    info={
        "header": "To customize your CatUserbot.",
        "options": {
            "pmpermit": "To customize pmpermit text. ",
            "pmblock": "To customize pmpermit block message.",
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
    },
)
async def custom_catuserbot(event):
    "To customize your CatUserbot."
    reply = await event.get_reply_message()
    text = reply.text
    if not reply:
        return await edit_delete(event, "**يرجى الرد على النص او الرابط اولا **ا")
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        addgvar("pmpermit_txt", text)
    if input_str == "pmblock":
        addgvar("pmblock", text)
    if input_str == "pmpic":
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(event, "`الرابط غير صحيح`", 5)
        addgvar("pmpermit_pic", urls[0])
    await edit_or_reply(event, f"** تم تحديث الامر بنجاح ✅❕**")


@catub.cat_cmd(
    pattern="حذف (pmpermit|pmblock|pmpic)$",
    command=("حذف", plugin_category),
    info={
        "header": "To delete costomization of your CatUserbot.",
        "options": {
            "pmpermit": "To delete custom pmpermit text",
            "pmblock": "To delete custom pmpermit block message",
            "pmpic": "To delete custom pmpermit pic.",
        },
        "usage": [
            "{tr}delcustom <option>",
        ],
    },
)
async def custom_catuserbot(event):
    "To delete costomization of your CatUserbot."
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(event," **انت لم تقم بتخصيص اي شي**")
        delgvar("pmpermit_txt")
    if input_str == "pmblock":
        if gvarstatus("pmblock") is None:
            return await edit_delete(event, "انت لم تقم بخصيص رد الحظر")
        delgvar("pmblock")
    if input_str == "pmpic":
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(event, "انت لم تقم بتخصيص صورة الحماية")
        delgvar("pmpermit_pic")
    await edit_or_reply(
        event, f"__تم بنجاح ازالة تخصيصك {input_str}.__"
    )
