from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.misc import firebase_init

if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

db = firestore.client()
ds = storage.bucket()

def getPhoto(id):
    blob = ds.blob(id)
    blob.make_public()
    return blob.public_url
