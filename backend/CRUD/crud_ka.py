import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
import datetime


if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

fauth = firebase_init.firebaseInit().auth()
db = firestore.client()
ds = storage.bucket()

def ka_create(request, judul, namaKegiatan, deskripsi, proker, tanggalAcara, norek, anrek, voucher, nominalDibutuhkan):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        print(user_data2)
        nama_birdep = user_data2['nama']
        idPermintaan = "ka-" + idBirdep + "-" + str(ka_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul,
            'nama_proker': proker,
            'nama_kegiatan': namaKegiatan,
            'deskripsi': deskripsi,
            'tanggal_acara': tanggalAcara,
            'nomor_rekening': norek,
            'AN_rekening': anrek,
            'link_voucher': voucher,
            'nominal_dibutuhkan': nominalDibutuhkan,
            'isTransfered': False,
            'tahapan': 0,
            'waktu_pengajuan': datetime.datetime.now()

        }
        db.collection('ka').document(idPermintaan).set(data)
    except:
        return "terjadi error"
    return ""

def ka_read():
    return

def ka_delete():
    return

def ka_update():
    return

def ka_updateCounter():
    data = db.collection('ka').document('counter').get().to_dict()
    data['length'] += 1
    db.collection('ka').document("counter").set(data)

def ka_getCounter():
    data = db.collection('ka').document('counter').get().to_dict()
    num = data['length']
    ka_updateCounter()
    return num
