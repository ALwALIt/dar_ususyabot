
# Hey 

import asyncio

import requests
from telethon import functions

from ..core.managers import edit_delete, edit_or_reply

from userbot import jmthon
from . import mention, CMD_LIST, HelpString, SUDO_LIST
from .sql_helper.globals import addgvar, gvarstatus


@bot.on(
    icss_cmd(outgoing=True, 
    pattern="مساعده ?(.*)")
)
async def cmd_list(event):
    if event.fwd_from:
        return
    if gvarstatus("HELPTYPE") and gvarstatus("HELPTYPE") == "false":
        HELPTYPE = False
    else:
        HELPTYPE = True
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = (
            "المجمـوع {count} أمر تم ايجاد {plugincount} اضافـه لبوت جيبثون\n\n"
        )
        catcount = 0
        plugincount = 0
        for i in sorted(CMD_LIST):
            plugincount += 1
            string += f"⌔∮ {plugincount}) الاوامر الموجوده في هذه الاضافه " + i + " هيه: \n"
            for iter_list in CMD_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                catcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=catcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"**⌔∮ جميع الاوامر لبوت جيبثون تستطيـع الحصول عليها [هـنا]({url})**"
            await event.edit(reply_text)
            return
        await event.edit(string.format(count=catcount, plugincount=plugincount))
        return
    if input_str:
        if input_str in CMD_LIST:
            string = "<b>{count} Commands found in plugin {input_str}:</b>\n\n"
            catcount = 0
            for i in CMD_LIST[input_str]:
                string += f"  •  <code>{i}</code>"
                string += "\n"
                catcount += 1
            await event.edit(
                string.format(count=catcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            await event.edit(input_str + " is not a valid plugin!")
            await asyncio.sleep(3)
            await event.delete()
    else:
        if HELPTYPE is True:
            help_string = (HelpString.format(mention))
            tgbotusername = Config.TG_BOT_USERNAME
            results = await event.client.inline_query(tgbotusername, help_string)
            await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
            await event.delete()
        else:
            string = "<b>معذرة تأكد من نوع الاضافة اللتي تريد المساعده حولها !!\
                \nعدد الاضافات : </b><code>{count}</code>\
                \n<b>Usage:</b> <code>.مساعده ثم اسم الاضافه</code> \n\n"
            catcount = 0
            for i in sorted(CMD_LIST):
                string += "◆ " + f"<code>{str(i)}</code>"
                string += " "
                catcount += 1
            await event.edit(string.format(count=catcount), parse_mode="HTML")


@jmthon.on(
    sudo_cmd(allow_sudo=True,
    pattern="مساعده ?(.*)")
)
async def info(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = "Total {count} commands found in {plugincount} sudo plugins of catuserbot\n\n"
        catcount = 0
        plugincount = 0
        for i in sorted(SUDO_LIST):
            plugincount += 1
            string += f"{plugincount}) Commands found in Plugin " + i + " are \n"
            for iter_list in SUDO_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                catcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=catcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"All commands of the catuserbot are [here]({url})"
            await event.reply(reply_text, link_preview=False)
            return
        await event.reply(
            string.format(count=catcount, plugincount=plugincount), link_preview=False
        )
        return
    if input_str:
        if input_str in SUDO_LIST:
            string = "<b>{count} Commands found in plugin {input_str}:</b>\n\n"
            catcount = 0
            for i in SUDO_LIST[input_str]:
                string += f"  •  <code>{i}</code>"
                string += "\n"
                catcount += 1
            await event.reply(
                string.format(count=catcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            reply = await event.reply(input_str + " is not a valid plugin!")
            await asyncio.sleep(3)
            await event.delete()
            await reply.delete()
    else:
        string = "<b>Please specify which plugin do you want help for !!\
            \nNumber of plugins : </b><code>{count}</code>\
            \n<b>Usage:</b> <code>.help plugin name</code>\n\n"
        catcount = 0
        for i in sorted(SUDO_LIST):
            string += "◆ " + f"<code>{str(i)}</code>"
            string += " "
            catcount += 1
        await event.reply(string.format(count=catcount), parse_mode="HTML")


@Jmthon.on(admin_cmd(outgoing=True, pattern="شرح ?(.*)"))
@jmthon.on(sudo_cmd(pattern="شرح ?(.*)", allow_sudo=True))
async def info(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            event = await edit_or_reply(event, "**الرجاء تحديد اسم الملف او الاضافـه من قائمـة مسـاعده ...**")
            await asyncio.sleep(3)
            await event.delete()
    else:
        string = "<b>يرجى تحديد الملف او الاضافه اللتي تريد ان اساعدك فيها !!\
            \nعـدد الاضافـات : </b><code>{count}</code>\
            \n<b>Usage : </b><code>.شرح واسم الملف او الاضافه</code>\n\n"
        catcount = 0
        for i in sorted(CMD_HELP):
            string += "◆ " + f"<code>{str(i)}</code>"
            string += " "
            catcount += 1
        if event.sender_id in Config.SUDO_USERS:
            await event.reply(string.format(count=catcount), parse_mode="HTML")
        else:
            await event.edit(string.format(count=catcount), parse_mode="HTML")


@jmthon.on(
    icss_cmd(pattern="المراكز$")
)
@jmthon.on(
    sudo_cmd(pattern="المراكز$", 
    allow_sudo=True)
)
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetNearestDcRequest())
    result = (
        _format.yaml_format(result)
        + "\n\n**قائـمه بمراكـز بيانات تيليجـرام::**\
                \nDC1 : ميامـي FL, USA\
                \nDC2 : امستـردام, NL\
                \nDC3 : ميامـي FL, USA\
                \nDC4 : امستـردام, NL\
                \nDC5 : سـانغفـوره, SG\
                "
    )
    await edit_or_reply(event, result)


@icssjmthon.on(
    icss_cmd(outgoing=True,
    pattern="انلاين (تفعيل|تعطيل)")
)
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    h_type = input_str == "تفعيل"
    if gvarstatus("HELPTYPE") and gvarstatus("HELPTYPE") == "تعطيل":
        HELPTYPE = False
    else:
        HELPTYPE = True
    if HELPTYPE:
        if h_type:
            await event.edit("**انلايـن مـود بالتأكيـد تم تفعيلـه ✅**")
        else:
            addgvar("HELPTYPE", h_type)
            await event.edit("**تـم تعطيـل وضـع الانلايـن بنجـاح 🔕**")
    else:
        if h_type:
            addgvar("HELPTYPE", h_type)
            await event.edit("**تـم تفعيل وضـع الانلايـن بنجـاح ☑️**")
        else:
            await event.edit("**انلايـن مـود بالتأكيـد تم تعطيله 🚫**")


CMD_HELP.update(
    {
        "مساعدة": """**اسم الاضافـه : **`مساعدة`
•  **╮•❐ الامـر ⦂ **`.مساعده/.مساعده + اسم الاضافه`
•  **الشـرح •• **__If you just type .help then shows you help menu, if plugin name is given then shows you only commands in thst plugin and if you use `.help text` then shows you all commands in your userbot__
•  **╮•❐ الامـر ⦂ **`.شرح/.شرح + اسم الاضافه`
•  **الشـرح •• **__To get details/information/usage of that plugin__
•  **╮•❐ الامـر ⦂ **`.المراكز`
•  **الشـرح •• **__Shows your dc id and dc ids list__
•  **╮•❐ الامـر ⦂ **`.انلاين (تفعيل|تعطيل)`
•  **الشـرح •• **__Sets help menu either in inline or text format__"""
    }
)
