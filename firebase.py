
import firebase_admin
from firebase_admin import credentials


def connection():
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
