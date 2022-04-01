import asyncio
import math
import os

import heroku3
import requests
import urllib3
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
from . import BOTLOG_CHATID, mention, jmthon
from userbot.utils import admin_cmd, sudo_cmd
from userbot import LOGS, bot as jmthon

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


jepthonnn = (
    "𓆩 [JEPTHON VARS - اوامـر الفـارات](t.me/jepthon) 𓆪\n\n"
    "⪼ `.اضف صورة الحماية` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة الوقتي` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اوامر الفارات` لعـرض بقيـة اوامـر الفـارات\n\n\n"
    "**✾╎قائـمه اوامر تغييـر بقيـة الفـارات بأمـر واحـد فقـط :** \n\n"
    "⪼ `.اضف كليشة الحماية` بالـرد ع الكليشـة\n\n"
    "⪼ `.اضف كليشة الفحص` بالـرد ع الكليشـة\n\n"
    "⪼ `.اضف رمز الوقتي` بالـرد ع رمـز\n\n"
    "⪼ `.اضف زخرفة الوقتي` بالـرد ع ارقـام الزغـرفه\n\n"
    "⪼ `.اضف البايو الوقتي` بالـرد ع البـايـو\n\n"
    "⪼ `.اضف اسم المستخدم` بالـرد ع اسـم\n\n"
    "⪼ `.اضف كروب الرسائل` بالـرد ع ايدي الكـروب\n\n"
    "⪼ `.اضف كروب السجل` بالـرد ع ايدي الكـروب\n\n"
    "⪼ `.اضف رسائل الحماية` بالـرد ع رقـم لعدد رسائل حماية الخاص\n\n\n"
    "⪼ `.جلب` + اسـم الفـار\n\n"
    "⪼ `.حذف` + اسـم الفـار\n\n"
    "\n𓆩 [السيد حسين علي](t.me/lMl10l) 𓆪"
)


# Copyright (C) 2022 jepthon . All Rights Reserved
@jmthon.on(admin_cmd(pattern=r"اضف (.*)"))
@jmthon.on(sudo_cmd(pattern=r"اضف (.*)", allow_sudo=True))
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await edit(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await ed(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vinfo = reply.text
    heroku_var = app.config()
    jep = await edit_or_reply(event, "**✾╎جـاري اضـافة الفـار الـى بـوتك ...**")
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغير : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "كليشة الحماية" or input_str == "كليشه الحمايه":
        variable = "PM_TEXT"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغير : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه  ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه  ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "TIME_JEP"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "زخرفه الوقتي" or input_str == "زخرفة الوقتي":
        variable = "JP_FN"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "الوقت" or input_str == "الساعه":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغيـر المنطقـة الزمنيـه**\n **✾╎المتغير : دولـة مصـر 🇪🇬**\n\n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**")
        else:
            await jep.edit("**✾╎تم اعـادة تغيـر المنطقـة الزمنيـه**\n **✾╎المتغير : دولـة مصـر 🇪🇬**\n\n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**")
        heroku_var[variable] = vinfo
    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "السجل" or input_str == "كروب السجل":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        variable = "COMMAND_HAND_LER"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "الريبو" or input_str == "السورس":
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        variable = "AUTONAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص":
        variable = "MAX_FLOOD_IN_PMS"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغييـر {} بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        else:
            await jep.edit("**✾╎تم اضافـة {} بنجـاح ☑️** \n**✾╎المضاف اليه :**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    else:
        if input_str:
            return await jep.edit("**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!..**".format(input_str))

        return await edit_or_reply(event, "**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!..**".format(input_str))


# Copyright (C) 2022 jepthon . All Rights Reserved
@jmthon.on(admin_cmd(pattern="حذف(?:\s|$)([\s\S]*)"))
@jmthon.on(sudo_cmd(pattern="حذف(?:\s|$)([\s\S]*)", allow_sudo=True))
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await edit(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.text[5:]
    heroku_var = app.config()
    jep = await edit_or_reply(event, "**✾╎جـاري حـذف الفـار مـن بـوتك 🚮...**")
    # All Rights Reserved for "Zedthon - UserBot" "زلـزال الهيبـه"
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "كليشة الحماية" or input_str == "كليشه الحمايه":
        variable = "PM_TEXT"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "صورة الفحص" or input_str == "صوره الفحص":
        variable = "ALIVE_PIC"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "صورة الحماية" or input_str == "صوره الحمايه":
        variable = "PM_PIC"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "صورة الوقتي" or input_str == "صوره الوقتي":
        variable = "DIGITAL_PIC"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "TIME_JEP"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "زخرفه الوقتي" or input_str == "زخرفة الوقتي":
        variable = "JP_FN"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "السجل" or input_str == "كروب السجل":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "الريبو" or input_str == "السورس":
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        variable = "AUTONAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "المطور" or input_str == "المطورين":
        variable = "SUDO_USERS"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص":
        variable = "MAX_FLOOD_IN_PMS"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await jep.edit("**✾╎عـذراً .. فـار {} غير موجود اصـلاً...**".format(input_str))

        await jep.edit("**✾╎تم حـذف {} بنجـاح ☑️**\n**✾╎المتغيـر المحـذوف : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت جيبثون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    else:
        if input_str:
            return await jep.edit("**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!..**".format(input_str))

        return await edit_or_reply(event, "**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!..**".format(input_str))


# Copyright (C) 2022 jepthon . All Rights Reserved
@zedthon.on(zelzal_cmd(pattern="جلب(?:\s|$)([\s\S]*)"))
@zedthon.on(sudo_cmd(pattern="جلب(?:\s|$)([\s\S]*)", allow_sudo=True))
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await edit(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit(
            event,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.text[5:]
    heroku_var = app.config()
    jep = await edit_or_reply(event, "**✾╎جـاري جلـب الفـار مـن بـوتك 🛂...**")
    if input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "TIME_JEP"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "زخرفه الوقتي" or input_str == "زخرفة الوقتي":
        variable = "JP_FN"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "الوقت" or input_str == "الساعه":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎تم تغيـر المنطقـة الزمنيـه**\n **✾╎المتغير : دولـة مصـر 🇪🇬**\n\n**✾╎قنـاة السـورس : @jepthon**")
        else:
            await jep.edit("**✾╎تم اعـادة تغيـر المنطقـة الزمنيـه**\n **✾╎المتغير : دولـة مصـر 🇪🇬**\n\n**✾╎قنـاة السـورس : @jepthon**")
        heroku_var[variable] = "Africa/Cairo"
    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "السجل" or input_str == "كروب السجل":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
 
    elif input_str == "الريبو" or input_str == "السورس":
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))

    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        variable = "AUTONAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))

    elif input_str == "المطور" or input_str == "المطورين":
        variable = "SUDO_USERS"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎المطـور {} موجـود 🧑🏻‍💻☑️**\n**✾╎ايدي المطـور : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ المطـور {} غيـر موجـود 🧑🏻‍💻❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))

    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص":
        variable = "MAX_FLOOD_IN_PMS"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await jep.edit("**✾╎الفـار {} موجـود ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))
        else:
            await jep.edit("**✾╎ الفـار {} غيـر موجـود ❌** \n**✾╎المتغيـر :**\n `{}` \n**✾╎قنـاة السـورس : @jepthon**".format(input_str, heroku_var[variable]))

    else:
        if input_str:
            return await jep.edit("**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!..**".format(input_str))

        return await edit_or_reply(event, "**✾╎عـذراً .. لايوجـد هنالك فـار بإسـم {} ؟!..**".format(input_str))

@jmthon.on(
    jmthon.ar(
       pattern="اضف صورة (الحماية|الحمايه|الفحص|الوقتي) ?(.*)"
    )
)
@jmthon.on(sudo_cmd(pattern="اضف صورة (الحماية|الحمايه|الفحص|الوقتي) ?(.*)", allow_sudo=True))
async def _(tosh):
    if tosh.fwd_from:
        return
    if Config.HEROKU_API_KEY is None:
        return await edit(
            var,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم الى الاعدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit(
            var,
            "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    heroku_var = app.config()
    jep = await edit_or_reply(tosh, "**✾╎جـاري اضـافة فـار الصـورة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await tosh.client.send_message(
            BOTLOG_CHATID,
            "**✾╎تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**✾╎لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = tosh.pattern_match.group(2)
    if tosh.reply_to_msg_id:
        start = datetime.now()
        r_message = await tosh.get_reply_message()
        input_str = tosh.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await tosh.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await jep.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await jep.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                heroku_var["PMPERMIT_PIC"] = vinfo
                await jep.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        elif input_str in ["الفحص", "السورس"]:
            downloaded_file_name = await tosh.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await jep.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await jep.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                heroku_var["ALIVE_PIC"] = vinfo
                await jep.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))
        elif input_str in ["الوقتي", "البروفايل"]:
            downloaded_file_name = await tosh.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await jep.edit(
                f"**✾╎تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await jep.edit("**✾╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://telegra.ph{}".format(media_urls[0]))
                heroku_var["DIGITAL_PIC"] = vinfo
                await jep.edit("**✾╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**✾╎المتغيـر : ↶**\n `{}` \n**✾╎يتم الان اعـادة تشغيـل بـوت زد ثـون يستغـرق الامر 2-1 دقيقـه ▬▭ ...**".format(input_str, vinfo))


    else:
        await jep.edit(
            "**✾╎بالـرد ع صـورة لتعييـن الفـار ...**",
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")



# Copyright (C) 2022 Jepthon . All Rights Reserved
@jmthon.on(admin_cmd(pattern="اوامر الفارات"))
@jmthon.on(sudo_cmd(pattern="اوامر الفارات", allow_sudo=True))
async def cmd(jepthonn):
    await edit_or_reply(jepthonn, jepthonnn)
