import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
import datetime
import pytz


if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

fauth = firebase_init
db = firestore.client()
ds = storage.bucket()

def sd_create(request, judul, nama_proker, nama_kegiatan, deskripsi, jenis_surat, surat_permintaan):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        print(user_data)
        idBirdep = user_data['users'][0]['localId']
        print(idBirdep)
        user_data2 = user_read(idBirdep)
        nama_birdep = user_data2['nama']
        idPermintaan = "sd-" + idBirdep + "-" + str(sd_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul,
            'nama_proker': nama_proker,
            'nama_kegiatan': nama_kegiatan,
            'deskripsi': deskripsi,
            'jenis_surat': jenis_surat,
            'surat_permintaan': surat_permintaan,
            'isTransfered': False,
            'tahapan': 0,
            'waktu_pengajuan': datetime.datetime.now(pytz.timezone('Asia/Jakarta')),
            'waktu_pengajuan_str': datetime.datetime.strftime(datetime.datetime.now(pytz.timezone('Asia/Jakarta')),
                                                              "%d %b %Y, %H:%M")

        }
        db.collection('sd').document(idPermintaan).set(data)

        return ""
    except:
        return "terjadi error"

def sd_read():
    return

def sd_delete():
    return

def sd_update():
    return

def sd_updateCounter():
    data = db.collection('sd').document('counter').get().to_dict()
    data['length'] += 1
    db.collection('sd').document("counter").set(data)

def sd_getCounter():
    data = db.collection('sd').document('counter').get().to_dict()
    num = data['length']
    sd_updateCounter()
    return num
