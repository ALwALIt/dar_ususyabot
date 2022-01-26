import re

from telethon import Button, events
from telethon.events import CallbackQuery

from Jmthon.razan.resources.assistant import *
from Jmthon.razan.resources.mybot import *
from userbot import jmthon
from ..core import check_owner
from ..Config import Config

ROZ_IC = "https://telegra.ph/file/da99302a87f1e1db4bbf4.jpg"
ROE = "** هـذه هي قائمة اوامـر سـورس جيبثون العرب **"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("اوامري") and event.query.user_id == bot.uid:
            buttons = [
                [Button.inline("• اوامر الادمن •", data="jmthon0")],
                [
                    Button.inline("• اوامر البوت •", data="rozbot"),
                    Button.inline("• الحساب •", data="Jmrz"),
                    Button.inline("• المجموعات •", data="gro"),
                ],
                [
                    Button.inline("• الصيغ و الجهات •", data="sejrz"),
                    Button.inline("• الحماية و تلكراف •", data="grrz"),
                ],
                [
                    Button.inline("• اوامر التسلية •", data="tslrzj"),
                    Button.inline("• الترحيبات والردود •", data="r7brz"),
                ],
                [
                    Button.inline("• التكرار والتنظيف •", data="krrznd"),
                    Button.inline("• الملصقات وصور •", data="jrzst"),
                ],
                [
                    Button.inline("• التكرار والتنظيف •", data="krrznd"),
                    Button.inline("• الترفيه •", data="rfhrz"),
                ],
                [
                    Button.inline("• اوامر المساعدة •", data="iiers"),
                    Button.inline("• الملصقات وصور •", data="jrzst"),
                ],
                [
                    Button.inline("• الأكستـرا •", data="iiers"),
                    Button.inline("• الانتحال والتقليد •", data="uscuxrz"),
                ],
            ]
            result = builder.article(
                    title="JEPTHON - USERBOT",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)


@bot.on(admin_cmd(outgoing=True, pattern="اوامري"))
async def repo(event):
    if event.fwd_from:
        return
    RR7PP = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(RR7PP, "اوامري")
    await response[0].click(event.chat_id)
    await event.delete()


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"jmthon0")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="jrzst"),]]
    await event.edit(ROZADM, buttons=buttons)

@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"jrzst")))
@check_owner
async def _(event):
    butze = [[Button.inline("التالي", data="tslrzj"),]]
    await event.edit(GRTSTI, buttons=butze)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"tslrzj")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="krrznd"),]]
    await event.edit(JMAN, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"krrznd")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="rozbot"),]]
    await event.edit(TKPRZ, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"rozbot")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="Jmrz"),]]
    await event.edit(ROZBOT, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"Jmrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="r7brz"),]]
    await event.edit(JROZT, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"r7brz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="sejrz"),]]
    await event.edit(JMTRD, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"sejrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="gro"),]]
    await event.edit(ROZSEG, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"gro")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="grrz"),]]
    await event.edit(JMGR1,buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"grrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="iiers"),]]
    await event.edit(ROZPRV, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"iiers")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="rfhrz"),]]
    await event.edit(HERP, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"rfhrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("التالي", data="uscuxrz"),]]
    await event.edit(T7SHIZ, buttons=buttons)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"uscuxrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع", data="jmthon0"),]]
    await event.edit(CLORN, buttons=buttons)
