from . import *
from userbot import jmthon

@jmthon.on(admin_cmd(pattern="(ذاتية|اح)"))
async def oho(event):
  if not event.is_reply:
    return await event.edit('يجـب عـليك الـرد عـلى صـورة ذاتيـة الـتدمير')
  rr9r7 = await event.get_reply_message()
  pic = await rr9r7.download_media()
  await bot.send_file('me', pic, caption=f"""
-تـم جلب الصوره
- CH: @Jepthon
- Dev:¹: @lMl10l
  """)
  await event.delete(كيوت❤️‍🔥)

#اخمط وسمي روحك مطور ما اوصيك
# كتابة السيد حسين  
#@lMl10"
