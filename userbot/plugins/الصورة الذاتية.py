from . import *
from userbot import jmthon

@jmthon.on(admin_cmd(pattern="جلب الصورة"))
async def oho(event):
  if not event.is_reply:
    return await event.edit('يجـب عـليك الـرد عـلى صـورة ذاتيـة الـتدمير')
  rr9r7 = await event.get_reply_message()
  pic = await rr9r7.download_media()
  await bot.send_file(event.chat_id, pic, caption=f"""
- ههاه ياب ترا انـي منصب سورس جمثـون اكـدر احفـظ الصـور المؤقتة 😂🙁♥

- ترا هذا رد من الملف الاصلي مو من صاحب الحساب

- مطوري  :  @RR9R7
  """)
  await event.delete()

#اخمط وسمي روحك مطور ما اوصيك
# كتابة محمد الزهيري  
#@RR9R7
