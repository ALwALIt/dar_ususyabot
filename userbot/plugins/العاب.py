# imported from uniborg credit goes to 
from telethon.tl.types import InputMediaDice
from . import jmthon
# EMOJI CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽️"
SLOT_E_MOJI = "🎰"
# EMOJI CONSTANTS


@jmthon.on(admin_cmd(pattern=f"({DART_E_MOJI}|سهم)( ([1-6])|$)"))
@jmthon.on(
    sudo_cmd(
        pattern=f"({DART_E_MOJI}|سهم)( ([1-6])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "سهم":
        emoticon = "🎯"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@jmthon.on(admin_cmd(pattern=f"({DICE_E_MOJI}|نرد)( ([1-6])|$)"))
@jmthon.on(
    sudo_cmd(
        pattern=f"({DICE_E_MOJI}|نرد)( ([1-6])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "نرد":
        emoticon = "🎲"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@jmthon.on(admin_cmd(pattern=f"({BALL_E_MOJI}|سلة)( ([1-5])|$)"))
@jmthon.on(
    sudo_cmd(
        pattern=f"({BALL_E_MOJI}|سلة)( ([1-5])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "سلة":
        emoticon = "🏀"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@jmthon.on(admin_cmd(pattern=f"({FOOT_E_MOJI}|قدم)( ([1-5])|$)"))
@jmthon.on(
    sudo_cmd(
        pattern=f"({FOOT_E_MOJI}|قدم)( ([1-5])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "قدم":
        emoticon = "⚽️"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@jmthon.on(admin_cmd(pattern=f"({SLOT_E_MOJI}|حظ)( ([1-64])|$)"))
@jmthon.on(
    sudo_cmd(
        pattern=f"({SLOT_E_MOJI}|حظ)( ([1-64])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "حظ":
        emoticon = "🎰"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


CMD_HELP.update(
    {
        "الالعاب": "**Syntax :** `.🎯 [1-6]` or `.سهم [1-6]`\
    \n**Usage : **each number shows different animation for dart\
    \n\n**Syntax : **`.🎲 [1-6]` or `.نرد [1-6]`\
    \n**Usage : **each number shows different animation for dice\
    \n\n**Syntax : **`.🏀 [1-5]` or `.سلة [1-5]`\
    \n**Usage : **each number shows different animation for basket ball\
    \n\n**Syntax : **`.⚽️ [1-5] `or `.قدم [1-5]`\
    \n**Usage : **each number shows different animation for football\
    \n\n**Syntax : **`.🎰 [1-64] `or `.حظ [1-64]`\
    \n**Usage : **each number shows different animation for slot machine(jackpot)\
    "
    }
)
