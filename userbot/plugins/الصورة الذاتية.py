from userbot import *
from userbot import jmthon

@jmthon.on(admin_cmd(pattern="(ذاتية|اح)"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("..")
    rr9r7 = await event.get_reply_message()
    pic = await rr9r7.download_media()
    await bot.send_file(
        "me",
        pic,
        caption=f"""
-تـم جـلب الصـورة بنجـاح ✅
- CH: @Jepthon
- Dev: @lMl10l
  """,
    )
    await event.edit("كيوت ❤️‍🔥")

#اخمط وسمي روحك مطور ما اوصيك
# كتابة السيد حسين  
#@lMl10"
