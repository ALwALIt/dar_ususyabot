import asyncio
#
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP
from userbot.utils import admin_cmd
from userbot import CMD_HELP


@borg.on(admin_cmd(pattern="بحث ?(.*)"))
async def FindMusicPleaseBot(roz):

    song = roz.pattern_match.group(1)

    chat = "@FindMusicPleaseBot"

    if not song:

        return await roz.edit("**- يجب وضع اسم الاغنية لبحثها اولا **")

    await roz.edit("⌔∮ يتم التعرف على الاغنية انتظر قليلا")
    await asyncio.sleep(2)

    async with bot.conversation(chat) as conv:

        await roz.edit("- جار تحميل الاغنية انتظر")

        try:

            await conv.send_message(song)

            response = await conv.get_response()

            if response.text.startswith("عذرا"):

                await bot.send_read_acknowledge(conv.chat_id)

                return await roz.edit(f"- لم يتم العثور على {song}")

            await conv.get_response()

            cobra = await conv.get_response()

        except YouBlockedUserError:

            await roz.edit(
                "• اولا الغي حظر هذا البوت @FindmusicpleaseBot\n واعد استخدام الامر مرة ثانية"
            )

            return

        await roz.edit("- يتم ارسال الاغنية انتظر لحضه")

        await bot.send_file(roz.chat_id, cobra)

        await bot.send_read_acknowledge(conv.chat_id)

    await roz.delete()
    
CMD_HELP.update(
    {
        "البحث": "\n.بحث <اسم الاغنية>\nيستخدم الامر للبحث عن اغنيه او مقطع صوتي اكتب الامر والعنوان فقط"
    }
)
