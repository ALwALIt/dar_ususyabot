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

jpvois1 = "userbot/helpers/styles/Voic/ابو عباس لو تاكل خره.ogg"
jpvois2 = "userbot/helpers/styles/Voic/استمر نحن معك.ogg"
jpvois3 = "userbot/helpers/styles/Voic/افحط بوجه.ogg"
jpvois4 = "userbot/helpers/styles/Voic/اكعد لا اسطرك سطره العباس.ogg"
jpvois5 = "userbot/helpers/styles/Voic/اللهم لا شماته.ogg"
jpvois6 = "userbot/helpers/styles/Voic/امرع دينه.ogg"
jpvois7 = "userbot/helpers/styles/Voic/امشي بربوك.ogg"
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
jpvois51 = "userbot/helpers/styles/Voic/نستودعكم الله.ogg"
jpvois52 = "userbot/helpers/styles/Voic/ها شنهي.ogg"
jpvois53 = "userbot/helpers/styles/Voic/ههاي الافكار حطها.ogg"
jpvois54 = "userbot/helpers/styles/Voic/وينهم.ogg"
jpvois55 = "userbot/helpers/styles/Voic/يموتون جهالي.ogg"
jpvois56 = "userbot/helpers/styles/Voic/اريد انام.ogg"
jpvois57 = "userbot/helpers/styles/Voic/افتحك فتح.ogg"
jpvois58 = "userbot/helpers/styles/Voic/اكل خره لدوخني.ogg"
jpvois59 = "userbot/helpers/styles/Voic/السيد شنهو السيد.ogg"
jpvois60 = "userbot/helpers/styles/Voic/زيج2.ogg"
jpvois61 = "userbot/helpers/styles/Voic/زيج لهارون.ogg"
jpvois62 = "userbot/helpers/styles/Voic/زيج الناصرية.ogg"
jpvois63 = "userbot/helpers/styles/Voic/راقبو اطفالكم.ogg"
jpvois64 = "userbot/helpers/styles/Voic/راح اموتن.ogg"
jpvois65 = "userbot/helpers/styles/Voic/ذس اس مضرطة.ogg"
jpvois66 = "userbot/helpers/styles/Voic/دروح سرسح منا.ogg"
jpvois67 = "userbot/helpers/styles/Voic/خويه ما دكوم بيه.ogg"
jpvois68 = "userbot/helpers/styles/Voic/خلصت تمسلت ديلة كافي انجب.ogg"
jpvois69 = "userbot/helpers/styles/Voic/بعدك تخاف.ogg"
jpvois70 = "userbot/helpers/styles/Voic/بسبوس.ogg"
jpvois71 = "userbot/helpers/styles/Voic/اني بتيتة كحبة.ogg"
jpvois72 = "userbot/helpers/styles/Voic/انعل ابوكم لابو اليلعب وياكم طوبة.ogg"
jpvois73 = "userbot/helpers/styles/Voic/انت شدخلك.ogg"
jpvois74 = "userbot/helpers/styles/Voic/انا ماشي بطلع.ogg"
jpvois75 = "userbot/helpers/styles/Voic/امداك وامده الخلفتك.ogg"
jpvois76 = "userbot/helpers/styles/Voic/امبيههههه.ogg"
jpvois77 = "userbot/helpers/styles/Voic/هدي بيبي.ogg"
jpvois78 = "userbot/helpers/styles/Voic/هاه صدك تحجي.ogg"
jpvois79 = "userbot/helpers/styles/Voic/مو كتلك رجعني.ogg"
jpvois80 = "userbot/helpers/styles/Voic/مامرجية منك هاية.ogg"
jpvois81 = "userbot/helpers/styles/Voic/ليش هيجي.ogg"
jpvois82 = "userbot/helpers/styles/Voic/كـــافـي.ogg"
jpvois83 = "userbot/helpers/styles/Voic/كس اخت السيد.ogg"
jpvois84 = "userbot/helpers/styles/Voic/شنو كواد ولك اني هنا.ogg"
jpvois85 = "userbot/helpers/styles/Voic/شجلبت.ogg"
jpvois86 = "userbot/helpers/styles/Voic/شبيك وجه الدبس.ogg"
jpvois87 = "userbot/helpers/styles/Voic/سييييي.ogg"
jpvois88 = "userbot/helpers/styles/Voic/زيجج1.ogg"
jpvois89 = "userbot/helpers/styles/Voic/يموتون جهالي.ogg"
jpvois90 = "userbot/helpers/styles/Voic/ياخي اسكت اسكت.ogg"
jpvois91 = "userbot/helpers/styles/Voic/وينهم.ogg"
jpvois92 = "userbot/helpers/styles/Voic/هيلو سامر وحود.ogg"
jpvois93 = "userbot/helpers/styles/Voic/هو.ogg"
jpvois94 = "userbot/helpers/styles/Voic/ههاي الافكار حطها.ogg"

def get_locks(chat_id):
    try:
        return SESSION.query(Locks).get(str(chat_id))
    finally:
        SESSION.close()
