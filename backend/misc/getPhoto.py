from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.misc import firebase_init

if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

firebase = firebase_init.firebaseInit()
fstorage = firebase.storage()
fauth = firebase_init.firebaseInit().auth()
db = firestore.client()
ds = storage.bucket()

def getPhoto(url):
    return fstorage.child(url).get_url(None)
