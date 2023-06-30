from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from backend.CRUD.crud_publikasi import publikasi_add_to_notes, publikasi_create, publikasi_delete, publikasi_read
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
from .forms import AddNotesForm, PublicationRequestCreateForm
from backend.constants.admins import publikasi_admin, publikasi_admin2 
from backend.constants.tahapan import tahap_publikasi
from datetime import datetime

fauth = firebase_init

channels = [
    {"name_label": "IG Feed"},
    {"name_label": "IG Story"},
    {"name_label": "IG Highlight"},
    {"name_label": "IG Guide"},
    {"name_label": "IG TV"},
    {"name_label": "IG Reels"},
    {"name_label": "Line OA"},
    {"name_label": "Line Today"},
    {"name_label": "Twitter"},
    {"name_label": "Youtube"},
    {"name_label": "TikTok"},
    {"name_label": "Facebook"},
    {"name_label": "Linkedin"},
    {"name_label": "Uinfo"},
    {"name_label": "Webiste"},
    {"name_label": "Spotify"},
]
# Create your views here.
def formPublikasi(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            current_user = user_read(user_session['users'][0]['localId']) # To make sure that they are still authenticated
            if (user_session):
                if(request.method != "POST"):
                    form = PublicationRequestCreateForm()
                    return render(request, 'publikasi/form_create_publication_request.html', {
                        "form": form,
                        "channels": channels
                    })
                else : 
                    selected_channels = []
                    for key, _ in request.POST.items():
                        if key.startswith("checkboxkanal-"):
                            channel_name = key[len("checkboxkanal-"):]
                            selected_channels.append(channel_name)

                    judul_konten = request.POST.get("program")
                    date_posted = request.POST.get("date_posted")
                    time_posted = request.POST.get("time_posted")
                    is_insidental = request.POST.get("is_insidental")
                    publikasi = request.POST.get("publikas")
                    notes = []
                    note = {
                        "type": "komen",
                        "time_stamp": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                        "note": request.POST.get("notes"),
                        "writer": current_user.get("panggilan")
                    }
                    notes.append(note)
                    bukti_insidental = request.POST.get("bukti_is_insidental")

                    publikasi_create(request, judul_konten, date_posted, time_posted, is_insidental, publikasi, notes, bukti_insidental, selected_channels)
                    
                    return HttpResponseRedirect("/")
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")

def spo_publikasi(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            user_read(user_session['users'][0]['localId']) # To make sure that they are still authenticated
            if (user_session):
                return render(request, 'publikasi/spo.html')
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")
    

# ---------------------
# Detail Publikasi
# --------------------
def detail(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            current_user = user_read(user_session['users'][0]['localId']) # To make sure that they are still authenticated
            if (user_session):
                if(request.method != "POST"):
                    form = AddNotesForm()
                    data_detail = publikasi_read(id)
                    user = user_read(user_session['users'][0]['localId'])
                    if (data_detail != []):
                        data_detail['date_posted'] = datetime.strptime(data_detail['date_posted'], '%Y-%m-%d')
                        if (user["id"] == data_detail["idBirdep"] or user['birdeptim'] in publikasi_admin2["admin"]):
                            return render(request, 'publikasi/publikasi_details.html', {
                                'data': data_detail,
                                'user': user,
                                'admin': publikasi_admin,
                                'id': id,
                                'tahap': tahap_publikasi,
                                'form': form,
                            })
                        else:
                            raise Http404
                else:
                    current_url = request.build_absolute_uri()
                    publikasi_id = current_url.strip().split("/")[-1]
                    
                    message = publikasi_add_to_notes(publikasi_id, request.POST.get("notes"), current_user.get("panggilan"))
                    
                    if(message != "terjadi error"):
                        return HttpResponseRedirect(current_url);
                    else:
                        return redirect("/user/signin")
            else:
                return redirect("/user/logout")
        else:
            return redirect("/user/signin")
    except Exception as e:
        return redirect("/user/signin")

def delete_publikasi(request):
    try: 
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            user = user_read(user_session['users'][0]['localId']) # To make sure that they are still authenticated
            if (user_session):
                if (user['birdeptim'] in publikasi_admin2["admin"]):
                    id_request = request.POST.get("id_request")
                    publikasi_delete(id_request)
                    return redirect('../../user/dashboard/publikasi/semua')
            else:
                return redirect("/user/logout")
    except:
        return redirect("/user/signin")
    
def edit_publikasi(request): 
    pass