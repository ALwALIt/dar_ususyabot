import asyncio
import time

import aiohttp
from telethon.errors import ChatAdminRequiredError as no_admin
from telethon.tl.functions.messages import ExportChatInviteRequest

from Jmthon.razan.resources.strings import *
from userbot import jmthon
from userbot.utils import admin_cmd

from ..core.managers import edit_or_reply
from ..core.managers import edit_or_reply as eod
from ..helpers import get_user_from_event
from . import *

@jmthon.on(admin_cmd(pattern="طقس (.*)"))
@jmthon.on(sudo_cmd(pattern="طقس (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    Key = "f806cebbd44f34cc4cd1d79a290081be"
    sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    input_str = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str, Key))
    response_api = await response_api_zero.json()
    if response_api["cod"] == 200:
        country_code = response_api["sys"]["country"]
        country_time_zone = int(response_api["timezone"])
        sun_rise_time = int(response_api["sys"]["sunrise"]) + country_time_zone
        sun_set_time = int(response_api["sys"]["sunset"]) + country_time_zone
        await edit_or_reply(
            event,
            """{}
•**الحـرارة**: {}°С
•**درجة الحرارة الصغرى:** {}°С
•**درجة الحرارة العظم:** {}°С
•**الرطـوبة**: {}%
•**الـرياح**: {}m/s
•**السحـاب**: {}hpa
•**شروق الشمس**: {} {}
•**غروب الشمس**: {} {}""".format(
                input_str,
                response_api["main"]["temp"],
                response_api["main"]["temp_min"],
                response_api["main"]["temp_max"],
                response_api["main"]["humidity"],
                response_api["wind"]["speed"],
                response_api["clouds"]["all"],
                # response_api["main"]["pressure"],
                time.strftime("%Y-%m-%d %I:%M:%S", time.gmtime(sun_rise_time)),
                country_code,
                time.strftime("%Y-%m-%d %I:%M:%S", time.gmtime(sun_set_time)),
                country_code,
            ),
        )
    else:
        await edit_or_reply(event, response_api["message"])


@jmthon.on(admin_cmd(pattern="wttr (.*)"))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://wttr.in/{}.png"
    # logger.info(sample_url)
    input_str = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str))
        # logger.info(response_api_zero)
        response_api = await response_api_zero.read()
        with io.BytesIO(response_api) as out_file:
            await event.reply(file=out_file)
    await edit_or_reply(event, input_str)
