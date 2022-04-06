import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from uuid import uuid4

cred = credentials.Certificate("testing-key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket' : 'sit-bemui.appspot.com'
})
db = firestore.client()
ds = storage.bucket()

def user_create(idBirdep, email, password, asal, nama, total_pesanan, panggilan, permintaan) :
    try:
        user = auth.create_user(
            uid=idBirdep, email=email, email_verified=False, password=password)
        print('Sucessfully created new user: {0}'.format(user.uid))
    except auth.EmailAlreadyExistsError:
        message = 'The user with the provided email already exists'
        return message;
    except auth.UidAlreadyExistsError:
        message = 'The user with the provided username already exists'
        return message;
    data = {
        'id': idBirdep,
        'email': email,
        'nama': nama,
        'asal': asal,
        'total_pesanan': total_pesanan,
        'panggilan': panggilan,
        'permintaan' : permintaan
    }
    db.collection('users').document(idBirdep).set(data)
    return "";

def user_read(idBirdep):
    data = db.collection('users').document(idBirdep).get()
    print('Successfully fetched user data: {0}'.format(data))
    return data

def user_update_email(idBirdep, email):
    user = auth.update_user(
        idBirdep,
        email=email)

    print('Sucessfully updated user: {0}'.format(user.uid))

def user_update_password(idBirdep, password):
    user = auth.update_user(
        idBirdep,
        password=password)

    print('Sucessfully updated user: {0}'.format(user.uid))

def user_update_data(idBirdep, email, asal, nama, total_pesanan, panggilan):
    data = {
        'id': idBirdep,
        'email': email,
        'nama': nama,
        'asal': asal,
        'total_pesanan': total_pesanan,
        'panggilan': panggilan
    }
    db.collection('users').document(idBirdep).set(data)
    return data

def user_delete(idBirdep):
    auth.delete_user(idBirdep)
    print('Successfully deleted user')