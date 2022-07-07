import firebase_admin
from firebase_admin import credentials, firestore, storage
from .crud_user import user_read

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
def ks_create(request, judul, namaKegiatan, deskripsi, bank, norek, anrek, voucher, nominal):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        nama_birdep = user_data2['nama']
        idPermintaan = "ks-" + idBirdep + "-" + str(ks_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul,
            'nama_kegiatan': namaKegiatan,
            'deskripsi': deskripsi,
            'bank': bank,
            'nomor_rekening': norek,
            'AN_rekening': anrek,
            'link_voucher': voucher,
            'isTransfered': False,
            'total_nominal': nominal,
            'tahapan': 0,
            'bukti_transaksi': [],
            'waktu_pengajuan': datetime.datetime.now()
        }
        db.collection('ks').document(idPermintaan).set(data)

        return idPermintaan
    except:
        return "terjadi error"

def ks_read(id):
    try:
        data = db.collection('ks').document(id).get().to_dict()
        return data
    except:
        data = []
    return data

def ks_delete():
    return

# ---------------------
# Update data per-tahap
# --------------------

def ks_update_0(request, id, num):
    try:
        db.collection('ks').document(id).update({
            "tahapan": num
        })
        return ""
    except:
        return "terjadi error"

def ks_update_1(request, id, voucher):
    try:
        db.collection('ks').document(id).update({
            "token_voucher": voucher,
            "tahapan": 2
        })
        return ""
    except:
        return "terjadi error"

def ks_update_2(request, id, bukti):
    db.collection('ks').document(id).update({
        "bukti_transfer": bukti,
        "tahapan": 3
    })
    return ""


# ---------------------
# Update data counter
# --------------------

def ks_updateCounter():
    data = db.collection('counter').document('ks').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("ks").set(data)

def ks_getCounter():
    data = db.collection('counter').document('ks').get().to_dict()
    num = data['length']
    ks_updateCounter()
    return num


# ---------------------
# Read list of requests
# --------------------
def ks_read_requests(idBirdep):
    try:
        data_dict = []
        datas = db.collection('ks').where('idBirdep', '==', idBirdep).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def ks_read_all():
    try:
        data_dict = []
        datas = db.collection('ks').get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict