from telethon import events, Button
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from Jmthon.razan.resources.mybot import *

ROZ_PIC = "https://telegra.ph/file/7a97963354e87e6fc7cde.jpg"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        me = await bot.get_me()
        if query.startswith("السورس") and event.query.user_id == bot.uid:
            buttons = [
                [
                    Button.url("رابط الشرح ⚙️", "https://youtu.be/ATAgbLGzr7w"),
                    Button.url("رابط التنصيب 👨🏼‍💻", "https://heroku.com/deploy?template=https://github.com/USERBOTJEPTHON/JEP-THON"),
                    Button.url("استخراج كود تيرمكس 🧸", "https://replit.com/@Hsynaaly5/UltroidStringSession#main.py"),
                    Button.url("بوت فاذر 👨🏻‍🦳", "http://t.me/BotFather"),
                    Button.url("استخراج الايبيات 🤍", "https://my.telegram.org/"),
                    Button.url("قناة السورس ✅", "https://t.me/JepThon"),

                ]
            ]
            if ROZ_PIC and ROZ_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    ROZ_PIC,
                    text=ROZ,
                    buttons=buttons,
                    link_preview=False
                )
            elif ROZ_PIC:
                result = builder.document(
                    ROZ_PIC,
                    title="JepThon - USERBOT",
                    text=ROZ,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="JepThon - USERBOT",
                    text=ROZ,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    RR7PP = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(RR7PP, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()

# edit by ~ @lMl10l
