
import firebase_admin
from firebase_admin import credentials, firestore, storage
from uuid import uuid4

cred = credentials.Certificate("testing-key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket' : 'sit-bemui.appspot.com'
})
db = firestore.client()
ds = storage.bucket()

