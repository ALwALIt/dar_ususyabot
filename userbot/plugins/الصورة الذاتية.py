from userbot import *
from userbot import jmthon
from ..Config import Config

Thadea = Config.THADEA_ET or "ذاتية"
@jmthon.on(admin_cmd(pattern="{Thadea}"))
async def dato(event):
    if not event.is_reply:
        return await event.edit("..")
    lMl10l = await event.get_reply_message()
    pic = await lMl10l.download_media()
    await bot.send_file(
        "me",
        pic,
        caption=f"""
-تـم جـلب الصـورة بنجـاح ✅
- CH: @Jepthon
- Dev: @lMl10l
  """,
    )
    await event.edit("احح")

#اخمط وسمي روحك مطور ما اوصيك
# كتابة السيد حسين  
#@lMl10"
