import firebase_admin
from firebase_admin import credentials, firestore, storage
from .crud_user import user_read
from backend.misc import firebase_init
from backend.constants.tahapan import tahap_advanced

import datetime
import pytz


# --------------------------
# Initialize Firebase Admin
# --------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("testing-key.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'sit-bemui.appspot.com'
    })

fauth = firebase_init
db = firestore.client()
ds = storage.bucket()


# --------------------------
# CRUD Functions
# --------------------------
def ka_create(request, judul, namaKegiatan, deskripsi, bank, norek, anrek, voucher, nominal):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        nama_birdep = user_data2['nama']
        idPermintaan = "ka-" + idBirdep + "-" + str(ka_getCounter())
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
            'nama_tahapan': tahap_advanced[0],
            'bukti_transaksi': [],
            'waktu_pengajuan': datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
        }
        db.collection('ka').document(idPermintaan).set(data)

        return idPermintaan
    except:
        return "terjadi error"

def ka_read(id):
    try:
        data = db.collection('ka').document(id).get().to_dict()
        return data
    except:
        data = []
    return data

def ka_delete():
    return

# ---------------------
# Update data per-tahap
# --------------------

def ka_update_0(request, id, num):
    try:
        db.collection('ka').document(id).update({
            "tahapan": num,
            "nama_tahapan": tahap_advanced[num]
        })
        return ""
    except:
        return "terjadi error"

def ka_update_1(request, id, diterima, voucher):
    try:
        db.collection('ka').document(id).update({
            "nominal_diterima": diterima,
            "token_voucher": voucher,
            "tahapan": 2,
            "nama_tahapan": tahap_advanced[2]
        })
        return ""
    except:
        return "terjadi error"

def ka_update_2(request, id, bukti):
    db.collection('ka').document(id).update({
        "bukti_transfer": bukti,
        "tahapan": 3,
        "nama_tahapan": tahap_advanced[3]
    })
    return ""


# ---------------------
# Update data counter
# --------------------

def ka_updateCounter():
    data = db.collection('counter').document('ka').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("ka").set(data)

def ka_getCounter():
    data = db.collection('counter').document('ka').get().to_dict()
    num = data['length']
    ka_updateCounter()
    return num


# ---------------------
# Read list of requests
# --------------------
def ka_read_requests(idBirdep, tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('ka').where('idBirdep', '==', idBirdep).get()
        else:
            datas = db.collection('ka').where('idBirdep', '==', idBirdep).where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def ka_read_all(tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('ka').get()
        else:
            datas = db.collection('ka').where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict