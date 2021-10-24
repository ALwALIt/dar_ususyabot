from . import jmthon

@jmthon.on(icss_cmd(pattern="بلاي$"))
@jmthon.on(sudo_cmd(pattern="بلاي$", allow_sudo=True))
async def icsrepo(icsp):
    await eor(icsp, R)
