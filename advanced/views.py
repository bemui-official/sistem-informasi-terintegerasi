import json
from django.shortcuts import render, redirect
from backend.CRUD.crud_ka import ka_create, ka_read, ka_update_0, ka_update_1, ka_update_2
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init, getPhoto
from backend.constants.admins import advanced_admin, advanced_admin2

# Initialize Firebase Database
fauth = firebase_init.firebaseInit().auth()


# ---------------------
# Form Request Advanced
# --------------------
def formKa(request):
    try:
        if (request.session['uid']):
            if (fauth.get_account_info(request.session['uid'])):
                return render(request, 'advanced/form_ka.html')
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")


def postFormKa(request):
    judul = request.POST.get("judul")
    nama_kegiatan = request.POST.get("nama_kegiatan")
    deskripsi = request.POST.get("deskripsi")
    bank = request.POST.get("bank")
    norek = request.POST.get("norek")
    anrek = request.POST.get("anrek")
    voucher = request.POST.get("link_voucher")
    nominal = request.POST.get("nominal")

    message = ka_create(request, judul, nama_kegiatan, deskripsi, bank, norek, anrek, voucher, nominal)
    if message != "terjadi error":
        return redirect("/advanced/detail/" + message)
    else:
        message = "Gagal Upload"
        return redirect('ka:formka')

# ---------------------
# Detail Advanced
# --------------------
def detail(request, id):
    # try:
    if (request.session['uid']):
        user_session = fauth.get_account_info(request.session['uid'])
        if (user_session):
            data_detail = ka_read(id)
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
                print(advanced_admin)
                return render(request, 'advanced/ka_details.html', {
                    'data': data_detail,
                    'user': user,
                    'admin': advanced_admin,
                    'id': id,
                    'voucher': voucher,
                    'transfer': transfer
                })
            else:
                return redirect("/user/logout")
    # except:
    #     return redirect("/user/signin")


# ---------------------
# Form Tahap 0 Advanced
# --------------------
def diterima(request):
    print('masuk')
    id_request = request.POST.get("id_request")
    ka_update_0(request, id_request, 1)
    return redirect('ka:detail', id=id_request)


def dibatalkan(request):
    id_request = request.POST.get("id_request")
    ka_update_0(request, id_request, -1)
    return redirect('ka:detail', id=id_request)


# ---------------------
# Form Tahap 1 Advanced
# --------------------
def form1(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if(user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = ka_read(id)
                if (user['birdeptim'] in advanced_admin2["tahap1"]):
                    if (data_detail["tahapan"] == 1):
                        return render(request, 'advanced/tahap1_form.html', {"id": id})
                    else:
                        return redirect("/advanced/detail/" + id)
                else:
                    return redirect("/advanced/detail/" + id)
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
            message = ka_update_1(request, id_request, diterima, voucher_meta)
            print(message)
            if message != "terjadi error":
                return redirect("/advanced/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/advanced/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/advanced/detail/" + id_request)
    except:
        return redirect("/")


# ---------------------
# Form Tahap 2 Advanced
# --------------------
def form2(request, id):
    try:
        if (request.session['uid']):
            print("masuk")
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = ka_read(id)
                if (user['birdeptim'] in advanced_admin2["tahap2"]):
                    if (data_detail["tahapan"] == 2):
                        return render(request, 'advanced/tahap2_form.html', {"id": id})
                    else:
                        return redirect("/advanced/detail/" + id)
                else:
                    return redirect("/advanced/detail/" + id)
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
            message = ka_update_2(request, id_request, bukti_meta)
            if message != "terjadi error":
                return redirect("/advanced/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/advanced/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/advanced/detail/" + id_request)
    except:
        return redirect("/")