import re

from telethon import Button, events
from telethon.events import CallbackQuery

from Jmthon.razan.resources.assistant import *
from Jmthon.razan.resources.mybot import *
from userbot import jmthon

from ..Config import Config

ROZ_IC = "https://telegra.ph/file/da99302a87f1e1db4bbf4.jpg"
ROE = "** هـذه هي قائمة اوامـر سـورس جيبثون **"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("مساعدة") and event.query.user_id == bot.uid:
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
            if ROZ_IC and ROZ_IC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    ROZ_IC, text=ROE, buttons=buttons, link_preview=False
                )
            elif ROZ_IC:
                result = builder.document(
                    ROZ_IC,
                    title="Jepthon - USERBOT",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="Jepthon - USERBOT",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)


@bot.on(admin_cmd(outgoing=True, pattern="مساعدة"))
async def repo(event):
    if event.fwd_from:
        return
    RR7PP = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(RR7PP, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"jmthon0")))
async def _(event):
    await event.edit(ROZADM)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"jrzst")))
async def _(event):
    await event.edit(GRTSTI)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"tslrzj")))
async def _(event):
    await event.edit(JMAN)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"krrznd")))
async def _(event):
    await event.edit(TKPRZ)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"rozbot")))
async def _(event):
    await event.edit(ROZBOT)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"Jmrz")))
async def _(event):
    await event.edit(JROZT)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"r7brz")))
async def _(event):
    await event.edit(JMTRD)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"sejrz")))
async def _(event):
    await event.edit(ROZSEG)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"gro")))
async def _(event):
    await event.edit(JMGR1)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"grrz")))
async def _(event):
    await event.edit(ROZPRV)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"iiers")))
async def _(event):
    await event.edit(HERP)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"rfhrz")))
async def _(event):
    await event.edit(T7SHIZ)


@jmthon.tgbot.on(CallbackQuery(data=re.compile(rb"uscuxrz")))
async def _(event):
    await event.edit(CLORN)
