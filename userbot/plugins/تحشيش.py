import html
import os

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from userbot import jmthon
from Jmthon.razan.resources.strings import *

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch
from telethon.utils import get_display_name
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format

plugin_category = "utils"



#كـتابة المـلف وتعديل.    :   السيد حسين.   اخمط وسمي روحك مطور فرخي 😂
# اذا انت ابن حرام اخمط 😂
# اي بعدك تريد تخمط ترا من تخمط مراح تنجح

@jmthon.on(admin_cmd(pattern="رفع مرتي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    jepthon = user.last_name.replace("\u2060", "") if user.last_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"🚻 ** ⌯︙ المستخدم => • ** [{jepthon}](tg://user?id={user.id}) \n ☑️ **⌯︙ تم رفعها مرتك بواسطه  :**{my_mention} 👰🏼‍♀️.\n**⌯︙ يلا حبيبي امشي نخلف بيبي 👶🏻🤤** ")

@jmthon.on(admin_cmd(pattern="رفع جلب(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه جلب 🐶 بواسطة :** {my_mention} \n**⌯︙ خليه خله ينبح 😂**")

@jmthon.on(admin_cmd(pattern="رفع تاج(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"⌯︙المستخدم [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه تاج بواسطة :** {my_mention} 👑🔥")

@jmthon.on(admin_cmd(pattern="رفع قرد(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"⌯︙المستخدم [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه قرد واعطائه موزة 🐒🍌 بواسطة :** {my_mention}")

@jmthon.on(admin_cmd(pattern="رفع بكلبي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه بكلـبك 🤍 بواسطة :** {my_mention} \n**⌯︙ انت حبي الابدي 😍**")
    
    

@jmthon.on(admin_cmd(pattern="رفع مطي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه مطي 🐴 بواسطة :** {my_mention} \n**⌯︙ تعال حبي استلم العربانه **")
    
#كـتابة المـلف وتعديل.    :   السيد حسين.   اخمط وسمي روحك مطور فرخي 😂
# اذا انت ابن حرام اخمط 😂
# اي بعدك تريد تخمط ترا من تخمط مراح تنجح


@jmthon.on(admin_cmd(pattern="رفع زوجي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه زوجج بواسطة :** {my_mention} \n**⌯︙ يلا حبيبي امشي نخلف 🤤🔞**")
    

@jmthon.on(admin_cmd(pattern="رفع زاحف(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفع المتهم زاحف اصلي بواسطة :** {my_mention} \n**⌯︙ ها يلزاحف شوكت تبطل سوالفك حيوان 😂🐍**")

@jmthon.on(admin_cmd(pattern="رفع كحبة(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفع المتهم كحبة 👙 بواسطة :** {my_mention} \n**⌯︙ ها يلكحبة طوبز خلي انيجك/ج**")

@jmthon.on(admin_cmd(pattern="رفع فرخ(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه فرخ الكروب بواسطة :** {my_mention} \n**⌯︙ لك الفرخ استر على خمستك ياهو اليجي يزورهاً 👉🏻👌🏻**")

@jmthon.ar_cmd(
    pattern="رزله(?:\s|$)([\s\S]*)",
    command=("رزله", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور **")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌯︙ولك [{tag}](tg://user?id={user.id}) \n⌯︙ هيو لتندك بسيادك لو بهاي 👞👈")

@jmthon.on(admin_cmd(pattern="رفع حاته(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـها حاته الكروب 🤤😻 بواسطة :** {my_mention} \n**⌯︙ تعاي يعافيتي اريد حضن دافي 😽**")

@jmthon.on(admin_cmd(pattern="رفع هايشة(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه المتهم هايشة 🐄 بواسطة :** {my_mention} \n**⌯︙ ها يلهايشة خوش بيك حليب تعال احلبك 😂**")

@jmthon.on(admin_cmd(pattern="رفع صاك(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    jepthon = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**⌯︙المستخدم** [{jepthon}](tg://user?id={user.id}) \n**⌯︙ تـم رفعـه صاك 🤤 بواسطة :** {my_mention} \n**⌯︙ تعال يلحلو انطيني بوسة من رگبتك 😻🤤**")

@jmthon.ar_cmd(
    pattern="مصه(?:\s|$)([\s\S]*)",
    command=("مصه", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    if user.id == 705475246:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور **")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"** ⣠⡶⠚⠛⠲⢄⡀\n⣼⠁      ⠀⠀⠀⠳⢤⣄\n⢿⠀⢧⡀⠀⠀⠀⠀⠀⢈⡇\n⠈⠳⣼⡙⠒⠶⠶⠖⠚⠉⠳⣄\n⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄\n⠀⠀⠀⠘⣆       ⠀⠀⠀⠀⠀⠈⠓⢦⣀\n⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⢤\n⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧\n⠀⠀⠀⠀⠀⠀⠀    ⠓⠦⠀⠀⠀⠀**\n**🚹 ¦ تعال مصه عزيزي ** [{tag}](tg://user?id={user.id})")

@jmthon.on(admin_cmd(pattern="تعليك(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    await edit_or_reply(mention, f"https://t.me/ThemeJep/95")
##RR9R7 
