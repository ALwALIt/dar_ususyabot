import re
from datetime import datetime

from telethon import Button, functions
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import mention

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER


async def do_pm_permit_action(event, chat):  # sourcery no-metrics
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    totalwarns = Config.MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= Config.MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.info(str(e))
        custompmblock = gvarstatus("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(
                mention=mention,
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
                totalwarns=totalwarns,
                warns=warns,
                remwarns=remwarns,
            )
        else:
            USER_BOT_WARN_ZERO = f"حذࢪتك وكتـلك لا تكࢪࢪ تَم حظࢪك بنجاح ما ٱكدر اخليك تزعج المالك \n- **بباي 🙁🤍**"
        msg = await event.reply(USER_BOT_WARN_ZERO)
        await event.client(functions.contacts.BlockRequest(chat.id))
        the_message = f"#المحظورين_الحمايه\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) تم حظره\
                            \n**عدد الرسائل:** {PM_WARNS[str(chat.id)]}"
        del PM_WARNS[str(chat.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
        try:
            return await event.client.send_message(
                BOTLOG_CHATID,
                the_message,
            )
        except BaseException:
            return
    custompmpermit = gvarstatus("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(
            mention=mention,
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
            totalwarns=totalwarns,
            warns=warns,
            remwarns=remwarns,
        )
    else:
        USER_BOT_NO_WARN = f"""ههلا بيك {mention} \n مالك الحساب غير موجود حاليا الرجاء الانتظار وعدم تكرار الرسائل. 

لديك {warns}/{totalwarns} من التحذيرات لا تكرر حتى ما تنحظر من البوت.

اختر احد الخيارات في الاسفل وانتظر الى ان اصبح متصلا بالانترنت ليتم الرد عليك 🔽🔽"""
    addgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        results = await event.client.inline_query(Config.TG_BOT_USERNAME, "pmpermit")
        msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
    except Exception as e:
        LOGS.error(e)
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


async def do_pm_options_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**ارجوك لا ترسل شي اخر فقط انتظر لا تكرر والا شيتم حظرك**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**اتذكر حذرتك وقلت لك لا تكرر اكثر من خيار ولا ترسل رسائل مجرد انتظر. \
تعتقد راح اخليك تكرر لا اسف راح احظرك من الحساب. \
حاليا متكدر بعد تتكلم الى ان ياتي صاحب الحساب ويقوم بالغاء الحظر. 🙂💘**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                            \n**السبب:** هو/هي لم يقم بالتوقف عن ارسال الرسائل والتكرار"
    sqllist.rm_from_list("pmoptions", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_enquire_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """ ههاه لازم تصبر مالك الحساب ما شاف الرسالة انتظر. \
مالك الحساب يرد على الكل بس ما اعرف اذا كان اكو كم شخص يتجاهلهم بس اصبر
مالك الحساب راح يرد عليك لما يكون متصل, اذا راد يرد عليك اصلا
**اتمنى ما تكرر الرسائل حتى ما اضطر احظرك 🙂🌿** """
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"اتذكر حذرتك وقلت لك لا تكرر اكثر من خيار ولا ترسل رسائل مجرد انتظر. \
تعتقد راح اخليك تكرر لا اسف راح احظرك من الحساب. \
**حاليا متكدر بعد تتكلم الى ان ياتي صاحب الحساب ويقوم بالغاء الحظر. 🙂💕**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#المحظورين_للحماية\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                \n**السبب:** هو/هي لم يقم بالتوقف عن ارسال الرسائل والتكرار"
    sqllist.rm_from_list("pmenquire", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_request_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """ههاه لازم تصبر مالك الحساب ما شاف الرسالة انتظر. \
مالك الحساب يرد على الكل بس ما اعرف اذا كان اكو كم شخص يتجاهلهم بس اصبر
مالك الحساب راح يرد عليك لما يكون متصل, اذا راد يرد عليك اصلا
**اتمنى ما تكرر الرسائل حتى ما اضطر احظرك 🙂🌿**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO =  f"اتذكر حذرتك وقلت لك لا تكرر اكثر من خيار ولا ترسل رسائل مجرد انتظر \
تعتقد راح اخليك تكرر لا اسف راح احظرك من الحساب \
**حاليا متكدر بعد تتكلم الى ان ياتي صاحب الحساب ويقوم بالغاء الحظر 🙂💕**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#المحظورين_للحماية\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                \n**السبب:** هو/هي لم يقم بالتوقف عن ارسال الرسائل والتكرار"
    sqllist.rm_from_list("pmrequest", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_chat_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """ههاه لازم تصبر مالك الحساب ما شاف الرسالة انتظر \
مالك الحساب يرد على الكل بس ما اعرف اذا كان اكو كم شخص يتجاهلهم بس اصبر
مالك الحساب راح يرد عليك لما يكون متصل, اذا راد يرد عليك اصلا
**اتمنى ما تكرر الرسائل حتى ما اضطر احظرك 😕🌿**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO =  f"اتذكر حذرتك وقلت لك لا تكرر اكثر من خيار ولا ترسل رسائل مجرد انتظر \
تعتقد راح اخليك تكرر لا اسف راح احظرك من الحساب \
**حاليا متكدر بعد تتكلم الى ان ياتي صاحب الحساب ويقوم بالغاء الحظر 😕💘**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                \n**السبب:** هو/هي لم يقم بالتوقف عن ارسال الرسائل والتكرار"
    sqllist.rm_from_list("pmchat", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_spam_action(event, chat):
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    USER_BOT_WARN_ZERO =  f"اتذكر حذرتك وقلت لك لا تكرر اكثر من خيار ولا ترسل رسائل مجرد انتظر \
تعتقد راح اخليك تكرر لا اسف راح احظرك من الحساب \
**حاليا متكدر بعد تتكلم الى ان ياتي صاحب الحساب ويقوم بالغاء الحظر 🙁💕**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                            \n**Reason:** he opted for spam option and messaged again."
    sqllist.rm_from_list("pmspam", chat.id)
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


@catub.cat_cmd(incoming=True, func=lambda e: e.is_private, edited=False)
async def on_new_private_message(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return await do_pm_spam_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return await do_pm_chat_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return await do_pm_request_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return await do_pm_enquire_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return await do_pm_options_action(event, chat)
    await do_pm_permit_action(event, chat)


@catub.cat_cmd(outgoing=True, func=lambda e: e.is_private, edited=False)
async def you_dm_other(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return
    if event.text and event.text.startswith(
        (
            f"{cmdhd}بلوك",
            f"{cmdhd}رفض",
            f"{cmdhd}س",
            f"{cmdhd}ر",
            f"{cmdhd}سماح",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(
            chat.id, get_display_name(chat), start_date, chat.username, "For Outgoing"
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"show_pmpermit_options")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**- عذرا هذه الخيارات ليست لك انها للمستخدمين الذين يراسلوك 😐⚕️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = f"""حسنا الان بإمكانك اختيار احد الخيارات في الاسفل للتواص مع , {mention}.
**اختر بهدوء خيار واحد فقط لنعرف سبب قدومك هنا ⚕️🤍**

**هذه الخيارات في الاسفل اختر واحد فقط 🔽**"""
    buttons = [
        (Button.inline(text="للاستفسار عن شي ما.", data="to_enquire_something"),),
        (Button.inline(text="لطلب شي ما.", data="to_request_something"),),
        (Button.inline(text="للدردشه مع مالك الحساب.", data="to_chat_with_my_master"),),
        (
            Button.inline(
                text="لاقوم بازعاج مالك الحساب",
                data="to_spam_my_master_inbox",
            ),
        ),
    ]
    sqllist.add_to_list("pmoptions", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    await event.edit(text, buttons=buttons)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_enquire_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**- عذرا هذه الخيارات ليست لك انها للمستخدمين الذين يراسلوك 😐⚕**"
        return await event.answer(text, cache_time=0, alert=True)
    text = """**حسنا تم ارسال طلبك بنجاح 💕 لا تقم بأختيار خيار ثاني \
مالك الحساب مشغول الان  عندما يصبح مالك الحساب متصلا سوف يقول بالرد عليك \
بعدها يمكنك التحدث بحرية لكن ليس الان**"""
    sqllist.add_to_list("pmenquire", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_request_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**- عذرا هذه الخيارات ليست لك انها للمستخدمين الذين يراسلوك 😐⚕**"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__حسنا لقد قمت بأبلاغ مالك الحساب عندما يصبح متصلا بالانترنت \
 أو عندما يكون مالك الحساب متاح سوف يقوم بالرد عليك لذلك ارجوك انتظر__\

**لكن في الوقت الحالي لا تكرر ارسال الرسائل حتر لا اضطر لحظرك 🙁💞**"""
    sqllist.add_to_list("pmrequest", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_chat_with_my_master")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**- عذرا هذه الخيارات ليست لك انها للمستخدمين الذين يراسلوك 😐⚕**"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__بالطبع يمكنك التحدث مع مالك الحساب لكن ليس الان نستطيع التكلم في\
وقت اخر حاليا انا مشغول قليلا عندما اصبح متصلا واذا كنت غير مشغول سأكلمك هذا اكيـد__"""
    sqllist.add_to_list("pmchat", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_spam_my_master_inbox")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "Idoit these options are for users who message you. not for you"
        return await event.answer(text, cache_time=0, alert=True)
    text = "`███████▄▄███████████▄\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓███░░░░░░░░░░░░█\
         \n██████▀▀▀█░░░░██████▀ \
         \n░░░░░░░░░█░░░░█\
         \n░░░░░░░░░░█░░░█\
         \n░░░░░░░░░░░█░░█\
         \n░░░░░░░░░░░█░░█\
         \n░░░░░░░░░░░░▀▀`\
         \n**جييد لكن هذا ليس بيتك حتى تقوم بالازعاج اذهب للعب بعيدا \
         \n\nو هذا اخر تحذير لك ااذا ترسل رسالة اخرى ساقوم بحظرك تلقائيا **"
    sqllist.add_to_list("pmrequesr", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmspam").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.cat_cmd(
    pattern="الحماية (on|off)$",
    command=("الحماية", plugin_category),
    info={
        "header": "To turn on or turn off pmpermit.",
        "usage": "{tr}pmguard on/off",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmpermit."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(
                event, "** تم تفعيل امر الحماية لحسابك بنجاح ✅**"
            )
        else:
            await edit_delete(event, "**امر الحمايه بالفعل مُمكن لحسابك 🌿**")
    else:
        if gvarstatus("pmpermit") is not None:
            delgvar("pmpermit")
            await edit_delete(
                event, "** تم تعطيل امر الحماية لحسابك بنجاح ✅**"
            )
        else:
            await edit_delete(event, "**امر الحمايه بالفعل مُعطل لحسابك 🌿**")


@catub.cat_cmd(
    pattern="(س|سماح)(?: |$)(.*)",
    command=("سماح", plugin_category),
    info={
        "header": "To approve user to direct message you.",
        "usage": [
            "{tr}a/approve <username/reply reason> in group",
            "{tr}a/approve <reason> in pm",
        ],
    },
)
async def approve_p_m(event):
    "To approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__يجب تفعيل امر الحمايه اولا للتفعيل ارسل __`{cmdhd}الحماية on` ليعمل الامر بنجاح ⚕️",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
    else:
        user, reason = await get_user_from_event(event, secondgroup=True)
        if not user:
            return
    if not reason:
        reason = "Not mentioned"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if not pmpermit_sql.is_approved(user.id):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        pmpermit_sql.approve(
            user.id, get_display_name(user), start_date, user.username, reason
        )
        chat = user
        if str(chat.id) in sqllist.get_collection_list("pmspam"):
            sqllist.rm_from_list("pmspam", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmchat"):
            sqllist.rm_from_list("pmchat", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmrequest"):
            sqllist.rm_from_list("pmrequest", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmenquire"):
            sqllist.rm_from_list("pmenquire", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmoptions"):
            sqllist.rm_from_list("pmoptions", chat.id)
        await edit_delete(
            event,
            f"تم المـوافقة على [{user.first_name}](tg://user?id={user.id})\n**السبب :** __{reason}__",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    else:
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __بالفعل موجود في قائمة السماح__",
        )


@catub.cat_cmd(
    pattern="(ر|رفض)(?: |$)(.*)",
    command=("رفض", plugin_category),
    info={
        "header": "To disapprove user to direct message you.",
        "note": "This command works only for approved users",
        "options": {"all": "To disapprove all approved users"},
        "usage": [
            "{tr}da/disapprove <username/reply> in group",
            "{tr}da/disapprove in pm",
            "{tr}da/disapprove all - To disapprove all users.",
        ],
    },
)
async def disapprove_p_m(event):
    "To disapprove user to direct message you."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__يجب تفعيل امر الحمايه اولا للتفعيل ارسل __`{cmdhd}الحماية on` __ليعمل الامر بنجاح__ ",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)

    else:
        reason = event.pattern_match.group(2)
        if reason != "all":
            user, reason = await get_user_from_event(event, secondgroup=True)
            if not user:
                return
    if reason == "all":
        pmpermit_sql.disapprove_all()
        return await edit_delete(
            event, "__حسنا! تم رفض الجميع بنجاح ✅__"
        )
    if not reason:
        reason = "Not Mentioned."
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
        await edit_or_reply(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __تـم رفضه بنـجاح ✅__\n**السبب:**__ {reason}__",
        )
    else:
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __لم تتم الموافقة عليه بالاصل__",
        )


@catub.cat_cmd(
    pattern="بلوك(?: |$)(.*)",
    command=("بلوك", plugin_category),
    info={
        "header": "To block user to direct message you.",
        "usage": [
            "{tr}block <username/reply reason> in group",
            "{tr}block <reason> in pm",
        ],
    },
)
async def block_p_m(event):
    "To block user to direct message you."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__يجب تفعيل امر الحمايه اولا للتفعيل ارسل __`{cmdhd}الحماية on` ليعمل الامر بنجاح ⚕️",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "Not Mentioned."
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(user.id) in PM_WARNS:
        del PM_WARNS[str(user.id)]
    if str(user.id) in PMMESSAGE_CACHE:
        try:
            await event.client.delete_messages(user.id, PMMESSAGE_CACHE[str(user.id)])
        except Exception as e:
            LOGS.info(str(e))
        del PMMESSAGE_CACHE[str(user.id)]
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    await event.client(functions.contacts.BlockRequest(user.id))
    await edit_delete(
        event,
        f"[{user.first_name}](tg://user?id={user.id}) __تم حظره بنجاح لا يمكنه مراسلتك بعد الان ✅⚕️__\n**السبب:** __{reason}__",
    )


@catub.cat_cmd(
    pattern="انبلوك(?: |$)(.*)",
    command=("انبلوك", plugin_category),
    info={
        "header": "To unblock a user.",
        "usage": [
            "{tr}unblock <username/reply reason> in group",
            "{tr}unblock <reason> in pm",
        ],
    },
)
async def unblock_pm(event):
    "To unblock a user."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__يجب تفعيل امر الحمايه اولا للتفعيل ارسل __`{cmdhd}الحماية on` ليعمل الامر بنجاح ⚕️",
        )
    if event.is_private:
        user = await event.get_chat()
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "Not Mentioned."
    await event.client(functions.contacts.UnblockRequest(user.id))
    await event.edit(
        f"[{user.first_name}](tg://user?id={user.id}) __تم الغاء حظره بنجاح يمكنه التكلم معك الان ✅⚕️__\n**السبب:** __{reason}__"
    )


@catub.cat_cmd(
    pattern="المسموح لهم$",
    command=("المسموح لهم", plugin_category),
    info={
        "header": "To see list of approved users.",
        "usage": [
            "{tr}listapproved",
        ],
    },
)
async def approve_p_m(event):
    "To see list of approved users."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__يجب تفعيل امر الحمايه اولا للتفعيل ارسل __`{cmdhd}الحماية on` ليعمل الامر بنجاح ⚕️",
        )
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "**قائمه امر الحماية**\n\n"
    if len(approved_users) > 0:
        for user in approved_users:
            APPROVED_PMs += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**الايدي:** `{user.user_id}`\n**المعرف:** @{user.username}\n**التاريخ: **__{user.date}__\n**السبب: **__{user.reason}__\n\n"
    else:
        APPROVED_PMs = "**- انت لم توافق على اي شخص بالاصل 💞⚕️"
    await edit_or_reply(
        event,
        APPROVED_PMs,
        file_name="approvedpms.txt",
        caption="`Current Approved PMs`",
    )
