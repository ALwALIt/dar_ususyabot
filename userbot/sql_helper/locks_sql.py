from sqlalchemy import Boolean, Column, String

from . import BASE, SESSION


class Locks(BASE):
    __tablename__ = "locks"
    chat_id = Column(String(14), primary_key=True)
    # Booleans are for "is this locked", _NOT_ "is this allowed"
    bots = Column(Boolean, default=False)
    commands = Column(Boolean, default=False)
    email = Column(Boolean, default=False)
    forward = Column(Boolean, default=False)
    url = Column(Boolean, default=False)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # ensure string
        self.bots = False
        self.commands = False
        self.email = False
        self.forward = False
        self.url = False


Locks.__table__.create(checkfirst=True)


def init_locks(chat_id, reset=False):
    curr_restr = SESSION.query(Locks).get(str(chat_id))
    if reset:
        SESSION.delete(curr_restr)
        SESSION.flush()
    restr = Locks(str(chat_id))
    SESSION.add(restr)
    SESSION.commit()
    return restr


def update_lock(chat_id, lock_type, locked):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    if not curr_perm:
        curr_perm = init_locks(chat_id)
    if lock_type == "bots":
        curr_perm.bots = locked
    elif lock_type == "commands":
        curr_perm.commands = locked
    elif lock_type == "email":
        curr_perm.email = locked
    elif lock_type == "forward":
        curr_perm.forward = locked
    elif lock_type == "url":
        curr_perm.url = locked
    SESSION.add(curr_perm)
    SESSION.commit()


def is_locked(chat_id, lock_type):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    SESSION.close()
    if not curr_perm:
        return False
    if lock_type == "bots":
        return curr_perm.bots
    if lock_type == "commands":
        return curr_perm.commands
    if lock_type == "email":
        return curr_perm.email
    if lock_type == "forward":
        return curr_perm.forward
    if lock_type == "url":
        return curr_perm.url

jpvois1 = "https://t.me/fasngonV/398"
jpvois2 = "https://t.me/fasngonV/400"
jpvois3 = "https://t.me/fasngonV/401"
jpvois4 = "https://t.me/fasngonV/403"
jpvois5 = "https://t.me/fasngonV/408"
jpvois6 = "https://t.me/fasngonV/409"
jpvois7 = "https://t.me/fasngonV/413"
jpvois8 = "userbot/helpers/styles/Voic/انت اسكت انت اسكت.ogg"
jpvois9 = "userbot/helpers/styles/Voic/انت سايق زربه.ogg"
jpvois10 = "userbot/helpers/styles/Voic/اوني تشان.ogg"
jpvois11 = "userbot/helpers/styles/Voic/برافو عليك استادي.ogg"
jpvois12 = "userbot/helpers/styles/Voic/بلوك محترم.ogg"
jpvois13 = "userbot/helpers/styles/Voic/بووم في منتصف الجبهة.ogg"
jpvois14 = "userbot/helpers/styles/Voic/بيتش.ogg"
jpvois15 = "userbot/helpers/styles/Voic/تخوني ؟.ogg"
jpvois15 = "userbot/helpers/styles/Voic/تره متكدرلي.ogg"
jpvois17 = "userbot/helpers/styles/Voic/تعبان اوي.ogg"
jpvois18 = "userbot/helpers/styles/Voic/تكذب.ogg"
jpvois19 = "userbot/helpers/styles/Voic/حسبي الله.ogg"
jpvois20 = "userbot/helpers/styles/Voic/حشاش.ogg"
jpvois21 = "userbot/helpers/styles/Voic/حقير.ogg"
jpvois22 = "userbot/helpers/styles/Voic/خاص.ogg"
jpvois23 = "userbot/helpers/styles/Voic/خاله ما تنامون.ogg"
jpvois24 = "userbot/helpers/styles/Voic/خرب شرفي اذا ابقى بالعراق.ogg"
jpvois25 = "userbot/helpers/styles/Voic/دكات الوكت الاغبر.ogg"
jpvois26 = "userbot/helpers/styles/Voic/ررردح.ogg"
jpvois27 = "userbot/helpers/styles/Voic/سلامن عليكم.ogg"
jpvois28 = "userbot/helpers/styles/Voic/شعليك.ogg"
jpvois29 = "userbot/helpers/styles/Voic/شكد شفت ناس مدودة.ogg"
jpvois30 = "userbot/helpers/styles/Voic/شلون ،.ogg"
jpvois31 = "userbot/helpers/styles/Voic/صح لنوم.ogg"
jpvois32 = "userbot/helpers/styles/Voic/صمت.ogg"
jpvois33 = "userbot/helpers/styles/Voic/ضحكة مصطفى الحجي.ogg"
jpvois34 = "userbot/helpers/styles/Voic/طماطه.ogg"
jpvois35 = "userbot/helpers/styles/Voic/طيح الله حضك.ogg"
jpvois36 = "userbot/helpers/styles/Voic/فاك يوو.ogg"
jpvois37 = "userbot/helpers/styles/Voic/فرحان.ogg"
jpvois38 = "userbot/helpers/styles/Voic/لا تضل تضرط.ogg"
jpvois39 = "userbot/helpers/styles/Voic/لا تقتل المتعه يا مسلم.ogg"
jpvois40 = "userbot/helpers/styles/Voic/لا مستحيل.ogg"
jpvois41 = "userbot/helpers/styles/Voic/لا والله شو عصبي.ogg"
jpvois42 = "userbot/helpers/styles/Voic/لش.ogg"
jpvois43 = "userbot/helpers/styles/Voic/لك اني شعليه.ogg"
jpvois44 = "userbot/helpers/styles/Voic/ما اشرب.ogg"
jpvois45 = "userbot/helpers/styles/Voic/مع الاسف.ogg"
jpvois46 = "userbot/helpers/styles/Voic/مقتدى.ogg"
jpvois47 = "userbot/helpers/styles/Voic/من رخصتكم.ogg"
jpvois48 = "userbot/helpers/styles/Voic/منو انت.ogg"
jpvois49 = "userbot/helpers/styles/Voic/منورني.ogg"
jpvois50 = "userbot/helpers/styles/Voic/نتلاكه بالدور الثاني.ogg"

def get_locks(chat_id):
    try:
        return SESSION.query(Locks).get(str(chat_id))
    finally:
        SESSION.close()
