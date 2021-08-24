# WRITE  BY @VUUZZ - @RR9R7
# PLUGIN FOR JMTHON USERBOT
# @JMTHON

import random
from telethon import events
import random, re

from userbot.utils import admin_cmd

import asyncio
from userbot import jmthon

from ..core.managers import edit_or_reply

plugin_category = "extra"

@jmthon.ar_cmd(
    pattern="الاوامر$",
    command=("الاوامر", plugin_category),
)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit(
        "قـائمـة اوامـر سـورس جـمثون  :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n( `.الامر 1` )  - اوامر الادمن\n( `.الامر 2` )  - اوامر المجموعة\n( `.الامر 3` )  -  اوامر الترحيب والردود\n\n( `.م4` )  - حماية خاص والتلكراف\n( `.م5` )  -  اوامر المنشن والانتحال\n( `.م6` )  -  اوامر التحميل والترجمة\n( `.م7` )  -  اوامر المنع و القفل\n( `.م8` )  -  اوامر التنظيف والتكرار\n( `.م9` )  -  اوامر التخصيص والفارات\n( `.م10` )  -  اوامر الوقتي و التشغيل\n( `.م11` )  -  اوامر الكشف و الروابط\n( `.م12` )  -  اوامر المساعدة والإذاعة \n( `.م13` )  -  اوامر الارسال\n( `.م14` )  -  اوامر المـلصقات وكوكل\n( `.م15` ) - اوامر التسلية والتحشيش \n( `.م16` ) - اوامر تحويل الصيغ\n( `.م17` ) - اوامر التمبلر والزغرفة والمتحركة\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ كيفـية الاستخـدام  :\n\nفقـط ارسل القـائمة  من (.الامر 1...الامر 3)\nو من  (.م4....)  وستـظهر لك العديد من الأوامـر"
)

@jmthon.ar_cmd(
    pattern="الامر 1$",
    command=("الامر 1", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الادمن لسورس جمثون :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الحظر` )\n- ( `.اوامر الكتم` )\n- ( `.اوامر التثبيت` )\n- ( `.اوامر الاشراف` )\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
		
@jmthon.ar_cmd(
    pattern="الامر 2$",
    command=("الامر 2", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر المجـموعه لسورس جمثون :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر التفليش` )\n- ( `.اوامر المحذوفين` )\n- ( `.اوامر الكروب` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="الامر 3$",
    command=("الامر 3", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الـترحيب والـردود :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الترحيب` )\n- ( `.اوامر الردود` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
@jmthon.ar_cmd(
    pattern="م4$",
    command=("م4", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر حـماية الخاص والتلكراف :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الخاص` )\n- ( `.اوامر التلكراف` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
@jmthon.ar_cmd(
    pattern="م5$",
    command=("م5", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الـمنشن والانتحال :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الانتحال` )\n- ( `.اوامر التقليد` )\n- ( `.اوامر المنشن` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="م6$",
    command=("م6", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر التحميل والترجمه :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر النطق` )\n- ( `.اوامر التحميل` )\n- ( `.اوامر الترجمة` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="م7$",
    command=("م7", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر القفل والمنع :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر القفل` )\n- ( `.اوامر الفتح` )\n- ( `.اوامر المنع` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="م8$",
    command=("م8", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر التكرار والتنظيف :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر التكرار` )\n- ( `.اوامر السبام` )\n- ( `.اوامر التنظيف` ) \n- ( `.اوامر المسح` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="م9$",
    command=("م9", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الفارات والتخصيص :\n هـنـا  : \n\n@FYFYFF"
		)

@jmthon.ar_cmd(
    pattern="م10$",
    command=("م10", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الوقتي والتشغيل :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الاسم` )\n- ( `.اوامر البايو` )\n- ( `.اوامر التشغيل` ) \n- ( `.اوامر الاطفاء` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)	

@jmthon.ar_cmd(
    pattern="م11$",
    command=("م11", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الكـشف و الروابط :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الكشف` )\n- ( `.اوامر الروابط` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
@jmthon.ar_cmd(
    pattern="م12$",
    command=("م12", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر المساعدة  :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الوقت والتاريخ` )\n- ( `.اوامر كورونا` )\n- ( `.اوامر الصلاة` ) \n- ( `.اوامر مساعدة` )\n- ( `.اوامر الاذاعه` ) \n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
@jmthon.ar_cmd(
    pattern="م13$",
    command=("م13", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الارسال :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.امر الصورة الذاتية` )\n- ( `.اوامر التحذيرات` )\n- ( `.اوامر اللستة` )\n- ( `.اوامر الملكية` ) \n- ( `.اوامر السليب` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
@jmthon.ar_cmd(
    pattern="م14$",
    command=("م14", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر الملصقات وكوكل :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر الملصقات` )\n- ( `.اوامر كوكل` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="م15$",
    command=("م15", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر التسلية والتحشيش :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر التسلية` )\n- ( `.اوامر التحشيش` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)

@jmthon.ar_cmd(
    pattern="م16$",
    command=("م16", plugin_category),
)
async def _(event):
	if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
		await event.edit(
		"قائمة اوامر تحويل الصيغ :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ⌔︙ اختر احدى هذه القوائم\n\n- ( `.اوامر التحويل` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @JMTHON"
)
