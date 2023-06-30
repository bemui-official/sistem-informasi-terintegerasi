import firebase_admin
from firebase_admin import credentials, firestore, storage
from .crud_user import user_read
from backend.misc import firebase_init
from backend.constants.tahapan import tahap_publikasi

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
def publikasi_create(request, judul_konten, date_posted, time_posted, is_insidental, publikasi, notes, bukti_insidental, channels):
    try:
        user_data = fauth.get_account_info(request.session['uid'])
        idBirdep = user_data['users'][0]['localId']
        user_data2 = user_read(idBirdep)
        print(user_data2)
        nama_birdep = user_data2['nama']
        idPermintaan = "publikasi-" + idBirdep + "-" + str(publikasi_getCounter())
        data = {
            'idPermintaan': idPermintaan,
            'idBirdep': idBirdep,
            'nama_birdep': nama_birdep,
            'judul': judul_konten,
            'date_posted': date_posted,
            'time_posted': time_posted,
            'is_insidental': is_insidental,
            'publikasi': publikasi,
            'notes': notes,
            'bukti_insidental': bukti_insidental,
            'tahapan': 0,
            'nama_tahapan': tahap_publikasi[0],
            'waktu_pengajuan': datetime.datetime.now(pytz.timezone('Asia/Jakarta')),
            'waktu_pengajuan_str': datetime.datetime.strftime(datetime.datetime.now(pytz.timezone('Asia/Jakarta')), "%d %b %Y, %H:%M"),
            'channels': channels
        }
        
        db.collection('publikasi').document(idPermintaan).set(data)

        return idPermintaan
    except Exception as e:
        print(e)
        return "terjadi error"

def publikasi_read(id):
    try:
        data = db.collection('publikasi').document(id).get().to_dict()
        return data
    except:
        data = []
    return data

def publikasi_delete(id):
    try:
        print("test")
        data = db.collection('publikasi').document(id).delete()
        return data
    except:
        return

def publikasi_add_to_notes(id, note, writer):
    try:
        data = db.collection('publikasi').document(id).get().to_dict()
        
        current_notes = data['notes']
        
        note = {
            "type": "komen",
            "time_stamp": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            "note": note,
            "writer": writer
        }

        current_notes.append(note)
        
        db.collection('publikasi').document(id).update({
            "notes": current_notes
        })
        
        return id
    except Exception as e:
        print(e) 
        return "terjadi error"
# ---------------------
# Update data counter
# --------------------
def publikasi_updateCounter():
    data = db.collection('counter').document('publikasi').get().to_dict()
    data['length'] += 1
    db.collection('counter').document("publikasi").set(data)
    
def publikasi_getCounter():
    data = db.collection('counter').document('publikasi').get().to_dict()
    num = data['length']
    publikasi_updateCounter()
    return num

# ---------------------
# Read list of requests
# --------------------
def publikasi_read_requests(idBirdep, tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('publikasi').where('idBirdep', '==', idBirdep).limit(10).get()
        else:
            datas = db.collection('publikasi').where('idBirdep', '==', idBirdep).where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def publikasi_read_all(tahap):
    try:
        data_dict = []
        if tahap == 'semua':
            datas = db.collection('publikasi').get()
        else:
            datas = db.collection('publikasi').where('tahapan', '==', int(tahap)).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict

def publikasi_read_all_line():
    try:
        data_dict = []
        datas = db.collection('publikasi').order_by('waktu_pengajuan').limit(10).get()
        for data in datas:
            data_dict.append(data.to_dict())
        return data_dict
    except:
        data_dict = []
    return data_dict