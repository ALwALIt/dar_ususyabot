# speech to text module for catuserbot by uniborg (@spechide)
import os
from datetime import datetime

import requests

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@catub.cat_cmd(
    pattern="اكتبها(?: |$)(.*)",
    command=("اكتبها", plugin_category),
    info={
        "الامر": "حتى يكتب الموجود بالبصمع",
        "الشرح": "رد على البصمه راح يكتبلك الموجود بيها",
        "الاستخدام": "{tr}stt",
    },
)
async def _(event):
    "speech to text."
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    if not event.pattern_match.group(1):
        input_str = "en"
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not event.reply_to_msg_id:
        return await edit_delete(
            event, "**يجي الرد على الرسالة الصوتية اولا 𖥻**"
        )

    catevent = await edit_or_reply(event, "**يتم التحليلي انتظر 𖥻**")
    previous_message = await event.get_reply_message()
    required_file_name = await event.client.download_media(
        previous_message, Config.TMP_DOWNLOAD_DIRECTORY
    )
    lan = input_str
    if Config.IBM_WATSON_CRED_URL is None or Config.IBM_WATSON_CRED_PASSWORD is None:
        return await catevent.edit(
            "`You need to set the required ENV variables for this module. \nModule stopping`"
        )
    await catevent.edit("**بدء تحويل البصمه الى كتابة 𖥻**")
    headers = {
        "Content-Type": previous_message.media.document.mime_type,
    }
    data = open(required_file_name, "rb").read() #Arabic Cat by  - @RRRD7.- @UUNZZ
    response = requests.post(
        Config.IBM_WATSON_CRED_URL + "/v1/recognize",
        headers=headers,
        data=data,
        auth=("apikey", Config.IBM_WATSON_CRED_PASSWORD),
    )
    r = response.json()
    if "results" not in r:
        return await catevent.edit(r["error"])
    # process the json to appropriate string format
    results = r["results"]
    transcript_response = ""
    transcript_confidence = ""
    for alternative in results:
        alternatives = alternative["alternatives"][0]
        transcript_response += " " + str(alternatives["transcript"]) + " + "
        transcript_confidence += " " + str(alternatives["confidence"]) + " + "
    end = datetime.now()
    ms = (end - start).seconds
    if transcript_response == "":
        string_to_show = "**الـلغة : **`{}`\n**الوقت المستغرق : **`{} من الثواني`\n**لم يتـم العثور علـى نتيجه**".format(
            lan, ms
        )
    else:
        string_to_show = "**الـلغة : **`{}`\n**الانعكاس : **`{}`\n**الـوقت المستغـرق : **`{} من الـثواني`\n**الاعـتماد : **`{}`".format(
            lan, transcript_response, ms, transcript_confidence
        )
    await catevent.edit(string_to_show)
    # now, remove the temporary file
    os.remove(required_file_name)
