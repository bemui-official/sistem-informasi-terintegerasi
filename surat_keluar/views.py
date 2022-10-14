import json

from django.http import Http404
from django.shortcuts import render, redirect
from backend.CRUD.crud_sk import sk_create, sk_read, sk_update, sk_update_2, sk_update_2_drive
from backend.CRUD.crud_user import user_read
from backend.constants.links import links_surat
from backend.constants.tahapan import tahap_surat_keluar
from backend.misc import firebase_init, getPhoto
from backend.constants.admins import suratkeluar_admin, suratkeluar_admin2

# Initialize Firebase Database
fauth = firebase_init


# ---------------------
# Form Request Surat Keluar
# --------------------
def formSk(request):
    try:
        if (request.session['uid']):
            if (fauth.get_account_info(request.session['uid'])):
                return render(request, 'form_sk.html', {
                    'links_surat': links_surat
                })
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
    insidental = request.POST.get("insidental")

    if (insidental == "True"):
        insidental = True
        bukti = request.POST.get("bukti")
    else:
        insidental = False
        bukti = ""

    message = sk_create(request, judul, nama_kegiatan, deskripsi, jenis_surat, link, insidental, bukti)
    print(message)
    if message != "terjadi error":
        return redirect("/surat_keluar/detail/" + message)
    else:
        return redirect("user:logout")


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
                if (user["id"] == data_detail["idBirdep"] or user['birdeptim'] in suratkeluar_admin2["admin"]):
                    # Get Dokumen Files
                    try:
                        url = getPhoto.getPhoto(data_detail["token_dokumen"][0])
                        dokumen = url
                    except:
                        dokumen = ""
                    return render(request, 'sk_details.html', {
                        'data': data_detail,
                        'user': user,
                        'admin': suratkeluar_admin,
                        'id': id,
                        'dokumen': dokumen,
                        'tahap': tahap_surat_keluar
                    })
                else:
                    raise Http404
        else:
            return redirect("/user/logout")
    else:
        return redirect("/user/signin")

# ---------------------
# Form Tahap 0,1,2 Surat Keluar
# --------------------
def diterima_1(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratkeluar_admin2["tahap1"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sk_update(request, id_request, 1)
                    return redirect('sk:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')


def diterima_3(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratkeluar_admin2["tahap3"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sk_update(request, id_request, 3)
                    return redirect('sk:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')

def ditolak_3(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratkeluar_admin2["tahap3"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sk_update(request, id_request, 0)
                    return redirect('sk:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')



# ---------------------
# Form Tahap 2 Surat Keluar
# --------------------
def form2(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = sk_read(id)
                if (user['birdeptim'] in suratkeluar_admin2["tahap2"]):
                    if (data_detail["tahapan"] == 1):
                        return render(request, 'tahap2_form.html', {"id": id})
                    else:
                        return redirect("/surat_keluar/detail/" + id)
                else:
                    return redirect("/surat_keluar/detail/" + id)
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except:
        return redirect("/")


def postForm2(request):
    dokumen = request.POST.get("uploadFiles")
    id_request = request.POST.get("id_request")
    drive_surat = request.POST.get("drive_surat")
    dokumen = json.loads(dokumen)
    print(dokumen)

    # Upload data to firebase
    try:
        if dokumen[0]["successful"]:
            print("masuk")
            dokumen_meta = []
            dokumen_meta.append(dokumen[0]["successful"][0]["meta"]["id_firebase"])
            message = sk_update_2(request, id_request, 2, dokumen_meta)
            print(message)
            if message != "terjadi error":
                return redirect("/surat_keluar/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/surat_keluar/detail/" + id_request)
        else:
            if drive_surat != "":
                message = sk_update_2_drive(request, id_request, 2, drive_surat)
                print(message)
                if message != "terjadi error":
                    return redirect("/surat_keluar/detail/" + id_request)
                else:
                    message = "Gagal Upload"
                    return redirect("/surat_keluar/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/surat_keluar/detail/" + id_request)
    except:
        return redirect("/")
