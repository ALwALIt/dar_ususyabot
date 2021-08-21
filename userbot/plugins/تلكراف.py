import os
import random
import string
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
from telethon.utils import get_display_name

from userbot import jmthon

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "utils"


telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


@jmthon.ar_cmd(
    pattern="(ت(ل)?ك(راف)?) ?(م|ن|ميديا|نص)(?:\s|$)([\s\S]*)",
    command=("تلكراف", plugin_category),
    )
async def _(event):
    "To get telegraph link"
    catevent = await edit_or_reply(event, "**⌔︙ جاري المعالجـة **")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"** تـم صـنع رابـط تليجـراف جديـد  :** {auth_url} \n **للجلسـة الحاليـة، لا تقـم بإعطـاء هـذا الرابـط إلى أي أحـد، حتى وإن قـال بأنّـه موظـف لـدى تليڪـرام !**",
        )
    optional_title = event.pattern_match.group(5)
    if not event.reply_to_msg_id:
        return await catevent.edit(
            "**⌔︙ قـم بالـردّ على رسالـة للحصـول على رابـط صـورة تليجـراف**",
        )

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()
    if input_str in ["ميديا", "م"]:
        downloaded_file_name = await event.client.download_media(
            r_message, Config.TEMP_DIR
        )
        await catevent.edit(f"**⌔︙ تـم التحميـل إلى**  `{downloaded_file_name}`")
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            media_urls = upload_file(downloaded_file_name)
        except exceptions.TelegraphException as exc:
            await catevent.edit(f"**⌔︙ حـدث خـطأ مـا : **\n`{str(exc)}`")
            os.remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms = (end - start).seconds
            os.remove(downloaded_file_name)
            await catevent.edit(
                 f"**⌔︙ الرابـط  : ** [اضغط هنا](https://telegra.ph{media_urls[0]})\
                    \n**⌔︙ الوقـت المستغـرق   : ** `{ms} الثوانـي.`",
                link_preview=True,
            )
    elif input_str in ["نص", "ن"]:
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        # apparently, all Users do not have last_name field
        if optional_title:
            title_of_page = optional_title
        page_content = r_message.message
        if r_message.media:
            if page_content != "":
                title_of_page = page_content
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8") + "\n"
            os.remove(downloaded_file_name)
        page_content = page_content.replace("\n", "<br>")
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
        except Exception as e:
            LOGS.info(e)
            title_of_page = "".join(
                random.choice(list(string.ascii_lowercase + string.ascii_uppercase))
                for _ in range(16)
            )
            response = telegraph.create_page(title_of_page, html_content=page_content)
        end = datetime.now()
        ms = (end - start).seconds
        cat = f"https://telegra.ph/{response['path']}"
        await catevent.edit(
            f"**⌔︙ الرابـط  : **[اضغـط هـنا]({cat})\
                 \n**⌔︙ الوقـت المستغـرق   : ** `{ms} الثوانـي.`",
            link_preview=True,
        )
