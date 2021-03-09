# Initializing on google cloud platform
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate(
    "linkedin-bot/src/db/firebaseCreds/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
