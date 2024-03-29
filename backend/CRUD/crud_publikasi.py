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
        nama_birdep = user_data2['nama']
        if(idBirdep.endswith('-bem_ui')):
            useBirdep = idBirdep[:-7]
        else:
            useBirdep = idBirdep
        idPermintaan = "publikasi-" + useBirdep + "-" + str(publikasi_getCounter())
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
            "design_link": "",
            "preview_link_instagram": "",
            "preview_link_twitter": "",
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
        query = db.collection('publikasi').get()
        matching_documents = [doc for doc in query if doc.get('idPermintaan').lower() == id.lower()]
        list_publikasi = []
        for document in matching_documents:
            list_publikasi.append(document.get("idPermintaan"))

        data = db.collection('publikasi').document(list_publikasi.pop()).get().to_dict()

        return data
    except:
        list_publikasi = []
    return list_publikasi

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

def publikasi_update(request, id, num, design_link = "", preview_link_instagram = "", preview_link_twitter = ""):
    try:
        if(num == 2):
            if(design_link != ""):
                db.collection('publikasi').document(id).update({
                    "tahapan": num,
                    "nama_tahapan": tahap_publikasi[num],
                    "design_link": design_link
                })
            else:
                db.collection('publikasi').document(id).update({
                    "tahapan": num,
                    "nama_tahapan": tahap_publikasi[num]
                })
        elif(num == 4):
            if(preview_link_instagram != "" and preview_link_twitter != ""):
                db.collection('publikasi').document(id).update({
                    "tahapan": num,
                    "nama_tahapan": tahap_publikasi[num],
                    "preview_link_instagram": preview_link_instagram,
                    "preview_link_twitter": preview_link_twitter
                })
            elif(preview_link_instagram != ""):
                db.collection('publikasi').document(id).update({
                    "tahapan": num,
                    "nama_tahapan": tahap_publikasi[num],
                    "preview_link_instagram": preview_link_instagram,
                })
            elif(preview_link_twitter != ""):
                db.collection('publikasi').document(id).update({
                    "tahapan": num,
                    "nama_tahapan": tahap_publikasi[num],
                    "preview_link_twitter": preview_link_twitter
                })
            else:
                db.collection('publikasi').document(id).update({
                    "tahapan": num,
                    "nama_tahapan": tahap_publikasi[num]
                })
        else:
            db.collection('publikasi').document(id).update({
                "tahapan": num,
                "nama_tahapan": tahap_publikasi[num]
            })
        return ""
    except:
        return "terjadi error"

def publikasi_tolak(request, id, tahapan: int):
    try:
        if(tahapan != 0):
            if(tahapan == 3):
                db.collection('publikasi').document(id).update({
                    "tahapan": tahapan - 2,
                    "nama_tahapan": tahap_publikasi[tahapan - 2]
                })
            else:
                db.collection('publikasi').document(id).update({
                    "tahapan": tahapan - 1,
                    "nama_tahapan": tahap_publikasi[tahapan - 1]
                })
        return ""
    except:
        return "terjadi error"

def publikasi_edit(request, id, judul_konten, date_posted, time_posted, is_insidental, publikasi, notes, bukti_insidental, channels):
    try:
        db.collection('publikasi').document(id).update({
            'judul': judul_konten,
            'date_posted': date_posted,
            'time_posted': time_posted,
            'is_insidental': is_insidental,
            'publikasi': publikasi,
            'notes': notes,
            'bukti_insidental': bukti_insidental,
            'channels': channels
        })
        return ""
    except:
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

def sort_key(item):
    date_posted = datetime.datetime.strptime(item['date_posted'], '%Y-%m-%d')
    time_posted = datetime.datetime.strptime(item['time_posted'], '%H:%M')
    return (date_posted, time_posted)

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
            
        sorted_data = sorted(data_dict, key=sort_key)
        
        return sorted_data
    except Exception as e:
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

def publikasi_notification(notInTahapan):
    today = datetime.datetime.now()
    try:
        data_dict = []
        datas = db.collection('publikasi').get()
        
        for data in datas:
            data_dict.append(data.to_dict())
            
        sorted_data = sorted(data_dict, key=sort_key)
        
        filtered_data = []
        for data in sorted_data:
            date_posted = datetime.datetime.strptime(data['date_posted'], '%Y-%m-%d')
            time_posted = datetime.datetime.strptime(data['time_posted'], '%H:%M')
            item_datetime = datetime.datetime.combine(date_posted.date(), time_posted.time())
            
            if item_datetime >= today and data['tahapan'] not in notInTahapan:
                filtered_data.append(data)
        
        return filtered_data[:10]
    except Exception as e:
        print(e)
        data_dict = []
        return data_dict

def get_publikasi_from_user(user):
    documents = db.collection('publikasi').where('idBirdep', '==', user).get()
    publikasi = []
    
    for document in documents:
        if(document.get("tahapan") != 4):
            publikasi.append(document.to_dict())

    return publikasi

def checkIfUnique(date_posted, time_posted):
    today = datetime.datetime.now()
    try:
        date_posted_temp = datetime.datetime.strptime(date_posted, '%Y-%m-%d')
        time_posted_temp = datetime.datetime.strptime(time_posted, '%H:%M')
        item_datetime = datetime.datetime.combine(date_posted_temp.date(), time_posted_temp.time())
        
        if item_datetime < today:
            return False
        
        encountered_date_times = set()

        datas = db.collection('publikasi').get()
        for data in datas:
            data_dict = data.to_dict()    
            encountered_date_times.add((data_dict['date_posted'], data_dict['time_posted']))
                    
        if (date_posted, time_posted) in encountered_date_times:
            return False
        
        return True
        
    except Exception as e:
        print(e)
        
    return False