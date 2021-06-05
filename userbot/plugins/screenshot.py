"""
`Credits` @amnd33p
from ..helpers.utils import _format
Modified by @mrconfused
"""

import io
import traceback
from datetime import datetime

import requests
from selenium import webdriver
from validators.url import url

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply
from . import reply_id

plugin_category = "utils"


@catub.cat_cmd(
    pattern="سكرين (.*)",
    command=("سكرين", plugin_category),
    info={
        "header": "To Take a screenshot of a website.",
        "usage": "{tr}ss <link>",
        "examples": "{tr}ss https://github.com/sandy1709/catuserbot",
    },
)
async def _(event):
    "To Take a screenshot of a website."
    if Config.CHROME_BIN is None:
        return await edit_or_reply(
            event, "تحتاج إلى تثبيت جوجل كروم. وحدة توقف."
        )
    catevent = await edit_or_reply(event, "`جار الالتقاط انتظر 🔍❤️ ...`")
    start = datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.CHROME_BIN
        await event.edit("`بدء Google Chrome BIN`")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        inputstr = input_str
        caturl = url(inputstr)
        if not caturl:
            inputstr = "http://" + input_str
            caturl = url(inputstr)
        if not caturl:
            return await catevent.edit("`الإدخال المحدد ليس عنوان url معتمدًا`")
        driver.get(inputstr)
        await catevent.edit("`حساب أبعاد الصفحة`")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        await catevent.edit("`وقف Chrome Bin`")
        driver.close()
        message_id = await reply_id(event)
        end = datetime.now()
        ms = (end - start).seconds
        hmm = f"**الرابط : **{input_str} \n**الوقت :** `{ms} ثواني`"
        await catevent.delete()
        with io.BytesIO(im_png) as out_file:
            out_file.name = input_str + ".PNG"
            await event.client.send_file(
                event.chat_id,
                out_file,
                caption=hmm,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
    except Exception:
        await catevent.edit(f"`{traceback.format_exc()}`")
