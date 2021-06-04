@JMTHOM

import os
from datetime import datetime

import aiohttp
import requests
from github import Github
from pySmartDL import SmartDL

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import reply_id

ppath = os.path.join(os.getcwd(), "temp", "githubuser.jpg")
plugin_category = "misc"

GIT_TEMP_DIR = "./temp/"


@catub.cat_cmd(
    pattern="بحث ريبو( -l(\d+))? (.*)",
    command=("بحث ريبو", plugin_category),
    info={
        "header": "Shows the information about an user on GitHub of given username",
        "flags": {"-l": "repo limit : default to 5"},
        "usage": ".github [flag] [username]",
        "examples": [".github sandy1709", ".github -l5 sandy1709"],
    },
)
async def _(event):
    "Get info about an GitHub User"
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_delete(event, "`" + username + " not found`")
            catevent = await edit_or_reply(event, "`fetching github info ...`")
            result = await request.json()
            photo = result["avatar_url"]
            if result["bio"]:
                result["bio"] = result["bio"].strip()
            repos = []
            sec_res = requests.get(result["repos_url"])
            if sec_res.status_code == 200:
                limit = event.pattern_match.group(2)
                limit = 5 if not limit else int(limit)
                for repo in sec_res.json():
                    repos.append(f"[{repo['name']}]({repo['html_url']})")
                    limit -= 1
                    if limit == 0:
                        break
            REPLY = "**GitHub معلومات الريبو** `{username}`\
                \n👤 **الاسم :** [{name}]({html_url})\
                \n🔧 **نوع :** `{type}`\
                \n🏢 **شركة :** `{company}`\
                \n🔭 **مدونة** : {blog}\
                \n📍 **موقع ** : `{location}`\
                \n📝 **بـايـو** : __{bio}__\
                \n❤️ **مـتـابـعـون** : `{followers}`\
                \n👁 **الـتـالـي** : `{following}`\
                \n📊 **إعادة الشراء العامة** : `{public_repos}`\
                \n📄 **الجماهير العامة** : `{public_gists}`\
                \n🔗 **تم إنشاء الملف الشخصي** : `{created_at}`\
                \n✏️ **تحديث الملف الشخصي** : `{updated_at}`".format(
                username=username, **result
            )

            if repos:
                REPLY += "\n🔍 **بعض الريبو** : " + " | ".join(repos)
            downloader = SmartDL(photo, ppath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
            await event.client.send_file(
                event.chat_id,
                ppath,
                caption=REPLY,
                reply_to=reply_to,
            )
            os.remove(ppath)
            await catevent.delete()


@catub.cat_cmd(
    pattern="commit$",
    command=("commit", plugin_category),
    info={
        "header": "To commit the replied plugin to github.",
        "description": "It uploads the given file to your github repo in **userbot/plugins** folder\
        \nTo work commit plugin set `GITHUB_ACCESS_TOKEN` and `GIT_REPO_NAME` Variables in Heroku vars First",
        "note": "As of now not needed i will sure develop it ",
        "usage": "{tr}commit",
    },
)
async def download(event):
    "To commit the replied plugin to github."
    if Config.GITHUB_ACCESS_TOKEN is None:
        return await edit_delete(
            event, "`Please ADD Proper Access Token from github.com`", 5
        )
    if Config.GIT_REPO_NAME is None:
        return await edit_delete(
            event, "`Please ADD Proper Github Repo Name of your userbot`", 5
        )
    mone = await edit_or_reply(event, "`Processing ...`")
    if not os.path.isdir(GIT_TEMP_DIR):
        os.makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        downloaded_file_name = await event.client.download_media(reply_message.media)
    except Exception as e:
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        await mone.edit("Committing to Github....")


async def git_commit(file_name, mone):
    content_list = []
    access_token = Config.GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name, "r", encoding="utf-8")
    commit_data = file.read()
    repo = g.get_repo(Config.GIT_REPO_NAME)
    print(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        print(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="' + file_name + '")':
            return await mone.edit("`File Already Exists`")
    if create_file:
        file_name = "userbot/plugins/" + file_name
        print(file_name)
        try:
            repo.create_file(
                file_name, "Uploaded New Plugin", commit_data, branch="master"
            )
            print("Committed File")
            ccess = Config.GIT_REPO_NAME
            ccess = ccess.strip()
            await mone.edit(
                f"`Commited On Your Github Repo`\n\n[Your PLUGINS](https://github.com/{ccess}/tree/master/userbot/plugins/)"
            )
        except BaseException:
            print("Cannot Create Plugin")
            await mone.edit("Cannot Upload Plugin")
    else:
        return await mone.edit("`Committed Suicide`")
