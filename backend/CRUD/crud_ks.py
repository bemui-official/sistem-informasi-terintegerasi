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

def ks_create(request, judul, nama_proker, namaKegiatan, deskripsi, voucher, nominal_setor, nominal_diterima, buktiPembayaran):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        print(user_data)
        idBirdep = user_data['users'][0]['localId']
        print(idBirdep)
        user_data2 = user_read(idBirdep)
        nama_birdep = user_data2['nama']
        idPermintaan = "ks-" + idBirdep + "-" + str(ks_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul,
            'nama_proker': nama_proker,
            'nama_kegiatan': namaKegiatan,
            'deskripsi': deskripsi,
            'link_voucher': voucher,
            'isTransfered': False,
            'nominal_setor': nominal_setor,
            'nominal_diterima': nominal_diterima,
            'tahapan': 0,
            'bukti_transaksi': [],
            'bukti_pembayaran': buktiPembayaran,
            'waktu_pengajuan': datetime.datetime.now()

        }
        db.collection('ks').document(idPermintaan).set(data)

        return ""
    except:
        return "terjadi error"

def ks_read():
    return

def ks_delete():
    return

def ks_update():
    return

def ks_updateCounter():
    data = db.collection('ks').document('counter').get().to_dict()
    data['length'] += 1
    db.collection('ks').document("counter").set(data)

def ks_getCounter():
    data = db.collection('ks').document('counter').get().to_dict()
    num = data['length']
    ks_updateCounter()
    return num
