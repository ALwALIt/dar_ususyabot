

import asyncio
import random
import glob
import re
import shutil
import urllib
import base64
import requests
import time
import os
import html
import telethon.password as pwd_mod
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.events import CallbackQuery
from telethon.errors import FloodWaitError
from telethon.tl import functions
from urlextract import URLExtract
from requests import get
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id, get_input_location
from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User
from telethon.errors.rpcerrorlist import UsernameOccupiedError
from asyncio.exceptions import TimeoutError as AsyncTimeout
from telethon.errors.rpcerrorlist import MessageTooLongError, YouBlockedUserError
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantsBots
from telethon.tl.types import DocumentAttributeVideo as video
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
from telethon.tl.types import InputMessagesFilterMusic
from telethon.tl.functions.messages import SaveDraftRequest
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from ..helpers.progress import humanbytes as hb
from userbot.utils import admin_cmd, sudo_cmd, eor
from telethon.utils import get_display_name
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from ..helpers.utils import reply_id as rd
from telethon.tl.types import Channel, Chat, InputPhoto, User
from userbot import jmthon
from userbot.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from . import ALIVE_NAME, AUTONAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO, get_user_from_event
from ..helpers import get_user_from_event, reply_id
from ..sql_helper.locks_sql import *
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..sql_helper.global_list import add_to_list, get_collection_list, is_in_list, rm_from_list
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import AUTONAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO, _catutils, edit_delete, iqthon, logging, spamwatch    

@jmthon.on(admin_cmd(outgoing=True, pattern="ص1$"))
async def jpvois(vois):
    if vois.fwd_from:
        return
    Ti = await rd(vois)
    if jpvois1:
        await vois.client.send_file(vois.chat_id, jpvois1, reply_to=Ti)
        await vois.delete()
