from telethon.errors import BadRequestError
from telethon.tl import functions
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from ..Config import Config
from . import catub, edit_or_reply

plugin_category = "tools"


@catub.cat_cmd(
    pattern="انشاء (كروب خاص|كروب|قناة) (.*)",
    command=("create", plugin_category),
    info={
        "header": "لإنشاء مجموعة / قناة خاصة باستخدام برنامج Userbot",
        "description": "استخدم cmd هذا لإنشاء مجموعة فائقة أو مجموعة أو قناة عادية",
        "flags": {
            "b": "لإنشاء مجموعة فائقة خاصة",
            "g": "لإنشاء مجموعة أساسية خاصة",
            "c": "لإنشاء قناة خاصة",
        },
        "usage": "{tr}create (b|g|c) <name of group/channel>",
        "examples": "{tr}create b catuserbot",
    },
)
async def _(event):
    "لإنشاء مجموعة / قناة خاصة باستخدام برنامج Userbot"
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "قناة":
        descript = "هذه قناة اختبار تم إنشاؤها باستخدام برنامج جمثون @JMTHON"
    else:
        descript = "هذه مجموعة اختبار تم إنشاؤها باستخدام جمثون @JMTHON"
    event = await edit_or_reply(event, "جار انشاء ..")
    flag = False
    if type_of_group == "كروب خاص":
        try:
            new_rights = ChatAdminRights(
                add_admins=False,
                invite_users=True,
                change_info=False,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
            )
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "كروب `{}` تم إنشاؤها بنجاح رابط الكروب  : {}".format(
                    group_name, result.link
                )
            )
            flag = True
            try:
                rank = "admin"
                p = await event.client.get_entity(Config.TG_BOT_USERNAME)
                result = await event.client(
                    EditAdminRequest(created_chat_id, p.id, new_rights, rank)
                )
            except BadRequestError:
                pass
        except Exception as e:
            if not flag:
                await event.edit(str(e))
            else:
                LOGS.error(e)
    elif type_of_group in ["كروب", "قناة"]:
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=type_of_group != "قناة",
                )
            )

            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await event.edit(
                "قناة `{}` تم إنشاؤها بنجاح رابط القناة للانضمام : {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("Read `.مساعدة` يمكنك إرسال أمر المساعده للمساعدة")
