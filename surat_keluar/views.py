import json

from django.shortcuts import render, redirect
from backend.CRUD.crud_sk import sk_create, sk_read, sk_update, sk_update_3
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
from backend.constants.admins import suratkeluar_admin, suratkeluar_admin2

# Initialize Firebase Database
fauth = firebase_init.firebaseInit().auth()


# ---------------------
# Form Request Surat Keluar
# --------------------
def formSk(request):
    try:
        if (request.session['uid']):
            if (fauth.get_account_info(request.session['uid'])):
                return render(request, 'form_sk.html')
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")


def postFormSk(request):
    judul = request.POST.get("judul")
    nama_kegiatan = request.POST.get("nama_kegiatan")
    deskripsi = request.POST.get("deskripsi")
    jenis_surat = request.POST.get("jenis")
    link = request.POST.get("linkdocs")

    message = sk_create(request, judul, nama_kegiatan, deskripsi, jenis_surat, link)
    print(message)
    if message == "":
        return redirect("/")
    else:
        return redirect(formSk)


# ---------------------
# Detail Surat Keluar
# --------------------
def detail(request, id):
    if (request.session['uid']):
        user_session = fauth.get_account_info(request.session['uid'])
        if (user_session):
            data_detail = sk_read(id)
            user = user_read(user_session['users'][0]['localId'])
            if (data_detail != []):
                return render(request, 'sk_details.html', {
                    'data': data_detail,
                    'user': user,
                    'admin': suratkeluar_admin,
                    'id': id,
                })
        else:
            return redirect("/user/logout")


# ---------------------
# Form Tahap 0,1,2 Surat Keluar
# --------------------
def diterima_1(request):
    print('masuk')
    id_request = request.POST.get("id_request")
    sk_update(request, id_request, 1)
    return redirect('detail', id=id_request)


def diterima_2(request):
    print('masuk')
    id_request = request.POST.get("id_request")
    sk_update(request, id_request, 2)
    return redirect('detail', id=id_request)


def dibatalkan(request):
    id_request = request.POST.get("id_request")
    sk_update(request, id_request, -1)
    return redirect('detail', id=id_request)


# ---------------------
# Form Tahap 3 Surat Keluar
# --------------------
def form3(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = sk_read(id)
                if (user['birdeptim'] in suratkeluar_admin2["tahap3"]):
                    if (data_detail["tahapan"] == 1):
                        return render(request, 'tahap3_form.html', {"id": id})
                    else:
                        return redirect("/suratkeluar/detail/" + id)
                else:
                    return redirect("/suratkeluar/detail/" + id)
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except:
        return redirect("/")


def postForm3(request):
    dokumen = request.POST.get("uploadFiles")
    id_request = request.POST.get("id_request")
    dokumen = json.loads(dokumen)
    print(dokumen)

    # Upload data to firebase
    try:
        if dokumen[0]["successful"]:
            print("masuk")
            dokumen_meta = []
            dokumen_meta.append(dokumen[0]["successful"][0]["meta"]["id_firebase"])
            message = sk_update_3(request, id_request, 3, dokumen_meta)
            print(message)
            if message != "terjadi error":
                return redirect("/suratkeluar/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/suratkeluar/detail/" + id_request)
        else:
            message = "Gagal Upload"
            return redirect("/suratkeluar/detail/" + id_request)
    except:
        return redirect("/")
