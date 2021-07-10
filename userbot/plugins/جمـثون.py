from telethon import events
import random, re
from userbot.utils import admin_cmd
import asyncio 

# Wespr File by  @RRRD7

@borg.on(
    admin_cmd(pattern="همسة ?(.*)")
)
async def wspr(event):
    if event.fwd_from:
        return
    jmthonb = event.pattern_match.group(1)
    rrrd7 = "@nnbbot"
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    tap = await bot.inline_query(rrrd7, jmthonb) 
    await tap[0].click(event.chat_id)
    await event.delete()
    
@borg.on(
    admin_cmd(
       pattern="اكس او$"
    )
)
# كتابة وتعديل فريق جمثون  #@RRRD7
async def gamez(event):
    if event.fwd_from:
        return
    jmthonusername = "@xobot"
    uunzz = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(jmthonusername, uunzz)
    await tap[0].click(event.chat_id)
    await event.delete()
    
@borg.on(admin_cmd("م28"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("**اوامر الهمسه واكس او **'\n\nالامر  𖥻 `.همسة`\nالاستخدام  𖥻 لكتابة همسه سرية لشخص في المجموعه \n───────────\n\n الامر 𖥻 `.الهمسة`\n استخدامه 𖥻 لعرض كيفية كتابة همسة سرية\n───────────\n\n الامر 𖥻 `.اكس او` \n استخدامه 𖥻 ففط ارسل الامر لبدء لعبة اكس او \n─────────── \n\nقنـاة السـورس   𖥻 [𝗝ََِ𝗠ٓ𝗧َُِْٓ𝗛ُ𝗢َ𝗡ٍَ](t.me/JMTHON)") 
        
@borg.on(admin_cmd("الهمسة"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("**شـرح كيـفية كـتابة همـسة سـرية**\n اولا اكتب الامر  .همسة  بعدها الرسالة بعدها اكتب معرف الشخص\nمـثال  :   `.همسة ههلا @RRRD7`")
        
@borg.on(
    admin_cmd(
       pattern="اكس او$"
    )
)
# كتابة وتعديل فريق جمثون  #@RRRD7
async def gamez(event):
    if event.fwd_from:
        return
    jmusername = "@xobot"
    uunzz = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(jmusername, uunzz)
    await tap[0].click(event.chat_id)
    await event.delete()