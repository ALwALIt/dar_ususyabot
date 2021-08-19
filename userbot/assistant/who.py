# Whois jmthon Userbot 
# from ~ @RR9R7

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
import os


@asst_cmd("ايدي")
@owner
async def who(event):
    replied_user = await get_user(event)
    try:
        caption = await detail(replied_user, event)
    except AttributeError:
        event.edit("لا استطيع جلب معلومات الشخص")
        return
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    await event.reply(caption, parse_mode="html")


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await asst(GetFullUserRequest(previous_message.sender_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.get_sender()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await asst(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await asst.get_entity(user)
            replied_user = await asst(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.reply("هـذا الشخـص غيـر موجودفي قاعـدة البيانات...)")
            return None

    return replied_user

async def detail(replied_user, event):
 try:
    pro = await bot.get_me()
    boy = pro.id
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    username = replied_user.user.username
    first_name = (
        first_name.replace("\u2060", "")
    )
    last_name = (
        last_name.replace("\u2060", "") if last_name else None
    )
    username = "@{}".format(username) if username else None

    caption = "<b>╔═══*.·:·.☽✧ معلـومات المستخدم: ✧☾.·:·.*═══╗</b> \n"
    caption += f"<b>➥ الايدي:</b> <code>{user_id}</code> \n"
    caption += f"<b>➥ الاسم الاول:</b> <code>{first_name}</code> \n"
    if last_name:
      caption += f"<b>➥ الاسم الثاني:</b> <code>{last_name}</code> \n"
    if username:
      caption += f"<b>➥ المعـرف:</b> <i>{username}</i> \n"
    caption += f'<b>➥ رابط الحساب:</b> <i><a href="tg://user?id={user_id}">Perma Link</a></i>'
    if user_id in kimo:
        caption += "\n<b>╚⊶⊶⊶⊶⊶ هـذا مطـوري ;) ⊷⊷⊷⊷⊷╝</b>"
    if not event.sender_id == boy:
       if user_id == boy:
        caption += "\n<b>╚⊶⊶⊶⊶⊶ هـذا مالـك الـبوت ⊷⊷⊷⊷⊷╝</b>"
    elif event.sender_id == boy and user_id == boy:
        caption += "\n<b>مـرحبـا ايهـا المـالك</b>"
    return caption
 except Exception:
        print("lel")
