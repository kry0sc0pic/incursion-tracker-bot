import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("secrets/creds.json")
firebase_admin.initialize_app(cred)

db = firebase_admin.firestore.Client()