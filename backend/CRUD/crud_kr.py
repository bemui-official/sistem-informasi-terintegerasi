import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
import datetime

# --------------------------
# Initialize Firebase Admin
# --------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

fauth = firebase_init.firebaseInit().auth()
db = firestore.client()
ds = storage.bucket()


# --------------------------
# CRUD Functions
# --------------------------
def kr_create(request, judul, namaKegiatan, deskripsi, norek, anrek, voucher, nominal, buktiPembayaran):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
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
            'bukti_pembayaran': buktiPembayaran,
            'waktu_pengajuan': datetime.datetime.now()
        }
        db.collection('kr').document(idPermintaan).set(data)

        return ""
    except:
        return "terjadi error"

def kr_read(id):
    try:
        data = db.collection('kr').document(id).get().to_dict()
        return data
    except:
        data = []
    return data

def kr_delete():
    return

def kr_update():
    return

def kr_update_1(request, id, diterima, voucher):
    db.collection('kr').document(id).update({
        "nominal_diterima": diterima,
        "token_voucher": voucher
    })
    return

def kr_update_2(request, id, bukti):
    db.collection('kr').document(id).update({
        "bukti_transfer": bukti,
    })
    return

def kr_updateCounter():
    data = db.collection('counter').document('kr').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("kr").set(data)

def kr_getCounter():
    data = db.collection('counter').document('kr').get().to_dict()
    num = data['length']
    kr_updateCounter()
    return num
