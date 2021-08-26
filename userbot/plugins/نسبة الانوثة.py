import html
import os
import random

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from userbot import jmthon

from ..Config import Config
from Jmthon.razan._fun import *
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch

plugin_category = "utils"


@jmthon.ar_cmd(
    pattern="نسبة الحب(?:\s|$)([\s\S]*)",
    command=("نسبة الحب", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1694386561:
        return await edit_or_reply(mention, f"**- انسـان بسـيط يحـب الكـل ويسـاعد الكـل 🖤،**")
    if user.id == 1715051616:
        return await edit_or_reply(mention, f"**- انسـان بسـيط يحـب الكـل ويسـاعد الكـل 🖤،**")
    if user.id == 1657933680:
        return await edit_or_reply(mention, f"**- انسـان بسـيط يحـب الكـل ويسـاعد الكـل 🖤،**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rza = random.choice(roz)
    await edit_or_reply(mention, f"نـسـبتكم انـت و [{muh}](tg://user?id={user.id}) هـي {rza} 😔🖤")
    
    
   
@jmthon.ar_cmd(
    pattern="نسبة الانوثة(?:\s|$)([\s\S]*)",
    command=("نسبة الانوثة", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1715051616:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور زلمة وعلى راسك**")
    if user.id == 1694386561:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور زلمة وعلى راسك**")
    if user.id == 1657933680:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور زلمة وعلى راسك**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    sos = random.choice(rr7)
    await edit_or_reply(mention, f"⌔︙ نسبة الانوثة لـ [{muh}](tg://user?id={user.id}) هـي {sos} 🥵🖤")
