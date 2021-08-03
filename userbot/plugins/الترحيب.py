# Copyright (C) 2021 JMTHON TEAM
# FILES WRITTEN BY  @RRRD7
# TRANSLATED TO MA BY @QHR_1

from telethon import events

from userbot import jmthon
from userbot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from . import BOTLOG_CHATID

plugin_category = "utils"
LOGS = logging.getLogger(__name__)


@jmthon.on(events.ChatAction)
async def _(event):  # sourcery no-metrics
    cws = get_current_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        if gvarstatus("clean_welcome") is None:
            try:
                await event.client.delete_messages(event.chat_id, cws.previous_welcome)
            except Exception as e:
                LOGS.warn(str(e))
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = chat.title or "لـهاد الـدردشـة"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws.reply:
                current_saved_welcome_message = cws.reply
        current_message = await event.reply(
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
        )
        update_previous_welcome(event.chat_id, current_message.id)


@jmthon.ar_cmd(
    pattern="ترحيب(?:\s|$)([\s\S]*)",
    command=("ترحيب", plugin_category),
    info={
        "الامر": ".ضع ترحيب",
        "الشرح": "امر الترحيب كيقوم بالترحيب بجميع الناس اللي كيدخلو للقروب",
        "الاضافات": {
            "{mention}": "تاق للمستخدم",
            "{title}": "باش تدير اسم القروب مع الاسم",
            "{count}": "باش دير عدد الاعضاء",
            "{first}": "باش دير الاسم الاول للمستخدم ",
            "{last}": "باش دير الاسم الثاني للمستخدم",
            "{fullname}": "باش دير الاسم الكامل للمستخدم",
            "{userid}": "باش دير ايدي الشخص",
            "{username}": "باش دير يوزر الشخص",
            "{my_first}": "باش دير الاسم الاول ديالك",
            "{my_fullname}": "باش دير الاسم الكامل ديالك",
            "{my_last}": "باش دير الاسم الثاني ديالك",
            "{my_mention}": "باش تطاقي راسك",
            "{my_username}": "باش تدير اليوزر ديالك.",
        },
        "الاستخدام": [
            "{tr}ترحيب <رسالة الترحيب>",
            " ريبوندي {tr}ترحيب على الرسالة او الصوره باش دير رساله ترحيبيه",
        ],
        "الامثلة": "{tr} مرحبا نورتي  .",
    },
)
async def save_welcome(event):
    "To set welcome message in chat."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙رسالة الترحيب  :\
                \n⌔︙ايدي الدردشة  : {event.chat_id}\
                \n⌔︙يتم حفظ الرسالة التالية كملاحظة ترحيبية لـ 🔖 : {event.chat.title}, ",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await edit_or_reply(
                event,
                "-",
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "⌔︙ الترحيب {} بنجاح ✅"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تـم الحفـظ"))
    rm_welcome_setting(event.chat_id)
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم الـتحديث"))
    await edit_or_reply("⌔︙ كايـن خـطأ في وضـع الـترحيب هـنا")


@jmthon.ar_cmd(
    pattern="حذف الترحيبات$",
    command=("حذف الترحيبات", plugin_category),
    info={
        "الامر": ".حذف ترحيب",
        "الشرح": "لحذف  الترحيب",
        "الاستخدام": "{tr}حذف ترحيب",
    },
)
async def del_welcome(event):
    "To turn off welcome message"
    if rm_welcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "⌔︙ تم حذف الترحيبات بنجاح ✅.")
    else:
        await edit_or_reply(event, "⌔︙ معنديـش اي تـرحيبـات فالأصـل")


@jmthon.ar_cmd(
    pattern="الترحيبات$",
    command=("الترحيبات", plugin_category),
    info={
        "الاستخدام": "لرؤية جميع الترحيبات المضافه للدردشه",
        "الامر": "{tr}الترحيبات",
    },
)
async def show_welcome(event):
    "To show current welcome message in group"
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        return await edit_or_reply(event, "⌔︙  متحفظش اي ترحيب هنـا !")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "⌔︙ أنا دب كنرحب بالمستخدمين جداد بهاد الرسالة"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "⌔︙ أنا دب كنرحب بالمستخدمين جداد بهاد الرسالة"
        )
        await event.reply(cws.reply)

@jmthon.ar_cmd(
    pattern="الترحيب السابق (تشغيل|ايقاف)$",
    command=("الترحيب السابق", plugin_category),
    info={
        "header": "⌔︙لإيقاف أو تشغيل حذف رسالة الترحيب السابقة .",
        "description": "⌔︙ إذا كنت ترغب في حذف رسالة الترحيب السابقة وإرسال رسالة ترحيب جديدة ، فقم بتشغيلها عن طريق  قم بإيقاف تشغيله إذا كنت بحاجة",
        "usage": "{tr}<رساله الترحيب السابقه <تشغيل/ايقاف",
    },
)
async def del_welcome(event):
    "⌔︙ لإيقاف أولا تشغيل حذف رسالة الترحيب اللي دازت ."
    input_str = event.pattern_match.group(1)
    if input_str == "تشغيل":
        if gvarstatus("clean_welcome") is None:
            return await edit_delete(event, "**⌔︙تم مشعولة ديجا ✅**")
        delgvar("clean_welcome")
        return await edit_delete(
            event,
            "**⌔︙ من دب رسالة الترحيب اللي دازت غتمحا وغادي تتصافط رسالة الترحيب الجديدة **",
        )
    if gvarstatus("clean_welcome") is None:
        addgvar("clean_welcome", "false")
        return await edit_delete(
            event, "**⌔︙ من دب مغديش تتمحا رسالة الترحيب اللي دازت **"
        )
    await edit_delete(event, "**⌔︙ تم مطفية ديجا ✅")
