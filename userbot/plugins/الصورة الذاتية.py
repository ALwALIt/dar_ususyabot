from userbot import *
from userbot import jmthon
from ..Config import Config
from ..sql_helper.globals import gvarstatus

Jepthon_CMD = Config.SCPIC_CMD or "ذاتية"
SC_TEXT = gvarstatus("SC_TEXT") or "** بـوت  َِ𝙅 َِ𝙀 َِ𝙋 َِ𝙏 َِ𝙃 َِ𝙊 َِ𝙉  يعـمل بنـجـاح  **"
@jmthon.on(admin_cmd(pattern=f"{Jepthon_CMD}"))
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
    await event.edit("{SC_TEXT}")
