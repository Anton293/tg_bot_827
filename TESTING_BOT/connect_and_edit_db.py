import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://sportnamefinish-default-rtdb.firebaseio.com"
})

ref = db.reference("/tg_bot_data_initialisation")


ref.update({
    "admin_command": True
})
print(str(ref.get()))
