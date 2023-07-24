from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from backend.CRUD.crud_publikasi import publikasi_add_to_notes, publikasi_create, publikasi_delete, publikasi_edit, publikasi_read, publikasi_tolak, publikasi_update
from backend.CRUD.crud_user import user_read
from backend.misc import firebase_init
from linebotpublikasi.views import translateDateToIndo
from .forms import AddNotesForm, DesignLinkForm, PreviewPublicationLinkForm, PublicationRequestCreateForm, PublicationRequestEditForm
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
                    if(is_insidental):
                        bukti_insidental = request.POST.get("bukti_insidental")
                    else:
                        bukti_insidental = None

                    publikasi = request.POST.get("publikas")
                    notes = []

                    if(request.POST.get("notes") != ""):
                        note = {
                            "type": "komen",
                            "time_stamp": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                            "note": request.POST.get("notes"),
                            "writer": current_user.get("panggilan")
                        }
                        notes.append(note)

                    pub_id = publikasi_create(request, judul_konten, date_posted, time_posted, is_insidental, publikasi, notes, bukti_insidental, selected_channels)
                    
                    # ''' --------- LINE PUSH MESSAGE --------- '''

                    # #INSIDENTAL
                    # insidental = ""
                    # if is_insidental:
                    #     insidental = "Ya"
                    #     insidental += f"\n> Bukti Insidental: {bukti_insidental}"
                    # else:
                    #     insidental = "Tidak"
                    # insidental_msg = f'> Insidental : {insidental}'

                    # #DATE_POSTED
                    # date_posted = date_posted.strftime('%A, %d %b %Y')
                    # date_posted = translateDateToIndo(date_posted)

                    # #CHANNELS
                    # pub_request_channels = selected_channels
                    # pub_request_channels_result = ""

                    # for channel in pub_request_channels:
                    #     pub_request_channels_result += f"- {channel}\n"

                    # push_message = f"[PESANAN PUBLIKASI BARU TELAH DATANG!!] \n\nPublikasi baru dengan ID '{pub_id}' telah dibuat.\n\n"
                    # push_message += (f"Judul : {judul_konten}\n\n" 
                    #                 + f"> Peminta : {pub_request.requester}\n"
                    #                 + f"> BirDepTim : {pub_request.birdep_requester}\n"
                    #                 + f"> Tgl Publikasi : \n{date_posted}\n"
                    #                 + f"> Waktu Publikasi : \n{time_posted}\n\n"
                    #                 + f"{insidental_msg}\n\n"
                    #                 + f"> Kanal Publikasi :\n{pub_request_channels_result}\n" 
                    #                 + f"> Bahan Publikasi : {publikasi}\n\n"
                    #                 + f"Lihat pada website : " + request.build_absolute_uri("/publikasi/detail/") + pub_id
                    #                 )
                    # status1 = PublicationStatus.objects.get(status='1')
                    # list_of_line_ids = status1.get_allowed_line_ids_push_message()
                    # if len(list_of_line_ids) != 0:
                    #     for id_line in list_of_line_ids:
                    #         try:
                    #             line_bot_api.push_message(id_line, TextSendMessage(text=push_message))
                    #         except LineBotApiError as e:
                    #             pass

                    # ''' --------- END OF LINE PUSH MESSAGE --------- '''

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
                    #if current status is status '2' or '4', make a form for design links or preview links
                    if data_detail.get("tahapan") == 1:
                        form_pub = DesignLinkForm()
                    elif data_detail.get("tahapan") == 3:
                        form_pub = PreviewPublicationLinkForm()
                    else:
                        form_pub = None
                    
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
                                'form_pub': form_pub
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
        print(e)
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

def add_to_notif(id, tahap, user):
    if(tahap != 4):
        notification_msg = f'Tahap <strong>{tahap_publikasi[tahap]}</strong> telah disetujui oleh <strong>{str(user["nama"])}</strong>. Tahap saat ini: <strong>{tahap_publikasi[tahap+1]}</strong>'
    else:
        notification_msg = f'Tahap <strong>{tahap_publikasi[tahap]}</strong> telah disetujui oleh <strong>{str(user["nama"])}</strong>.'
    
    publikasi_add_to_notes(id, notification_msg, user.get("panggilan"))
    
def diterima_1(request):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in publikasi_admin2["tahap1"]):
                    id_request = request.POST.get("id_request")
                    publikasi_update(request, id_request, 1)
                    add_to_notif(id_request, 0, user)
                    return redirect('publikasi:detail', id=id_request)
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
                if (user['birdeptim'] in publikasi_admin2["tahap2"]):
                    id_request = request.POST.get("id_request")
                    if(request.POST.get("design_link") != ""):
                        design_link = request.POST.get("design_link")
                    else:
                        design_link = ""
                        
                    publikasi_update(request, id_request, 2, design_link)
                    add_to_notif(id_request, 1, user)

                    return redirect('publikasi:detail', id=id_request)
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
                if (user['birdeptim'] in publikasi_admin2["tahap3"]):
                    id_request = request.POST.get("id_request")
                    publikasi_update(request, id_request, 3)
                    add_to_notif(id_request, 3, user)
                    return redirect('publikasi:detail', id=id_request)
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
                if (user['birdeptim'] in publikasi_admin2["tahap4"]):
                    if(request.POST.get("preview_link_instagram") != ""):
                        preview_link_instagram = request.POST.get("preview_link_instagram")
                    else:
                        preview_link_instagram = ""
                        
                    if(request.POST.get("preview_link_twitter") != ""):
                        preview_link_twitter = request.POST.get("preview_link_twitter")
                    else:
                        preview_link_twitter = ""
                        
                    id_request = request.POST.get("id_request")
                    publikasi_update(request, id_request, 4, "", preview_link_instagram, preview_link_twitter)
                    
                    add_to_notif(id_request, 4, user)
                    return redirect('publikasi:detail', id=id_request)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')
        
def declineRequest(request, id: str, tahapan: int):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                if (user['birdeptim'] in publikasi_admin2["admin"]):
                    publikasi_tolak(request, id, tahapan)
                    return redirect('publikasi:detail', id=id)
            else:
                redirect('user:logout')
    except:
        redirect('user:signin')
        
def edit_publikasi(request, id):
    try:
        if (request.session['uid']):
            user_session = fauth.get_account_info(request.session['uid'])
            if (user_session):
                user = user_read(user_session['users'][0]['localId'])
                data_detail = publikasi_read(id)
                if(request.method != "POST"):
                    form = PublicationRequestEditForm(initial = {
                        "program": data_detail.get("judul"),
                        "id_pub_request": data_detail.get("idPermintaan"),  # Replace with appropriate keys from data_detail
                        "date_posted": data_detail.get("date_posted"),
                        "time_posted": data_detail.get("time_posted"),
                        "is_insidental": data_detail.get("is_insidental"),
                        "bukti_insidental": data_detail.get("bukti_insidental"),
                        "publikas": data_detail.get("publikasi"),
                    })
                    if(data_detail.get("idBirdep") == user['id']):
                        return render(request, 'publikasi/form_edit_publication_request.html', {
                            "form": form,
                            "channels": channels,
                            "pub_request_channels": data_detail.get("channels")
                        })
                else:
                    selected_channels = []
                    for key, _ in request.POST.items():
                        if key.startswith("checkboxkanal-"):
                            channel_name = key[len("checkboxkanal-"):]
                            selected_channels.append(channel_name)

                    judul_konten = request.POST.get("program")
                    date_posted = request.POST.get("date_posted")
                    time_posted = request.POST.get("time_posted")
                    is_insidental = request.POST.get("is_insidental")
                    
                    if(is_insidental):
                        bukti_insidental = request.POST.get("bukti_insidental")
                    else:
                        bukti_insidental = None

                    publikasi = request.POST.get("publikas")
                    notes = data_detail.get("notes")
                    note = {
                        "type": "komen",
                        "time_stamp": datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                        "note": "Dilakuakan pengeditan pada publikasi ini.",
                        "writer": user.get("panggilan")
                    }
                    notes.append(note)

                    publikasi_edit(request, id, judul_konten, date_posted, time_posted, is_insidental, publikasi, notes, bukti_insidental, selected_channels)
                    
                    return HttpResponseRedirect(f"/publikasi/detail/{id}")
            else:
                redirect('user:logout')
    except Exception as e:
        print(e)
        redirect('user:signin')