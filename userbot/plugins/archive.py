import asyncio
import io
import os
import time
import zipfile
from datetime import datetime
from pathlib import Path
from tarfile import is_tarfile
from tarfile import open as tar_open

from telethon import types
from telethon.utils import get_extension

from ..Config import Config
from . import catub, edit_delete, edit_or_reply, progress

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
plugin_category = "misc"


def zipdir(dirName):
    filePaths = []
    for root, directories, files in os.walk(dirName):
        for filename in files:
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    return filePaths


@catub.cat_cmd(
    pattern="ضغط(?: |$)(.*)",
    command=("ضغط", plugin_category),
    info={
        "header": "To compress the file/folders",
        "description": "سيتم إنشاء ملف مضغوط لمسار الملف المحدد أو مسار المجلد",
        "usage": [
            "{tr}zip <file/folder path>",
        ],
        "examples": ["{tr}zip downloads", "{tr}zip sample_config.py"],
    },
)
async def zip_file(event):
    "To create zip file"
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(event, "`توفير مسار الملف إلى zip`")
    start = datetime.now()
    if not os.path.exists(Path(input_str)):
        return await edit_or_reply(
            event,
            f"لا يوجد مثل هذا الدليل أو الملف بالاسم `{input_str}` تحقق مرة اخرى",
        )
    if os.path.isfile(Path(input_str)):
        return await edit_delete(event, "`ضغط الملف لم يتم تنفيذه بعد`")
    mone = await edit_or_reply(event, "`جارٍ الضغط....`")
    filePaths = zipdir(input_str)
    filepath = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY, os.path.basename(Path(input_str))
    )
    zip_file = zipfile.ZipFile(filepath + ".zip", "w")
    with zip_file:
        for file in filePaths:
            zip_file.write(file)
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"Zipped the path `{input_str}` into `{filepath+'.zip'}` in __{ms}__ Seconds"
    )

@catub.cat_cmd(
    pattern="فك الضغط(?: |$)(.*)",
    command=("فك الضغط", plugin_category),
    info={
        "header": "لفك ضغط ملف مضغوط معين",
        "description": "الرد على ملف مضغوط أو توفير مسار ملف مضغوط بأمر لفك ضغط الملف المحدد الرد على ملف مضغوط أو توفير مسار ملف مضغوط بأمر لفك ضغط الملف",
        "usage": [
            "{tr}unzip <reply/file path>",
        ],
    },
)
async def zip_file(event):  # sourcery no-metrics
    "To unpack the zip file"
    input_str = event.pattern_match.group(1)
    if input_str:
        path = Path(input_str)
        if os.path.exists(path):
            start = datetime.now()
            if not zipfile.is_zipfile(path):
                return await edit_delete(
                    event, f"`الطريق المعطى {str(path)} ليس ملف مضغوط لفك ضغطه`"
                )
            mone = await edit_or_reply(event, "`تفريغ....`")
            destination = os.path.join(
                Config.TMP_DOWNLOAD_DIRECTORY,
                os.path.splitext(os.path.basename(path))[0],
            )
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(destination)
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                f"فك ضغطها وتخزينها في ملفات `{destination}` \n**الوقت المستغرق :** `{ms} ثواني`"
            )
        else:
            await edit_delete(event, f"لا أستطيع أن أجد هذا الطريق `{input_str}`", 10)
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        ext = get_extension(reply.document)
        if ext != ".zip":
            return await edit_delete(
                event,
                "`الملف الذي تم الرد عليه ليس ملف مضغوط أعد التحقق من الرسالة التي تم الرد عليها`",
            )
        mone = await edit_or_reply(event, "`تفريغ....`")
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                filename = attr.file_name
        filename = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, filename)
        c_time = time.time()
        try:
            dl = io.FileIO(filename, "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
            dl.close()
        except Exception as e:
            return await edit_delete(mone, f"**Error:**\n__{str(e)}__")
        await mone.edit("`Download finished Unpacking now`")
        destination = os.path.join(
            Config.TMP_DOWNLOAD_DIRECTORY,
            os.path.splitext(os.path.basename(filename))[0],
        )
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(destination)
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            f"unzipped and stored to `{destination}` \n**Time Taken :** `{ms} seconds`"
        )
        os.remove(filename)
    else:
        await edit_delete(
            mone,
            "`Either reply to the zipfile or provide path of zip file along with command`",
        )
