import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
from backend.constants.tahapan import tahap_surat_besar

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
def sb_create(request, judul, namaKegiatan, deskripsi, jenisSurat, link, insidental, bukti):
    try:
        print(request.session['uid'])
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        print(user_data2)
        nama_birdep = user_data2['nama']
        idPermintaan = "sb-" + idBirdep + "-" + str(sb_getCounter())
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
            'nama_tahapan': tahap_surat_besar[0],
            'waktu_pengajuan': datetime.datetime.now(pytz.timezone('Asia/Jakarta')),
            'isInsidental': insidental,
            'buktiInsidental': bukti
        }
        db.collection('sb').document(idPermintaan).set(data)

        return idPermintaan
    except:
        return "terjadi error"
    return ""

def sb_read(id):
    try:
        data = db.collection('sb').document(id).get().to_dict()
        return data
    except:
        data = []
    return data

def sb_delete():
    return

def sb_update(request, id, num):
    try:
        db.collection('sb').document(id).update({
            "tahapan": num,
            "nama_tahapan": tahap_surat_besar[num]
        })
        return ""
    except:
        return "terjadi error"

def sb_update_4(request, id, num, dokumen):
    try:
        db.collection('sb').document(id).update({
            "tahapan": num,
            "token_dokumen": dokumen,
            "nama_tahapan": tahap_surat_besar[num]
        })
        return ""
    except:
        return "terjadi error"

def sb_update_4_drive(request, id, num, drive_surat):
    try:
        db.collection('sb').document(id).update({
            "tahapan": num,
            "drive_surat": drive_surat,
            "nama_tahapan": tahap_surat_besar[num]
        })
        return ""
    except:
        return "terjadi error"


# ---------------------
# Update data counter
# --------------------
def sb_updateCounter():
    data = db.collection('counter').document('sb').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("sb").set(data)

def sb_getCounter():
    data = db.collection('counter').document('sb').get().to_dict()
    num = data['length']
    sb_updateCounter()
    return num


# ---------------------
# Read list of requests
# --------------------
def sb_read_requests(idBirdep, tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('sb').where('idBirdep', '==', idBirdep).get()
        else:
            datas = db.collection('sb').where('idBirdep', '==', idBirdep).where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def sb_read_all(tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('sb').get()
        else:
            datas = db.collection('sb').where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def sb_read_all_line():
    try:
        data_dict = []
        datas = db.collection('sb').order_by('waktu_pengajuan').limit(10).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict