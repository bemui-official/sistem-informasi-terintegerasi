import json
from django.shortcuts import render, redirect
from backend.CRUD.crud_kr import kr_create, kr_read, kr_update_0, kr_update_1, kr_update_2
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init, getPhoto
from backend.constants.admins import reimbursement_admin, reimbursement_admin2

# Initialize Firebase Database
fauth = firebase_init.firebaseInit().auth()


# ---------------------
# Form Request Reimbursement
# --------------------
def formKr(request):
    try:
        if (request.session['uid']):
            if (fauth.get_account_info(request.session['uid'])):
                return render(request, 'form_kr.html')
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")


def postFormKr(request):
    judul = request.POST.get("judul")
    nama_kegiatan = request.POST.get("nama_kegiatan")
    deskripsi = request.POST.get("deskripsi")
    norek = request.POST.get("norek")
    anrek = request.POST.get("anrek")
    voucher = request.POST.get("link_voucher")
    nominal = request.POST.get("nominal")
    photos = request.POST.get("uploadFiles")
    photos = json.loads(photos)
    print(photos)

    # Upload data to firebase
    if photos[0]["successful"]:
        photos_meta = []
        for i in photos[0]["successful"]:
            photos_meta.append(i["meta"]["id_firebase"])
        message = kr_create(request, judul, nama_kegiatan, deskripsi, norek, anrek, voucher, nominal, photos_meta)
        if message != "terjadi error":
            return redirect("/reimbursement/detail/" + message)
        else:
            message = "Gagal Upload"
            return redirect('kr:formkr')
    else:
        message = "Gagal Upload"
        return redirect('kr:formkr')


# ---------------------
# Detail Reimbursement
# --------------------
def detail(request, id):
    # try:
    if (request.session['uid']):
        user_session = fauth.get_account_info(request.session['uid'])
        if (user_session):
            data_detail = kr_read(id)
            user = user_read(user_session['users'][0]['localId'])
            if (data_detail != []):
                data_photo = []
                for photo in data_detail["bukti_pembayaran"]:
                    url = getPhoto.getPhoto(photo)
                    data_photo.append(url)
                try:
                    url = getPhoto.getPhoto(data_detail["token_voucher"][0])
                    voucher = url
                except:
                    voucher = ""
                print(data_detail)
                print(reimbursement_admin)
                print(data_photo)
                return render(request, 'kr_details.html', {
                    'data': data_detail,
                    'user': user,
                    'admin': reimbursement_admin,
                    'id': id,
                    'photos': data_photo,
                    'voucher': voucher
                })
            else:
                return redirect("/user/logout")
    # except:
    #     return redirect("/user/signin")


# ---------------------
# Form Tahap 0 Reimbursement
# --------------------
def diterima(request):
    print('masuk')
    id_request = request.POST.get("id_request")
    kr_update_0(request, id_request, 1)
    return redirect('kr:detail', id=id_request)


def dibatalkan(request):
    id_request = request.POST.get("id_request")
    kr_update_0(request, id_request, -1)
    return redirect('kr:detail', id=id_request)


# ---------------------
# Form Tahap 1 Reimbursement
# --------------------
def form1(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if(user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = kr_read(id)
                if (user['birdeptim'] in reimbursement_admin2["tahap1"]):
                    if (data_detail["tahapan"] == 1):
                        return render(request, 'tahap1_form.html', {"id": id})
                    else:
                        return redirect("/reimbursement/detail/" + id)
                else:
                    return redirect("/reimbursement/detail/" + id)
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except:
        return redirect("/")


def postForm1(request):
    diterima = request.POST.get("diterima")
    voucher = request.POST.get("uploadFiles")
    id_request = request.POST.get("id_request")
    voucher = json.loads(voucher)
    print(voucher)

    # Upload data to firebase
    try:
        if voucher[0]["successful"] :
            print("masuk")
            voucher_meta = []
            voucher_meta.append(voucher[0]["successful"][0]["meta"]["id_firebase"])
            message = kr_update_1(request, id_request, diterima, voucher_meta)
            print(message)
            if message != "terjadi error":
                return redirect("/reimbursement/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/reimbursement/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/reimbursement/detail/" + id_request)
    except:
        return redirect("/")


# ---------------------
# Form Tahap 2 Reimbursement
# --------------------
def form2(request, id):
    try:
        if (request.session['uid']):
            print("masuk")
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = kr_read(id)
                if (user['birdeptim'] in reimbursement_admin2["tahap2"]):
                    if (data_detail["tahapan"] == 2):
                        return render(request, 'tahap2_form.html', {"id": id})
                    else:
                        return redirect("/reimbursement/detail/" + id)
                else:
                    return redirect("/reimbursement/detail/" + id)
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except:
        return redirect("/")


def postForm2(request):
    bukti = request.POST.get("uploadFiles")
    id_request = request.POST.get("id_request")
    bukti = json.loads(bukti)
    print(bukti)

    # Upload data to firebase
    try:
        if bukti[0]["successful"]:
            bukti_meta = []
            bukti_meta.append(bukti[0]["successful"][0]["meta"]["id_firebase"])
            message = kr_update_2(request, id_request, bukti_meta)
            if message != "terjadi error":
                return redirect("/reimbursement/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/reimbursement/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/reimbursement/detail/" + id_request)
    except:
        return redirect("/")