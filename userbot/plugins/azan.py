# ported from uniborg
# https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvakti.py
import json

import requests

from ..sql_helper.globals import gvarstatus
from . import catub, edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="صلاه(?: |$)(.*)",
    command=("صلاه", plugin_category),
    info={
        "header": "Shows you the Islamic prayer times of the given city name.",
        "note": "you can set default city by using {tr}setcity command.",
        "usage": "{tr}صلاه <المحافظه>",
        "examples": "{tr}صلاه baghdad ",
    },
)
async def get_adzan(adzan):
    "Shows you the Islamic prayer times of the given city name"
    input_str = adzan.pattern_match.group(1)
    LOKASI = gvarstatus("DEFCITY") or "Delhi" if not input_str else input_str
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        return await edit_delete(
            adzan, f"`Couldn't fetch any data about the city {LOKASI}`", 5
        )
    result = json.loads(request.text)
    catresult = f"<b>اوقـات صـلاه المـسلمين 👳 </b>\
            \n\n<b>المـدينة     : </b><i>{result['query']}</i>\
            \n<b>الـدولة  : </b><i>{result['country']}</i>\
            \n<b>التـاريـخ     : </b><i>{result['items'][0]['date_for']}</i>\
            \n<b>الـفجر     : </b><i>{result['items'][0]['fajr']}</i>\
            \n<b>شـروق الشمس    : </b><i>{result['items'][0]['shurooq']}</i>\
            \n<b>الظهـر    : </b><i>{result['items'][0]['dhuhr']}</i>\
            \n<b>العـصر    : </b><i>{result['items'][0]['asr']}</i>\
            \n<b>المـغرب    : </b><i>{result['items'][0]['maghrib']}</i>\
            \n<b>العشـاء     : </b><i>{result['items'][0]['isha']}</i>\
    "
    await edit_or_reply(adzan, catresult, "html")
