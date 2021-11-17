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

plugin_category = "utils"



#كـتابة المـلف وتعديل.    :   محـمد الـزهيري.   اخمط وسمي روحك مطور فرخي 😂
# اذا انت ابن حرام اخمط 😂
# اي بعدك تريد تخمط ترا من تخمط مراح تنجح

@jmthon.ar_cmd(
    pattern="رفع مرتي(?:\s|$)([\s\S]*)",
    command=("رفع مرتي", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه مـࢪتك بواسطة {my_mention} \n⌯︙يلا حبيبي جاهز/ه نخلف بيبي 👶🏻🤤")

@jmthon.ar_cmd(
    pattern="رفع جلب(?:\s|$)([\s\S]*)",
    command=("رفع جلب", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه جلب خليه خله ينبح 😂🐶")

@jmthon.ar_cmd(
    pattern="رفع تاج(?:\s|$)([\s\S]*)",
    command=("رفع تاج", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه تاج 👑🔥")

@jmthon.ar_cmd(
    pattern="رفع قرد(?:\s|$)([\s\S]*)",
    command=("رفع قرد", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه قرد واعطائه موزة 🐒🍌")

@jmthon.ar_cmd(
    pattern="رفع بكلبي(?:\s|$)([\s\S]*)",
    command=("رفع بكلبي", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه بڪلبك 🖤 ")
    
    
@jmthon.ar_cmd(
    pattern="رفع مطي(?:\s|$)([\s\S]*)",
    command=("رفع مطي", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تم رفعه مطي في الكروب \n⌯︙ تعال حبي استلم العربانه")
    
#كـتابة المـلف وتعديل.    :   محـمد الـزهيري.   اخمط وسمي روحك مطور فرخي 😂
# اذا انت ابن حرام اخمط 😂
# اي بعدك تريد تخمط ترا من تخمط مراح تنجح


@jmthon.ar_cmd(
    pattern="رفع زوجي(?:\s|$)([\s\S]*)",
    command=("رفع زوجي", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙تـم رفعه زوجج روحوا خلفوا 🤤😂")
    

@jmthon.ar_cmd(
    pattern="رفع زاحف(?:\s|$)([\s\S]*)",
    command=("رفع زاحف", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المتهم [{tag}](tg://user?id={user.id}) \n⌯︙تم رفعه في قائمة الزواحف ، لك حيوان شوكت تبطل سوالفك 😂🐍 ")

@jmthon.ar_cmd(
    pattern="رفع كحبة(?:\s|$)([\s\S]*)",
    command=("رفع كحبة", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه كحبة تعال يلكحبة طوبز خلي انيجك 👌🏻👉🏻")

@jmthon.ar_cmd(
    pattern="رفع فرخ(?:\s|$)([\s\S]*)",
    command=("رفع فرخ", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه فرخ الكروب لكك فرخ استر على خمستك كام ياهو الي يجي يزورها 😉🤤")

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

@jmthon.ar_cmd(
    pattern="رفع حاته(?:\s|$)([\s\S]*)",
    command=("رفع حاته", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدمه [{tag}](tg://user?id={user.id}) \n⌯︙ تم رفعها حاته بلكروب  \n⌯︙ تعال يعافيتي الحاته اريد حضن 🥺❤️")

@jmthon.ar_cmd(
    pattern="رفع بقره(?:\s|$)([\s\S]*)",
    command=("رفع بقره", plugin_category),
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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تم رفعه بقره في الكروب  \n⌯︙ ها يلهايشه خوش بيك حليب تع احلبك 😹🐄")

@jmthon.ar_cmd(
    pattern="رفع صاك(?:\s|$)([\s\S]*)",
    command=("رفع صاك", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تم رفعه صاك بلكروب \n⌯︙تعال حبي الصاك نطيني بوسه من الحلق 😻🙊")

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

##RR9R7 
