import re
from ..helpers.utils import reply_id as rd
from userbot import jmthon

@jmthon.on(admin_cmd(outgoing=True, pattern="ص1$"))
async def iqvois(vois):
    if vois.fwd_from:
        return
    Ti = await rd(vois)
    if iqvois1:
        await vois.client.send_file(vois.chat_id, iqvois1, reply_to=Ti)
        await vois.delete()
