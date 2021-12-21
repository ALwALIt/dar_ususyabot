from pyrogram import Client,errors,filters
import random
app = Client("Pyrothon",api_id=12345,api_hash="ASfdasf")


@app.on_message(filters.me,filters.text)
def d(clinet,message):
    msg = message.text
    if msg == "فحص يوزرات":
        dod = 0
        errors1 = 0
        while True:
            user = 'QWERTYUIOPASDFGHJKLZXCVNBM'
            us = str("".join(random.choice(user) for i in range(1)))
            us2 = str("".join(random.choice(user) for i in range(1)))
            username = us + 'nasdasdnn' + us2
            try:
                app.send_message(f"{username}","test")
                errors1 += 1
            except errors.exceptions.bad_request_400.UsernameNotOccupied:
                dod += 1
                app.send_message("me",f"{username}")
            print(f"Results : Done {dod} : did : {errors1}")
app.run()