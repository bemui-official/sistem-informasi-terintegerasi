import firebase_admin
from firebase_admin import credentials, firestore, storage
from .crud_user import user_read
from ..constants.tahapan import tahap_reimbursement

from backend.misc import firebase_init
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
def kr_create(request, judul, namaKegiatan, deskripsi, bank, norek, anrek, voucher, nominal, buktiPembayaran):
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
            'bank': bank,
            'nomor_rekening': norek,
            'AN_rekening': anrek,
            'link_voucher': voucher,
            'isTransfered': False,
            'total_nominal': nominal,
            'tahapan': 0,
            'nama_tahapan': tahap_reimbursement[0],
            'bukti_transaksi': [],
            'bukti_pembayaran': buktiPembayaran,
            'waktu_pengajuan': datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
        }
        db.collection('kr').document(idPermintaan).set(data)

        return idPermintaan
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

# ---------------------
# Update data per-tahap
# --------------------

def kr_update_0(request, id, num):
    try:
        db.collection('kr').document(id).update({
            "tahapan": num,
            "nama_tahapan": tahap_reimbursement[num]
        })
        return ""
    except:
        return "terjadi error"

def kr_update_1(request, id, diterima, voucher):
    try:
        db.collection('kr').document(id).update({
            "nominal_diterima": diterima,
            "token_voucher": voucher,
            "tahapan": 2,
            "nama_tahapan": tahap_reimbursement[2]
        })
        return ""
    except:
        return "terjadi error"

def kr_update_2(request, id, bukti):
    db.collection('kr').document(id).update({
        "bukti_transfer": bukti,
        "tahapan": 3,
        "nama_tahapan": tahap_reimbursement[3],
    })
    return ""


# ---------------------
# Update data counter
# --------------------

def kr_updateCounter():
    data = db.collection('counter').document('kr').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("kr").set(data)

def kr_getCounter():
    data = db.collection('counter').document('kr').get().to_dict()
    num = data['length']
    kr_updateCounter()
    return num


# ---------------------
# Read list of requests
# --------------------
def kr_read_requests(idBirdep, tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('kr').where('idBirdep', '==', idBirdep).limit(10).get()
        else:
            datas = db.collection('kr').where('idBirdep', '==', idBirdep).where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def kr_read_all(tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('kr').limit(10).get()
        else:
            datas = db.collection('kr').where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def kr_read_all_line():
    try:
        data_dict = []
        datas = db.collection('kr').order_by('waktu_pengajuan').limit(10).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict