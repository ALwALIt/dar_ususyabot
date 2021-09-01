#    جميع الحقوق لمطوري سورس جمثون حصريا لهم فقط
#    اذا تخمط الملف اذك الحقوق وكاتبيه ومطوريه لا تحذف الحقوق وتصير فاشل 👍
#    كتابة محمد الزهيري 
import asyncio
import io
import re

from telethon import Button, custom, events
from telethon.tl.functions.users import GetFullUserRequest

from userbot import bot
from userbot.sql_helper.blacklist_assistant import (
    add_nibba_in_db,
    is_he_added,
    removenibba,
)
from userbot.sql_helper.botusers_sql import add_me_in_db, his_userid
from userbot.sql_helper.idadder_sql import (
    add_usersid_in_db,
    already_added,
    get_all_users,
)


@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    starkbot = await tgbot.get_me()
    bot_id = starkbot.first_name
    bot_username = starkbot.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    vent = event.chat_id
    starttext = f"**مـرحبا {firstname} ! انـا هـو {bot_id}, بـوت مساعـد بسيـط 🧸🤍 \n\n- [مـالك البـوت](tg://user?id={bot.uid}) \nيمكـنك مراسلـة المـالك عبـر هذا البـوت . \n\nاذا كـنت تـريد تنـصيب بـوت خـاص بـك تـاكد من الازرار بالأسفل**"
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
            message=f"اهـلا يا مالكـي انـه انـا {bot_id}, مسـاعدك ! \nمـاذا تريـد ان تفعـل اليـوم ?",
            buttons=[
                [custom.Button.inline("عرض المستخدمين 📬", data="users")],
                [custom.Button.inline("اوامر البـوت ⚒️", data="gibcmd")],
                [
                    Button.url(
                        "اضفـني الـى مجموعـة 👥", f"t.me/{bot_username}?startgroup=true"
                    )
                ],
            ],
        )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(event.sender_id)
        await tgbot.send_message(
            event.chat_id,
            message=starttext,
            link_preview=False,
            buttons=[
                [custom.Button.inline("تنـصيب جمثـون  🐍", data="deploy")],
                [Button.url("تحتاج مسـاعدة ❓", "https://t.me/GroupJmthon")],
            ],
        )


# Data's


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
    await event.delete()
    if event.query.user_id is not bot.uid:
        await tgbot.send_message(
            event.chat_id,
            message="**لتـنصيب البـوت الخاص بك اتبـع الخطـوات في الاسفـل وحاول واذا لم تستطيع تفضل الى مجموعة المساعدة ليساعدوك 🧸♥**.",
            buttons=[
                [Button.url("شرح التنصيب 📺", "https://youtu.be/9VJ1HYtGbJU")],
                [Button.url("كروب المساعدة ❓", "https://t.me/GroupJmthon")],
            ],
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        total_users = get_all_users()
        users_list = "- قـائمة مستخـدمين البـوت  : \n\n"
        for starked in total_users:
            users_list += ("==> {} \n").format(int(starked.chat_id))
        with io.BytesIO(str.encode(users_list)) as tedt_file:
            tedt_file.name = "razan.txt"
            await tgbot.send_file(
                event.chat_id,
                tedt_file,
                force_document=True,
                caption="مجموع مستخدمـين بوتـك",
                allow_cache=False,
            )
    else:
        pass


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
    await event.delete()
    grabon = "**قـائمـة اوامـر البـوت الخاصـة بك**:\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات**\n• /start \n ( للـتأكد من حالـة البـوت) \n• /ping \n ( امـر بنـك )  \n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n• /id \n  ( لعـرض ايدي المسـتخدم ) \n• /alive \n- ( لـرؤية معلومات البـوت ) \n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n• /prumote  \n-  ( لرفـع شخص مشـرف )\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n• /stats  \n-  ( لعرض مستخدمين البوت )  \n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n• /del  \n-  ( بالـرد على الرسالـة لحـذفها )"
    await tgbot.send_message(event.chat_id, grabon)


# Jmthon Userbot 
@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def all_messages_catcher(event):
    if is_he_added(event.sender_id):
        return
    if event.raw_text.startswith("/"):
        pass
    elif event.sender_id == bot.uid:
        return
    else:
        await event.get_sender()
        event.chat_id
        sed = await event.forward_to(bot.uid)
        # اضافة المستخدمين لقاعدة البيانات لامر الاذاعة  ~ by ~ @JMTHON
        # (C) @RROR7
        add_me_in_db(sed.id, event.sender_id, event.id)


@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def sed(event):
    msg = await event.get_reply_message()
    msg.id
    msg_s = event.raw_text
    user_id, reply_message_id = his_userid(msg.id)
    if event.sender_id == bot.uid:
        if event.raw_text.startswith("/"):
            pass
        else:
            await tgbot.send_message(user_id, msg_s)


# broadcast
@tgbot.on(
    events.NewMessage(
        pattern="^/broadcast ?(.*)", func=lambda e: e.sender_id == bot.uid
    )
)
async def sedlyfsir(event):
    msgtobroadcast = event.pattern_match.group(1)
    userstobc = get_all_users()
    error_count = 0
    sent_count = 0
    for starkcast in userstobc:
        try:
            sent_count += 1
            await tgbot.send_message(int(starkcast.chat_id), msgtobroadcast)
            await asyncio.sleep(0.2)
        except Exception as e:
            try:
                logger.info(f"- خـطأ : {error_count}\n- خـطأ : {e} \n- المستخدمين : {chat_id}")
            except:
                pass
    await tgbot.send_message(
        event.chat_id,
        f"-** تمت الاذاعـة بنجاح فـي {sent_count} من الكـروبات والمستخدميـن 🧸♥**",
    )


@tgbot.on(
    events.NewMessage(pattern="^/stats ?(.*)", func=lambda e: e.sender_id == bot.uid)
)
async def starkisnoob(event):
    starkisnoob = get_all_users()
    await event.reply(
        f"**حـالة البـوت  : ** \n- **مجـموع مستخـدمين البوت**: {len(starkisnoob)}"
    )


@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    grabon = "**قـائمـة اوامـر البـوت الخاصـة بك**:\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات**\n• /start \n ( للـتأكد من حالـة البـوت) \n• /ping \n ( امـر بنـك )  \n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n• /id \n  ( لعـرض ايدي المسـتخدم ) \n• /alive \n- ( لـرؤية معلومات البـوت ) \n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n• /prumote  \n-  ( لرفـع شخص مشـرف )\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n• /stats  \n-  ( لعرض مستخدمين البوت )  \n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n• /del  \n-  ( بالـرد على الرسالـة لحـذفها )"
    await event.reply(grabonx)


@tgbot.on(
    events.NewMessage(pattern="^/block ?(.*)", func=lambda e: e.sender_id == bot.uid)
)
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = his_userid(msg.id)
    if is_he_added(user_id):
        await event.reply("**بالفـعل محـظور 🤍،**")
    elif not is_he_added(user_id):
        add_nibba_in_db(user_id)
        await event.reply("** تم حـظره بنجـاح ✅**")
        await tgbot.send_message(
            user_id, "**لقـد تم حـظرك لا تستـطيع مراسـلة مالك البـوت من الان 🤍**،"
        )


@tgbot.on(
    events.NewMessage(pattern="^/unblock ?(.*)", func=lambda e: e.sender_id == bot.uid)
)
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = his_userid(msg.id)
    if not is_he_added(user_id):
        await event.reply("**غير محظور اصلا ❕**")
    elif is_he_added(user_id):
        removenibba(user_id)
        await event.reply("**تم الغاء حظر هذا الشخص بنجاح ✅**")
        await tgbot.send_message(
            user_id, "**لقـد تم الغاء حـظرك تستـطيع مراسـلة مالك البـوت من الان 🤍**،"
        )
