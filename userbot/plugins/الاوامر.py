# WRITE  BY @VUUZZ - @RR9R7
# PLUGIN FOR JepThon USERBOT
# @JepThon

import random
from telethon import events
import random, re
from ..Config import Config

from userbot.utils import admin_cmd

import asyncio
from userbot import jmthon

from ..core.managers import edit_or_reply
from ..sql_helper.globals import gvarstatus

plugin_category = "extra"

Command = Config.COMM_ET or "الاوامر"

@jmthon.on(admin_cmd(pattern=f"{Command}(?:\s|$)([\s\S]*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit(
        ": ** 𓆩قائمة اوامر سورس الوالي𓆪 **\n 𓍹——————❁AΞL❁——————𓍻\n( `.م1` )  ☞ اوامر الادمن\n( `.م2` )  ☞ اوامر المجموعة\n( `.م3` )  ☞  اوامر الترحيب والردود\n( `.م4` )  ☞ حماية خاص والتلكراف\n( `.م5` )  ☞ اوامر المنشن والانتحال\n( `.م6` )  ☞ اوامر التحميل والترجمة\n( `.م7` )  ☞ اوامر المنع و القفل\n( `.م8` )  ☞ اوامر التنظيف والتكرار\n( `.م9` )  ☞ اوامر التخصيص والفارات\n( `.م10` )  ☞ اوامر الوقتي و التشغيل\n( `.م11` )  ☞ اوامر الكشف و الروابط\n( `.م12` )  ☞ اوامر المساعدة والإذاعة \n( `.م13` )  ☞ اوامر الارسال والاذكار\n( `.م14` )  ☞ اوامر المـلصقات وكوكل\n( `.م15` ) ☞ اوامر التسلية والميمز والتحشيش \n( `.م16` ) ☞ اوامر الصيغ والجهات\n( `.م17` ) ☞ اوامر التمبلر والزغرفة والمتحركة\n( `.م18` ) ☞ اوامر الحساب والالعاب\n( `.م19` ) ☞ اوامر الصور والفلاتر\n( `.م20` ) ☞ اوامر بصمات الميمز\n𓍹——————❁AΞL❁——————𓍻\n ⌯︙[ ┈┉━｢ KZR BOT ｣━┅┈ ](t.me/ioi_t)"
)

@jmthon.ar_cmd(
    pattern="م1$",
    command=("م1", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الادمن لسورس الوالي **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الحظر` )\n- ( `.اوامر الكتم` )\n- ( `.اوامر التثبيت` )\n- ( `.اوامر الاشراف` )\n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)
		
@jmthon.ar_cmd(
    pattern="م2$",
    command=("م2", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر المجـموعه لسورس الوالي **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر التفليش` )\n- ( `.اوامر المحذوفين` )\n- ( `.اوامر الكروب` )\n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م3$",
    command=("م3", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الـترحيب والـردود **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الترحيب` )\n- ( `.اوامر الردود` )\n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)
@jmthon.ar_cmd(
    pattern="م4$",
    command=("م4", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر حـماية الخاص والتلكراف **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الحماية` )\n- ( `.اوامر التلكراف` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)
@jmthon.ar_cmd(
    pattern="م5$",
    command=("م5", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الـمنشن والانتحال **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الانتحال` )\n- ( `.اوامر التقليد` )\n- ( `.اوامر المنشن` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م6$",
    command=("م6", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر التحميل والترجمه **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر النطق` )\n- ( `.اوامر التحميل` )\n- ( `.اوامر الترجمة` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م7$",
    command=("م7", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر القفل والمنع **:\n𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر القفل` )\n- ( `.اوامر الفتح` )\n- ( `.اوامر المنع` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م8$",
    command=("م8", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر التكرار والتنظيف **:\n𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر التكرار` )\n- ( `.اوامر السبام` )\n- ( `.اوامر التنظيف` ) \n- ( `.اوامر المسح` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م9$",
    command=("م9", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الفارات والتخصيص **:\n هـنـا  : \n\n@KZR_666"
		)

@jmthon.ar_cmd(
    pattern="م10$",
    command=("م10", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الوقتي والتشغيل **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الاسم` )\n- ( `.اوامر البايو` )\n- ( `.اوامر التشغيل` ) \n- ( `.اوامر الاطفاء` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)	

@jmthon.ar_cmd(
    pattern="م11$",
    command=("م11", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الكـشف و الروابط **:\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الكشف` )\n- ( `.اوامر الروابط` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @ioi_t"
)
@jmthon.ar_cmd(
    pattern="م12$",
    command=("م12", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر المساعدة  **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الوقت والتاريخ` )\n- ( `.اوامر كورونا` )\n- ( `.اوامر الصلاة` ) \n- ( `.اوامر مساعدة` )\n- ( `.اوامر الاذاعه` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)
@jmthon.ar_cmd(
    pattern="م13$",
    command=("م13", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الارسال **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.امر الصورة الذاتية` )\n- ( `.اوامر التحذيرات` )\n- ( `.اوامر اللستة` )\n- ( `.اوامر الملكية` ) \n- ( `.اوامر السليب` ) \n- ( `.اوامر الاذكار` )\n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)
@jmthon.ar_cmd(
    pattern="م14$",
    command=("م14", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الملصقات وكوكل **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الملصقات` )\n- ( `.اوامر كوكل` )\n𓍹——————❁ＪΞＰ❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م15$",
    command=("م15", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر التسلية والتحشيش **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر التسلية` )\n- ( `.اوامر التحشيش` )\n- ( `.اوامر الميمز` )\n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م16$",
    command=("م16", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر تحويل الصيغ و الجهات **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر التحويل` )\n- ( `.اوامر الجهات` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"
)

@jmthon.ar_cmd(
    pattern="م18$",
    command=("م18", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر الحساب و الالعاب **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.اوامر الحساب` )\n- ( `.اوامر الالعاب` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"

)

@jmthon.ar_cmd(
    pattern="م19$",
    command=("م19", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"**قائـمه اوامر فلاتر الصـور**:\n 𓍹——————❁AΞL❁——————𓍻\n ◂ `.عكس اللون`\n- بالرد على صورة او فيديو او ملصق لعكس اللوان الميديا \n\n ◂ `.قلب الصورة`\n- بالرد على الصورة لقلبها نحو الاعلى\n\n ◂ `.فلتر شمسي`\n- بالرد على صورة او فيديو او ملصق لعمل فلتر شمسي عليه\n\n ◂  `.فلتر رمادي`\n-بالرد على صورة او فيديو او ملصق لعمل فلتر رمادي عليه\n\n ◂ `.زووم`\n. بالرد على الصورة لعمل زوم للصورة وتقريبها\n\n ◂ `.اطار`.\n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"

)

@jmthon.ar_cmd(
    pattern="م20$",
    command=("م20", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"** قائمة اوامر بصمات الميمز **:\n 𓍹——————❁AΞL❁——————𓍻\n ⌯︙اختر احدى هذه القوائم\n\n- ( `.بصمات ميمز` )\n- ( `.بصمات ميمز2` )\n- ( `.بصمات ميمز3` ) \n𓍹——————❁AΞL❁——————𓍻\n⌔︙CH : @ioi_t"

)
