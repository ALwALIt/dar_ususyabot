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

#start 
@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    razan = await tgbot.get_me()
    bot_id = razan.first_name
    bot_username = razan.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    vent = event.chat_id
    starttext = f"**مـرحبا {firstname} ! انـا هـو {bot_id}, بـوت مساعـد بسيـط 🧸🤍 \n\n- [مـالك البـوت](tg://user?id={bot.uid}) \nيمكـنك مراسلـة المـالك عبـر هذا البـوت . \n\nاذا كـنت تـريد تنـصيب بـوت خـاص بـك تـاكد من الازرار بالأسفل**"
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
            message=f"اهـلا يا مالكـي انـه انـا {bot_id}, مسـاعدك ! \nمـاذا تريـد ان تفعـل اليـوم ?",
            buttons=[
                                     [Button.inline("عرض المستخدمين 📬", data="users"), Button.inline(
                                         "اوامر البـوت ⚒️", data="gibcmd")],
                                     [Button.url("المطـور 🔗", "https://t.me/RR9R7")],

                                 ])
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

#Data

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
    rorza = "**قـائمـة اوامـر البـوت الخاصـة بك**:\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات**\n• /start \n ( للـتأكد من حالـة البـوت) \n• /ping \n ( امـر بنـك )  \n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n• /id \n  ( لعـرض ايدي المسـتخدم ) \n• /alive \n- ( لـرؤية معلومات البـوت ) \n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n• /prumote  \n-  ( لرفـع شخص مشـرف )\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n• /stats  \n-  ( لعرض مستخدمين البوت )  \n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n• /del  \n-  ( بالـرد على الرسالـة لحـذفها )"
    await tgbot.send_message(event.chat_id, rorza)


@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    rorza = "**قـائمـة اوامـر البـوت الخاصـة بك**:\n- **جميع هذه الاوامر تستخدم بعد اضافة البوت في مجموعة ورفعه مشـرف مع بعض الصلاحيـات**\n• /start \n ( للـتأكد من حالـة البـوت) \n• /ping \n ( امـر بنـك )  \n• /broadcast \n ( لعمـل اذاعـة لجميـع المستخدمين في البـوت )  \n• /id \n  ( لعـرض ايدي المسـتخدم ) \n• /alive \n- ( لـرؤية معلومات البـوت ) \n• /bun \n-  ( تعمل في المجموعات لحظر شخص )\n• /unbun  \n-  ( تعمل في المجموعات لالغاء حظر مستخدم )  \n• /prumote  \n-  ( لرفـع شخص مشـرف )\n• /demute  \n-  ( لتنزيل الشخص من رتبة الاشراف ) \n• /pin  \n-  ( لتثبيـت رسالة في المجموعـة )  \n• /stats  \n-  ( لعرض مستخدمين البوت )  \n• /purge  \n-  ( بالرد على رسالة ليقوم بحذف ما تحتها من رسائل ) \n• /del  \n-  ( بالـرد على الرسالـة لحـذفها )"
    await event.reply(rorza)

@tgbot.on(events.NewMessage(pattern="^/alive", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    razan = "**𝘑𝘔𝘛𝘏𝘖𝘕 𝘜𝘚𝘌𝘙𝘉𝘖𝘛**\n•━═━═━═━═━━═━═━═━═━•‌‌\n**- حالة البوت **  يعمـل بنجـاح\n**- اصدار التليثون  **: 1.23.0\n**- اصدار البايثون **: 3.9.6\n**- يوزرك ** {mention}\n**- CH : @JMTHON\n•━═━═━═━═━━═━═━═━═━•‌‌\n"
    await event.reply(razan)
