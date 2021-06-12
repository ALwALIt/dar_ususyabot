from covid import Covid

from userbot.utils import admin_cmd

from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="كورونا (.*)"))

async def _(event):

    if event.pattern_match.group(1):
        country = (event.pattern_match.group(1)).title()
    else:
        country = "World"
    catevent = await edit_or_reply(event, "`جـاري جلب معلـومات كـورنا عـن هذا البـلد 🦠`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n¹- الحالات المؤكدة ¦ <code>{hmm1}</code>"
        data += f"\n²- النشطة ¦ <code>{country_data['active']}</code>"
        data += f"\n³-️ الميتين ¦ <code>{hmm2}</code>"
        data += f"\n⁴- حالات الحرجة ¦ <code>{country_data['critical']}</code>"
        data += f"\n⁵- المتعافي ¦ <code>{country_data['recovered']}</code>"
        data += f"\n⁶- مجموع الاختبارات ¦ <code>{country_data['total_tests']}</code>"
        data += f"\n⁷- حالات جديدة ¦ <code>{country_data['new_cases']}</code>"
        data += f"\n⁸- الموتى الجدد ¦ <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>Corona Virus Info of {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n\¹-  الحالات المؤكدة ¦  <code>{data['new_positive']}</code>\
                \n²- النشطة ¦ <code>{data['new_active']}</code>\
                \n³- الميتين ¦ <code>{data['new_death']}</code>\
                \n⁴- حالات الحرجة ¦ <code>{data['new_cured']}</code>\
                \n⁵- المتعافي ¦ <code>{cat1}</code>\
                \n⁶- الموتى الجدد ¦ <code>{cat2}</code>\
                \n⁷- علاجه جديد ¦ <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                "`معلومات عن فيروس كورونا من {} غير متوفر أو غير قادر على الجلب`".format(
                    country
                ),
                5,
            )

CMD_HELP.update(
    {
        "corona": ".corona (country name)"


    }
)
