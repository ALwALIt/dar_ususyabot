from json import dump, load
from math import ceil
from os.path import join as ospjoin
from random import choice
from re import compile, findall
from time import time
from uuid import uuid4

from telethon import Button
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.types import (
    InputBotInlineMessageMediaAuto,
    InputBotInlineResult,
    InputWebDocument,
)
from youtubesearchpython import VideosSearch

from userbot import jmthon, tr

from ..Config import Config
from ..helpers.functions import rand_key
from ..helpers.functions.utube import (
    download_button,
    get_yt_video_id,
    get_ytthumb,
    result_formatter,
    ytsearch_data,
)
from ..plugins import mention
from ..sql_helper.globals import gvar
from . import CMD_INFO, GRP_INFO, PLG_INFO, check_owner
from .logger import logging

LOGS = logging.getLogger(__name__)

BTN_URL_REGEX = compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
ROZLOGO = "https://telegra.ph/file/e76bb41ff12a7e8b71e3c.mp4"


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


def main_menu():
    text = f"**- [سـورس جـمثون](https://t.me/JMTHON)\
        \n المسـاعد\
        \n\
        \n◽ جمثـون لـ {mention}**"
    buttons = [
        (
            Button.inline(
                f"ℹ️️ INFO ℹ️",
                data="check",
            ),
        ),
        (
            Button.inline(
                f"👮‍♂️ Aᴅᴍɪɴ ({len(GRP_INFO['admin'])})",
                data=f"admin_menu",
            ),
            Button.inline(
                f"🤖 Boᴛ ({len(GRP_INFO['bot'])})",
                data=f"bot_menu",
            ),
        ),
        (
            Button.inline(
                f"🎈 Fᴜɴ ({len(GRP_INFO['fun'])})",
                data=f"fun_menu",
            ),
            Button.inline(
                f"🪀 Mɪsᴄ ({len(GRP_INFO['misc'])})",
                data=f"misc_menu",
            ),
        ),
        (
            Button.inline(
                f"🧰 Tooʟ ({len(GRP_INFO['tool'])})",
                data=f"tool_menu",
            ),
        ),
        (
            Button.inline(
                f"⛔ CLOSE ⛔",
                data=f"close",
            ),
        ),
    ]
    return text, buttons


def command_in_category(cname):
    cmds = 0
    for i in GRP_INFO[cname]:
        for _ in PLG_INFO[i]:
            cmds += 1
    return cmds


def paginate_help(
    page_number,
    loaded_plugins,
    prefix,
    plugins=True,
    category_plugins=None,
    category_pgno=0,
):  # sourcery no-metrics
    try:
        number_of_rows = int(gvar("NO_OF_ROWS_IN_HELP") or 6)
    except (ValueError, TypeError):
        number_of_rows = 6
    try:
        number_of_cols = int(gvar("NO_OF_COLUMNS_IN_HELP") or 2)
    except (ValueError, TypeError):
        number_of_cols = 2
    HELP_EMOJI = gvar("HELP_EMOJI") or " "
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    if len(HELP_EMOJI) == 2:
        if plugins:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_prev(1)_command_{prefix}_{page_number}",
                )
                for x in helpable_plugins
            ]
        else:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
                )
                for x in helpable_plugins
            ]
    elif plugins:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_prev(1)_command_{prefix}_{page_number}",
            )
            for x in helpable_plugins
        ]
    else:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
            )
            for x in helpable_plugins
        ]
    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    elif len(modules) % number_of_cols == 2:
        pairs.append((modules[-2], modules[-1]))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if plugins:
        if len(pairs) > number_of_rows:
            pairs = pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [
                (
                    Button.inline(
                        "⏪",
                        data=f"{prefix}_prev({modulo_page})_plugin",
                    ),
                    Button.inline(
                        "🐾 Mᴇɴᴜ",
                        data="mainmenu",
                    ),
                    Button.inline(
                        "⏩",
                        data=f"{prefix}_next({modulo_page})_plugin",
                    ),
                ),
                (
                    Button.inline(
                        "⛔ Cʟosᴇ",
                        data="close",
                    ),
                ),
            ]
        else:
            pairs = pairs + [
                (
                    Button.inline("🐾 Mᴇɴᴜ", data="mainmenu"),
                    Button.inline("⛔ Cʟosᴇ", data="close"),
                ),
            ]
    elif len(pairs) > number_of_rows:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "⏪",
                    data=f"{prefix}_prev({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "⏩",
                    data=f"{prefix}_next({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
            ),
            (
                Button.inline(
                    "⬅️️ Bᴀᴄᴋ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "🐾 Mᴇɴᴜ",
                    data="mainmenu",
                ),
                Button.inline("⛔ Cʟosᴇ", data="close"),
            ),
        ]
    else:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs + [
            (
                Button.inline(
                    "⬅️️ Bᴀᴄᴋ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "🐾 Mᴇɴᴜ",
                    data="mainmenu",
                ),
                Button.inline("⛔ Cʟosᴇ", data="close"),
            ),
        ]
    return pairs


def get_back_button(name):
    button = [Button.inline("⬅️️ Bᴀᴄᴋ", data=f"{name}")]
    return button


@jmthon.tgbot.on(InlineQuery)
async def inline_handler(event):  # sourcery no-metrics
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        hmm = compile("troll (.*) (.*)")
        match = findall(hmm, query)
        inf = compile("sec (.*) (.*)")
        match2 = findall(inf, query)
        hid = compile("hide (.*)")
        match3 = findall(hid, query)
        if query.startswith("ㅤ") or query.startswith("JmthonUserbot"):
            buttons = [
                (
                    Button.url(" Jmthon UsᴇʀBoᴛ", "https://t.me/Jmthon"),
                    Button.inline("🐾 Iɴғo", data="infos"),
                )
            ]
            ALIVE_PIC = gvar("ALIVE_PIC")
            IALIVE_PIC = gvar("IALIVE_PIC")
            if IALIVE_PIC:
                RAZAN = [x for x in IALIVE_PIC.split()]
                PIC = list(RAZAN)
                I_IMG = choice(PIC)
            if not IALIVE_PIC and ALIVE_PIC:
                RAZAN = [x for x in ALIVE_PIC.split()]
                PIC = list(RAZAN)
                I_IMG = choice(PIC)
            elif not IALIVE_PIC:
                I_IMG = None
            if I_IMG and I_IMG.endswith((".jpg", ".png")):
                result = builder.photo(
                    I_IMG,
                    text=query,
                    buttons=buttons,
                )
            elif I_IMG:
                result = builder.document(
                    I_IMG,
                    title=" jmthon UserBot Alive",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title=" jmthon UserBot Alive",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
        elif query.startswith("Inline buttons"):
            markdown_note = query[14:]
            prev = 0
            note_data = ""
            buttons = []
            for match in BTN_URL_REGEX.finditer(markdown_note):
                n_escapes = 0
                to_check = match.start(1) - 1
                while to_check > 0 and markdown_note[to_check] == "\\":
                    n_escapes += 1
                    to_check -= 1
                if n_escapes % 2 == 0:
                    buttons.append(
                        (match.group(2), match.group(3), bool(match.group(4)))
                    )
                    note_data += markdown_note[prev : match.start(1)]
                    prev = match.end(1)
                elif n_escapes % 2 == 1:
                    note_data += markdown_note[prev:to_check]
                    prev = match.start(1) - 1
                else:
                    break
            else:
                note_data += markdown_note[prev:]
            message_text = note_data.strip()
            tl_ib_buttons = ibuild_keyboard(buttons)
            result = builder.article(
                title=" jmthon UserBot Buttons",
                text=message_text,
                buttons=tl_ib_buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
        elif match:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            troll = ospjoin("./userbot", "troll.txt")
            try:
                jsondata = load(open(troll))
            except Exception:
                jsondata = False
            try:
                # if u is user id
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        ROZ = f"@{u.username}"
                    else:
                        ROZ = f"[{u.first_name}](tg://user?id={u.id})"
                    u = int(u.id)
                except ValueError:
                    # ValueError: Couldn't find the input entity
                    ROZ = f"[user](tg://user?id={u})"
            except ValueError:
                # if u is username
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    ROZ = f"@{u.username}"
                else:
                    ROZ = f"[{u.first_name}](tg://user?id={u.id})"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time() * 2)
            newtroll = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline("🔐 عـرض الـرسـالة", data=f"troll_{timestamp}")]
            result = builder.article(
                title="رسـالة تـرول من سـورس جمـثون 🧸♥",
                text=f"🤡 فقـط {ROZ} هـو من قـادر عـلى رؤيتهـا",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newtroll)
                dump(jsondata, open(troll, "w"))
            else:
                dump(newtroll, open(troll, "w"))
        elif match2:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            secret = ospjoin("./userbot", "secrets.txt")
            try:
                jsondata = load(open(secret))
            except Exception:
                jsondata = False
            try:
                # if u is user id
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        ROZ = f"@{u.username}"
                    else:
                        ROZ = f"[{u.first_name}](tg://user?id={u.id})"
                    u = int(u.id)
                except ValueError:
                    # ValueError: Couldn't find the input entity
                    ROZ = f"[user](tg://user?id={u})"
            except ValueError:
                # if u is username
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    ROZ = f"@{u.username}"
                else:
                    ROZ = f"[{u.first_name}](tg://user?id={u.id})"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time() * 2)
            newsecret = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline("🔐 عـرض الـرسـالة", data=f"sec_{timestamp}")]
            result = builder.article(
                title=" همسـة سـرية من سـورس جمـثون 🧸♥",
                text=f"🧸♥ فقـط {ROZ} هـو من قـادر عـلى رؤيتهـا",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newsecret)
                dump(jsondata, open(secret, "w"))
            else:
                dump(newsecret, open(secret, "w"))
        elif match3:
            query = query[5:]
            builder = event.builder
            hide = ospjoin("./userbot", "hide.txt")
            try:
                jsondata = load(open(hide))
            except Exception:
                jsondata = False
            timestamp = int(time() * 2)
            newhide = {str(timestamp): {"text": query}}

            buttons = [Button.inline("🔏 قـراءة الرسـالة", data=f"hide_{timestamp}")]
            result = builder.article(
                title="رسـالة مخفيـة من سـورس جمـثون 🧸♥",
                text=f"ㅤ",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newhide)
                dump(jsondata, open(hide, "w"))
            else:
                dump(newhide, open(hide, "w"))
        elif string == "help" or "jmthon":
            _result = main_menu()
            result = builder.article(
                title="Jmthon UserBot Help",
                description="Help Menu",
                text=_result[0],
                buttons=_result[1],
                link_preview=False,
            )
            await event.answer([result] if result else None)
        elif str_y[0].lower() == "yt" and len(str_y) == 2:
            link = get_yt_video_id(str_y[1].strip())
            found_ = True
            if link is None:
                search = VideosSearch(str_y[1].strip(), limit=15)
                resp = (search.result()).get("result")
                if len(resp) == 0:
                    found_ = False
                else:
                    outdata = await result_formatter(resp)
                    key_ = rand_key()
                    ytsearch_data.store_(key_, outdata)
                    buttons = [
                        Button.inline(
                            f"1 - {len(outdata)}",
                            data=f"ytdl_next_{key_}_1",
                        ),
                        Button.inline(
                            "📜 Lɪsᴛ Aʟʟ",
                            data=f"ytdl_listall_{key_}_1",
                        ),
                        Button.inline(
                            "⬇️ Doᴡɴʟoᴀᴅ",
                            data=f'ytdl_download_{outdata[1]["video_id"]}_0',
                        ),
                    ]
                    caption = outdata[1]["message"]
                    photo = await get_ytthumb(outdata[1]["video_id"])
            else:
                caption, buttons = await download_button(link, body=True)
                photo = await get_ytthumb(link)
            if found_:
                markup = event.client.build_reply_markup(buttons)
                photo = InputWebDocument(
                    url=photo, size=0, mime_type="image/jpeg", attributes=[]
                )
                text, msg_entities = await event.client._parse_message_text(
                    caption, "html"
                )
                result = InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=link,
                    description="⬇️ Doᴡɴʟoᴀᴅ",
                    thumb=photo,
                    content=photo,
                    send_message=InputBotInlineMessageMediaAuto(
                        reply_markup=markup, message=text, entities=msg_entities
                    ),
                )
            else:
                result = builder.article(
                    title="🙁 I couldn't find this",
                    text=f"🚨 No results found for `{str_y[1]}`",
                    description="INVALID",
                )
            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="🙁 I couldn't find this",
                            text=f"🚨 No results found for `{str_y[1]}`",
                            description="INVALID",
                        )
                    ]
                )
        elif string == "pmpermit":
            buttons = [
                Button.inline(text="🪐 الخـيارات", data="show_pmpermit_options"),
            ]
            PM_PIC = gvar("PM_PIC")
            if PM_PIC:
                RAZAN = [x for x in PM_PIC.split()]
                PIC = list(RAZAN)
                RAZAN_IMG = choice(PIC)
            else:
                RAZAN_IMG = None
            query = gvar("pmpermit_text")
            if RAZAN_IMG and RAZAN_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(
                    RAZAN_IMG,
                    # title="Alive RAZAN",
                    text=query,
                    buttons=buttons,
                )
            elif RAZAN_IMG:
                result = builder.document(
                    RAZAN_IMG,
                    title="Jmthon UserBot Alive",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="Jmthon UserBot Alive",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
    else:
        buttons = [
            (
                Button.url("قنـاة السـورس ⚒️", "https://t.me/Jmthon"),
                Button.url(
                    "كـروب المـساعدة 📬",
                    "https://t.me/GroupJmthon",
                ),
            )
        ]
        markup = event.client.build_reply_markup(buttons)
        photo = InputWebDocument(
            url=ROZLOGO, size=0, mime_type="image/jpeg", attributes=[]
        )
        text, msg_entities = await event.client._parse_message_text(
            "**[بـوت جـمثـون 🧸♥](https://t.me/Jmthon)**\
            \n\
            \n❤ جمثـون هـو بـوت بسـيط يدخـل الـى حسـابك لجعـلك تتحـكم به معـ اوامـر معينـة.\
            \n\
            \n**اذا كـنت تـرغب بتـنصيـب السـورس عـلى حسـابك ,\
            \n🐾 تعال الـى [كروب المسـاعدة](https://t.me/GroupJmthon)!**",
            "md",
        )
        result = InputBotInlineResult(
            id=str(uuid4()),
            type="photo",
            title="Jmthon UserBot 🧸♥",
            description="ادخـل كـروب المسـاعدة",
            url="https://t.me/GroupJmthon",
            thumb=photo,
            content=photo,
            send_message=InputBotInlineMessageMediaAuto(
                reply_markup=markup, message=text, entities=msg_entities
            ),
        )
        await event.answer([result] if result else None)


@jmthon.tgbot.on(CallbackQuery(data=compile(b"close")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    buttons = [
        (Button.inline("القائمة", data="mainmenu"),),
    ]
    await event.edit(
        f"**[سـورس جـمثون 🧸♥](https://t.me/Jmthon)\
        \n\
        \n◽ مالك البـوت هـو {mention}**",
        buttons=buttons,
        link_preview=False,
    )


@jmthon.tgbot.on(CallbackQuery(data=compile(b"check")))
async def on_plugin_callback_query_handler(event):
    text = f"سـورس جـمثـون\
            \n\
            \n🧩 Pʟᴜɢɪɴs: {len(PLG_INFO)}\
            \n⌨️ Coᴍᴍᴀɴᴅs: {len(CMD_INFO)}\
            \n\
            \n{tr}jmthon .c <command>: For any command info.\
            \n{tr}s <query>: To search any commands."
    await event.answer(text, cache_time=0, alert=True)


@jmthon.tgbot.on(CallbackQuery(data=compile(b"(.*)_menu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    buttons = paginate_help(0, GRP_INFO[category], category)
    text = f"**[سورس جمثـون](https://t.me/Jmthon)\
            \n🐾 Hᴇʟᴘᴇʀ\
            \n\
            \n🗃 Cᴀᴛᴇɢoʀʏ: **{category}\
            \n**🧩 Pʟᴜɢɪɴs: **{len(GRP_INFO[category])}\
            \n**⌨️ Coᴍᴍᴀɴᴅs: **{command_in_category(category)}"
    await event.edit(text, buttons=buttons, link_preview=False)


@jmthon.tgbot.on(
    CallbackQuery(
        data=compile(b"back_([a-z]+)_([a-z1-9]+)_([0-9]+)_?([a-z1-9]+)?_?([0-9]+)?")
    )
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    mtype = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    if mtype == "plugin":
        buttons = paginate_help(pgno, GRP_INFO[category], category)
        text = f"**[سورس جمثـون](https://t.me/Jmthon)\
                \n🐾 Hᴇʟᴘᴇʀ\
                \n\
                \n🗃 Cᴀᴛᴇɢoʀʏ: **{category}\
                \n**🧩 Pʟᴜɢɪɴs: **{len(GRP_INFO[category])}\
                \n**⌨️ Coᴍᴍᴀɴᴅs: **{command_in_category(category)}"
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            pgno,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**[سورس جمثـون](https://t.me/Jmthon)\
                \n🐾 Hᴇʟᴘᴇʀ\
                \n\
                \n🧩 Pʟᴜɢɪɴ: **{category}\
                \n**🗃 Cᴀᴛᴇɢoʀʏ: **{getkey(category)}\
                \n**⌨️ Coᴍᴍᴀɴᴅs: **{len(PLG_INFO[category])}"
    await event.edit(text, buttons=buttons, link_preview=False)


@jmthon.tgbot.on(CallbackQuery(data=compile(rb"mainmenu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    _result = main_menu()
    await event.edit(_result[0], buttons=_result[1], link_preview=False)


@jmthon.tgbot.on(
    CallbackQuery(data=compile(rb"(.*)_prev\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number - 1, GRP_INFO[category], category)
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            current_page_number - 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**[سورس جمثـون](https://t.me/Jmthon)\
                \n🐾 Hᴇʟᴘᴇʀ\
                \n\
                \n🧩 Pʟᴜɢɪɴ: **{category}\
                \n**🗃 Cᴀᴛᴇɢoʀʏ: **{getkey(category)}\
                \n**⌨️ Coᴍᴍᴀɴᴅs: **{len(PLG_INFO[category])}"
        try:
            return await event.edit(text, buttons=buttons, link_preview=False)
        except Exception as e:
            LOGS.error(str(e))
    await event.edit(buttons=buttons, link_preview=False)


@jmthon.tgbot.on(
    CallbackQuery(data=compile(rb"(.*)_next\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = event.pattern_match.group(4)
    if category_plugins:
        category_plugins = str(category_plugins.decode("UTF-8"))
    category_pgno = event.pattern_match.group(5)
    if category_pgno:
        category_pgno = int(category_pgno.decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number + 1, GRP_INFO[category], category)
    else:
        buttons = paginate_help(
            current_page_number + 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
    await event.edit(buttons=buttons, link_preview=False)


@jmthon.tgbot.on(
    CallbackQuery(data=compile(b"(.*)_cmdhelp_([a-z1-9]+)_([0-9]+)_([a-z]+)_([0-9]+)"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    cmd = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
    category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
    buttons = [
        (
            Button.inline(
                "⬅️️ Bᴀᴄᴋ",
                data=f"back_command_{category}_{pgno}_{category_plugins}_{category_pgno}",
            ),
            Button.inline(
                "🐾 Mᴇɴᴜ",
                data="mainmenu",
            ),
            Button.inline(
                "⛔ Cʟosᴇ",
                data="close",
            ),
        ),
    ]
    text = f"**[سورس جمثـون](https://t.me/Jmthon)\
            \n🐾 Hᴇʟᴘᴇʀ\
            \n\
            \n⌨️ Coᴍᴍᴀɴᴅ: **`{tr}{cmd}`\
            \n**🧩 Pʟᴜɢɪɴ: **{category}\
            \n**🗃 Cᴀᴛᴇɢoʀʏ: **{category_plugins}\
            \n\
            \n**ℹ️ Iɴғo:**\n{CMD_INFO[cmd][0]}"
    await event.edit(text, buttons=buttons, link_preview=False)
