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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفعـه مـࢪتك مـشي نخـلف 😹🤤")

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
    await edit_or_reply(mention, f"⌯︙المستخدم [{tag}](tg://user?id={user.id}) \n⌯︙ تـم رفـعه مطي هـنا ")
    
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
    await edit_or_reply(mention, f"⌯︙المتهم [{tag}](tg://user?id={user.id}) \n⌯︙تم رفعه في قائمة الزواحف ")


##RR9R7
