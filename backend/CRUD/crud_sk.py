import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
from backend.constants.tahapan import tahap_surat

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
def sk_create(request, judul, namaKegiatan, deskripsi, jenisSurat, link):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        print(user_data2)
        nama_birdep = user_data2['nama']
        idPermintaan = "sk-" + idBirdep + "-" + str(sk_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul,
            'nama_kegiatan': namaKegiatan,
            'deskripsi': deskripsi,
            'jenis_surat': jenisSurat,
            'link_docs': link,
            'tahapan': 0,
            'nama_tahapan': tahap_surat[0],
            'waktu_pengajuan': datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
        }
        db.collection('sk').document(idPermintaan).set(data)

        return idPermintaan
    except:
        return "terjadi error"
    return ""

def sk_read(id):
    try:
        data = db.collection('sk').document(id).get().to_dict()
        return data
    except:
        data = []
    return data

def sk_delete():
    return

def sk_update(request, id, num):
    try:
        db.collection('sk').document(id).update({
            "tahapan": num,
            "nama_tahapan": tahap_surat[num]
        })
        return ""
    except:
        return "terjadi error"

def sk_update_3(request, id, num, dokumen):
    try:
        db.collection('sk').document(id).update({
            "tahapan": num,
            "token_dokumen": dokumen,
            "nama_tahapan": tahap_surat[num]
        })
        return ""
    except:
        return "terjadi error"


# ---------------------
# Update data counter
# --------------------
def sk_updateCounter():
    data = db.collection('counter').document('sk').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("sk").set(data)

def sk_getCounter():
    data = db.collection('counter').document('sk').get().to_dict()
    num = data['length']
    sk_updateCounter()
    return num


# ---------------------
# Read list of requests
# --------------------
def sk_read_requests(idBirdep, tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('sk').where('idBirdep', '==', idBirdep).get()
        else:
            datas = db.collection('sk').where('idBirdep', '==', idBirdep).where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def sk_read_all(tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('sk').get()
        else:
            datas = db.collection('sk').where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def sk_read_all_line():
    try:
        data_dict = []
        datas = db.collection('sk').order_by('waktu_pengajuan').limit(10).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict