from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.misc import firebase_init

if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

fauth = firebase_init.firebaseInit().auth()
db = firestore.client()
ds = storage.bucket()

def uploadPhoto(request):
    print(2)
    if request.method == "POST" and request.FILES:
        file = request.FILES.get('file')
        file = file.file
        source = request.POST.get('source')

        print(file)
        id_firebase = request.POST.get("id_firebase")
        blob = ds.blob(source + id_firebase)
        metadata = {"firebaseStorageDownloadTokens": id_firebase}
        blob.metadata = metadata
        blob.upload_from_file(file)

        print(request.POST.get("id_firebase"))

        return JsonResponse('sesai', safe=False)
