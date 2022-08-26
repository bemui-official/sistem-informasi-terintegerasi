import json

from django.http import Http404
from django.shortcuts import render, redirect
from backend.CRUD.crud_sb import sb_create, sb_read, sb_update, sb_update_4, sb_update_4_drive
from backend.CRUD.crud_user import user_read
from backend.constants.links import links_surat_besar
from backend.constants.tahapan import tahap_surat_besar
from backend.misc import firebase_init, getPhoto
from backend.constants.admins import suratbesar_admin, suratbesar_admin2

# Initialize Firebase Database
fauth = firebase_init


# ---------------------
# Form Request Surat Besar
# --------------------
def formSb(request):
    try:
        if (request.session['uid']):
            if (fauth.get_account_info(request.session['uid'])):
                return render(request, 'surat_besar/form_sb.html', {
                    'links_surat': links_surat_besar
                })
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")


def postFormSb(request):
    judul = request.POST.get("judul")
    nama_kegiatan = request.POST.get("nama_kegiatan")
    deskripsi = request.POST.get("deskripsi")
    jenis_surat = request.POST.get("jenis")
    link = request.POST.get("linkdocs")

    message = sb_create(request, judul, nama_kegiatan, deskripsi, jenis_surat, link)
    print(message)
    if message != "terjadi error":
        return redirect("/surat_besar/detail/" + message)
    else:
        return redirect("sb:formsb")


# ---------------------
# Detail Surat Besar
# --------------------
def detail(request, id):
    # try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                data_detail = sb_read(id)
                user = user_read(user_session['users'][0]['localId'])
                if (data_detail != []):
                    if (user["id"] == data_detail["idBirdep"] or user['birdeptim'] in suratbesar_admin2["admin"]):
                        # Get Dokumen Files
                        try:
                            url = getPhoto.getPhoto(data_detail["token_dokumen"][0])
                            dokumen = url
                        except:
                            dokumen = ""
                        return render(request, 'surat_besar/sb_details.html', {
                            'data': data_detail,
                            'user': user,
                            'admin': suratbesar_admin,
                            'id': id,
                            'dokumen': dokumen,
                            'tahap': tahap_surat_besar
                        })
                    else:
                        raise Http404
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    # except:
    #     return redirect("/user/signin")

# ---------------------
# Form Tahap 0,1,2 Surat Besar
# --------------------
def diterima_1(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratbesar_admin2["tahap1"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sb_update(request, id_request, 1)
                    return redirect('sb:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')

def diterima_2(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratbesar_admin2["tahap2"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sb_update(request, id_request, 2)
                    return redirect('sb:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')


def diterima_4(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratbesar_admin2["tahap4"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sb_update(request, id_request, 4)
                    return redirect('sb:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')

def ditolak_4(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratbesar_admin2["tahap4"]):
                    print('masuk')
                    id_request = request.POST.get("id_request")
                    sb_update(request, id_request, 0)
                    return redirect('sb:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')

def dibatalkan(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in suratbesar_admin2["tahap1"]):
                    id_request = request.POST.get("id_request")
                    sb_update(request, id_request, -1)
                    return redirect('sb:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')


# ---------------------
# Form Tahap 3 Surat Besar
# --------------------
def form3(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = sb_read(id)
                if (user['birdeptim'] in suratbesar_admin2["tahap3"]):
                    if (data_detail["tahapan"] == 2):
                        return render(request, 'surat_besar/tahap3_form.html', {"id": id})
                    else:
                        return redirect("/surat_besar/detail/" + id)
                else:
                    return redirect("/surat_besar/detail/" + id)
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except:
        return redirect("/")


def postForm3(request):
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
            message = sb_update_4(request, id_request, 3, dokumen_meta)
            print(message)
            if message != "terjadi error":
                return redirect("/surat_besar/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/surat_besar/detail/" + id_request)
        else:
            if drive_surat != "":
                message = sb_update_4_drive(request, id_request, 3, drive_surat)
                print(message)
                if message != "terjadi error":
                    return redirect("/surat_besar/detail/" + id_request)
                else:
                    message = "Gagal Upload"
                    return redirect("/surat_besar/detail/" + id_request)
            else:
                message = "Gagal Upload"
                return redirect("/surat_besar/detail/" + id_request)
    except:
        return redirect("/")
