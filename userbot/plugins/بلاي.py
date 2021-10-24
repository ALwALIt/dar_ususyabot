from . import R

@icssbot.on(icss_cmd(pattern="بلاي$"))
@icssbot.on(sudo_cmd(pattern="بلاي$", allow_sudo=True))
async def icsrepo(icsp):
    await eor(icsp, R)
