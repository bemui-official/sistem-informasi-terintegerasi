import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.crud_user import user_read
from backend import firebase_init
import datetime


if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

fauth = firebase_init.firebaseInit().auth()
db = firestore.client()
ds = storage.bucket()

def kr_create(request, judul, namaKegiatan, deskripsi, norek, anrek, voucher, nominal, ):
    #TODO: Buat metode input bukti transaksi
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        print(user_data2)
        nama_birdep = user_data2['nama']
        idPermintaan = "kr-" + idBirdep + "-" + str(kr_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul,
            'nama_kegiatan': namaKegiatan,
            'deskripsi': deskripsi,
            'nomor_rekening': norek,
            'AN_rekening': anrek,
            'link_voucher': voucher,
            'isTransfered': False,
            'total_nominal': nominal,
            'tahapan': 0,
            'bukti_transaksi': [],
            'waktu_pengajuan': datetime.datetime.now()

        }
        db.collection('kr').document(idPermintaan).set(data)
    except:
        return "terjadi error"
    return ""

def kr_read():
    return

def kr_delete():
    return

def kr_update():
    return

def kr_updateCounter():
    data = db.collection('kr').document('counter').get().to_dict()
    data['length'] += 1
    db.collection('kr').document("counter").set(data)

def kr_getCounter():
    data = db.collection('kr').document('counter').get().to_dict()
    num = data['length']
    kr_updateCounter()
    return num
