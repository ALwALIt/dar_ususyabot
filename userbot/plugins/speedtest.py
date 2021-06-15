"""Check your internet speed powered by speedtest.net
Syntax: .speedtest
Available Options: image, file, text"""

from datetime import datetime

import speedtest

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "utils"


def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "kilobytes", 2: "megabytes", 3: "gigabytes", 4: "terabytes"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


@catub.cat_cmd(
    pattern="سرعة النت(?: |$)(.*)",
    command=("سرعة النت", plugin_category),
    info={
        "header": "Botserver's speedtest by ookla.",
        "options": {
            "text": "will give output as text",
            "image": "Will give output as image this is default option if no input is given.",
            "file": "will give output as png file.",
        },
        "usage": ["{tr}speedtest <option>", "{tr}speedtest"],
    },
)
async def _(event):
    "Botserver's speedtest by ookla."
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    catevent = await edit_or_reply(
        event, "`حساب سرعة الإنترنت الخاصة بي. أرجو الإنتظار!!`"
    )
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = await reply_id(event)
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await catevent.edit(
                """`اكتمل اختبار السرعه في ثانيه {} seconds`

`تنزيل : {}`
`تحميل : {}`
`البنك : {}`
`مزود الخدمة الانترنيت : {}`
`ISP تـقـيـم : {}`""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    convert_from_bytes(upload_speed),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="**اختبار السرعة** اكتمل في  {} من الثواني ".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
    except Exception as exc:
        await catevent.edit(
            """**اكتمل اختبار السرعه في ثانيه {} seconds
تنزيل: {}
تحميل: {}
البنك: {}

__مع الاخطاء التالية__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                str(exc),
            )
        )
