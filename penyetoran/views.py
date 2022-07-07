import json
from django.shortcuts import render, redirect
from backend.CRUD.crud_ks import ks_create, ks_read, ks_update_0, ks_update_1, ks_update_2
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init, getPhoto
from backend.constants.admins import penyetoran_admin, penyetoran_admin2

# Initialize Firebase Database
fauth = firebase_init.firebaseInit().auth()


# ---------------------
# Form Request Penyetoran
# --------------------
def formKs(request):
    try:
        if (request.session['uid']):
            if (fauth.get_account_info(request.session['uid'])):
                return render(request, 'penyetoran/form_ks.html')
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")


def postFormKs(request):
    judul = request.POST.get("judul")
    nama_kegiatan = request.POST.get("nama_kegiatan")
    deskripsi = request.POST.get("deskripsi")
    bank = request.POST.get("bank")
    norek = request.POST.get("norek")
    anrek = request.POST.get("anrek")
    voucher = request.POST.get("link_voucher")
    nominal = request.POST.get("nominal")

    message = ks_create(request, judul, nama_kegiatan, deskripsi, bank, norek, anrek, voucher, nominal)
    if message != "terjadi error":
        return redirect("/penyetoran/detail/" + message)
    else:
        message = "Gagal Upload"
        return redirect('ks:formks')

# ---------------------
# Detail Penyetoran
# --------------------
def detail(request, id):
    # try:
    if (request.session['uid']):
        user_session = fauth.get_account_info(request.session['uid'])
        if (user_session):
            data_detail = ks_read(id)
            user = user_read(user_session['users'][0]['localId'])
            if (data_detail != []):
                # Get Voucher Files
                try:
                    url = getPhoto.getPhoto(data_detail["token_voucher"][0])
                    voucher = url
                except:
                    voucher = ""
                # Get Bukti Transfer
                try:
                    url = getPhoto.getPhoto(data_detail["bukti_transfer"][0])
                    transfer = url
                except:
                    transfer = ""
                print(data_detail)
                print(penyetoran_admin)
                return render(request, 'penyetoran/ks_details.html', {
                    'data': data_detail,
                    'user': user,
                    'admin': penyetoran_admin,
                    'id': id,
                    'voucher': voucher,
                    'transfer': transfer
                })
            else:
                return redirect("/user/logout")
    # except:
    #     return redirect("/user/signin")


# ---------------------
# Form Tahap 0 Penyetoran
# --------------------
def diterima(request):
    print('masuk')
    id_request = request.POST.get("id_request")
    ks_update_0(request, id_request, 1)
    return redirect('ks:detail', id=id_request)


def diterima2(request):
    print('masuk')
    id_request = request.POST.get("id_request")
    ks_update_0(request, id_request, 4)
    return redirect('ks:detail', id=id_request)


def dibatalkan(request):
    id_request = request.POST.get("id_request")
    ks_update_0(request, id_request, -1)
    return redirect('ks:detail', id=id_request)


# ---------------------
# Form Tahap 1 Penyetoran
# --------------------
def form1(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if(user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = ks_read(id)
                if (user['birdeptim'] in penyetoran_admin2["tahap1"]):
                    if (data_detail["tahapan"] == 1):
                        return render(request, 'penyetoran/tahap1_form.html', {"id": id})
                    else:
                        return redirect("/penyetoran/detail/" + id)
                else:
                    return redirect("/penyetoran/detail/" + id)
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except:
        return redirect("/")


def postForm1(request):
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
            message = ks_update_1(request, id_request, voucher_meta)
            print(message)
            if message != "terjadi error":
                return redirect("/penyetoran/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/penyetoran/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/penyetoran/detail/" + id_request)
    except:
        return redirect("/")


# ---------------------
# Form Tahap 2 Penyetoran
# --------------------
def form2(request, id):
    try:
        if (request.session['uid']):
            print("masuk")
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                data_detail = ks_read(id)
                if (data_detail["tahapan"] == 2):
                    return render(request, 'penyetoran/tahap2_form.html', {"id": id})
                else:
                    return redirect("/penyetoran/detail/" + id)
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
            message = ks_update_2(request, id_request, bukti_meta)
            if message != "terjadi error":
                return redirect("/penyetoran/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/penyetoran/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/penyetoran/detail/" + id_request)
    except:
        return redirect("/")