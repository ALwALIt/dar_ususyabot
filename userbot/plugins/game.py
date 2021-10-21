import asyncio

from userbot import jmthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "fun"

game_code = ["لعبة1", "لعبة2", "لعبة3", "لعبة4", "لعبة5", "لعبة6", "لعبة7", "لعبة8"]
button = ["0", "1", "2", "3", "4", "5", "6", "7"]
game_name = [
    "Tic-Tac-Toe",
    "Tic-Tac-Four",
    "Connect Four",
    "Rock-Paper-Scissors",
    "Rock-Paper-Scissors-Lizard-Spock",
    "Russian Roulette",
    "Checkers",
    "Pool Checkers",
]
game_list = "1.`لعبة1` :- Tic-Tac-Toe\n2.`لعبة2` :- Tic-Tac-Four\n3.`لعبة3` :- Connect Four\n4.`لعبة4` :- Rock-Paper-Scissors\n5.`لعبة5` :- Rock-Paper-Scissors-Lizard-Spock\n6.`لعبة6` :- Russian Roulette\n7.`لعبة7` :- Checkers\n8.`لعبة8` :- Pool Checkers"


@jmthon.ar_cmd(
    pattern="بلي(?:\s|$)([\s\S]*)",
    command=("بلي", plugin_category),
    info={
        "header": "Play inline games",
        "description": "Start an inline game by inlinegamebot",
        "Game code & Name": {
            "لعبة1": "تيك تاك تو",
            "لعبة2": "تيك تاك فور",
            "لعبة3": "ربط اربعه",
            "لعبة4": "حجر ورقة مقص",
            "لعبة5": "حجر ورقه مقص زار",
            "لعبة6": "روليت",
            "لعبة7": "تشيكرز",
            "لعبة8": "بول تشيكرز",
        },
        "usage": "{tr}game <game code>",
        "examples": "{tr}game ttt ",
    },
)
async def igame(event):
    "Fun game by inline"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    data = dict(zip(game_code, button))
    name = dict(zip(game_code, game_name))
    if not input_str:
        await edit_delete(
            event, f"**Available Game Codes & Names :-**\n\n{game_list}", time=60
        )
        return
    if input_str not in game_code:
        catevent = await edit_or_reply(event, "`Give me a correct game code...`")
        await asyncio.sleep(1)
        await edit_delete(
            catevent, f"**Available Game Codes & Names :-**\n\n{game_list}", time=60
        )
    else:
        game = data[input_str]
        gname = name[input_str]
        await edit_or_reply(
            event, f"**Game code `{input_str}` is selected for game:-** __{gname}__"
        )
        await asyncio.sleep(1)
        bot = "@inlinegamesbot"
        results = await event.client.inline_query(bot, gname)
        await results[int(game)].click(event.chat_id, reply_to=reply_to_id)
        await event.delete()
