# ported from paperplaneExtended by avinashreddy3108 for media support
# For Catuserbot
# Arabic Translate By  :  @RRRD7

from telethon import events

from userbot import catub
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


@catub.on(events.ChatAction)
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
        title = chat.title or "this chat"
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


@catub.cat_cmd(
    pattern="ترحيب(?: |$)(.*)",
    command=("ترحيب", plugin_category),
    info={
        "الامر": ".ضع ترحيب",
        "الشرح": "امر الترحيب يقوم بالتحريب بجميع الاشخاص الذين يدخلون للمجموعه",
        "الاضافات": {
            "{mention}": "عمل تاك للمستخدم",
            "{title}": "لوضع اسم الدردشه مع الاسم",
            "{count}": "لوضع عدد الاعضاء",
            "{first}": "لوضع الاسم الاول للمستخدم ",
            "{last}": "لوضع الاسك الثاني للمستخدم",
            "{fullname}": "لوضع الاسم الكامل للمستخدم",
            "{userid}": "لوضع ايدي الشخص",
            "{username}": "لوضع معرف الشخص",
            "{my_first}": "لوضع الاسم الاول الخاص بك",
            "{my_fullname}": "لوضع الاسم الكامل الخاص بك",
            "{my_last}": "لوضع الاسم الثاني الخاص بك",
            "{my_mention}": "لعمل تاك لنفسك ",
            "{my_username}": "لاستخدام معرفك.",
        },
        "الاستخدام": [
            "{tr}ضع ترحيب <رسالة التحريب>",
            "قم بالرد {tr}ضع ترحيب على الرسالة او الصوره لوضعها رساله ترحيبيه",
        ],
        "الامثلة": "{tr}ضع ترحيب - هَِـلا يڪَِـمـࢪ نورِت 💞🦋 .",
    },
)
async def save_welcome(event):
    "لوضع رسالة ترحيبيه في المجموعه"
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#رسالة_الترحيب\
                \nايدي الدردشه: {event.chat_id}\
                \nيتم حفظ الرسالة التالية كملاحظة ترحيبية لـ {event.chat.title}, لا تثم بحذف هذه الرسالة !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await edit_or_reply(
                event,
                "حفظ الصوره كـرسالة ترحيبيه يتطلب وضع الفار لـ BOTLOG_CHATID ",
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "** تم حفظ الترحيب الخاص بهذه الدردشه بنجاح**"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("saved"))
    rm_welcome_setting(event.chat_id)
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("updated"))
    await edit_or_reply("Error while setting welcome in this group")


@catub.cat_cmd(
    pattern="حذف ترحيب$",
    command=("حذف ترحيب", plugin_category),
    info={
        "الامر": ".حذف ترحيب",
        "الشرح": "يقوم بحذف جميع الرسائل الترحيبيه للدردشه.",
        "الاستخدام": "{tr}حذف ترحيب",
    },
)
async def del_welcome(event):
    "لحذف الرسائل الترحيبيه"
    if rm_welcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**تم حذف جميع الرسائل الترحيبيه لهذه الدردشه**")
    else:
        await edit_or_reply(event, "** هل إمتلك ترحيبات بالاصل هنا  ?**")


@catub.cat_cmd(
    pattern="الترحيبات$",
    command=("الترحيبات", plugin_category),
    info={
        "الامر": "لرؤية جميع التحريبات المضافه للدردشه",
        "الاستخدام": "{tr}الترحيبات",
    },
)
async def show_welcome(event):
    "To show current welcome message in group"
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        return await edit_or_reply(event, "**لم يتم حفظ اي رسائل ترحيبيه هنا**")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "** أنا الان اقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**أنا الان اقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة**"
        )
        await event.reply(cws.reply)


@catub.cat_cmd(
    pattern="cleanwelcome (on|off)$",
    command=("cleanwelcome", plugin_category),
    info={
        "header": "To turn off or turn on of deleting previous welcome message.",
        "description": "if you want to delete previous welcome message and send new one turn on it by deafult it will be on. Turn it off if you need",
        "usage": "{tr}cleanwelcome <on/off>",
    },
)
async def del_welcome(event):
    "To turn off or turn on of deleting previous welcome message."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("clean_welcome") is None:
            return await edit_delete(event, "__Already it was turned on.__")
        delgvar("clean_welcome")
        return await edit_delete(
            event,
            "__From now on previous welcome message will be deleted and new welcome message will be sent.__",
        )
    if gvarstatus("clean_welcome") is None:
        addgvar("clean_welcome", "false")
        return await edit_delete(
            event, "__From now on previous welcome message will not be deleted .__"
        )
    await edit_delete(event, "It was turned off already")
