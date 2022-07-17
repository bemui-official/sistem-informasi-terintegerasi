from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from backend.CRUD.crud_ka import ka_read_all_line, ka_read
from backend.CRUD.crud_kr import kr_read_all_line, kr_read
from backend.CRUD.crud_ks import ks_read_all_line, ks_read
from backend.CRUD.crud_sb import sb_read_all_line, sb_read
from backend.CRUD.crud_sk import sk_read_all_line, sk_read

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

# constant
LINK_TO_REQUEST_REIMBURSEMENT = "https://sitbemui.herokuapp.com/reimbursement/detail/"
LINK_TO_REQUEST_ADVANCED = "https://sitbemui.herokuapp.com/advanced/detail/"
LINK_TO_REQUEST_PENYETORAN = "https://sitbemui.herokuapp.com/penyetoran/detail/"
LINK_TO_REQUEST_SURATKELUAR = "https://sitbemui.herokuapp.com/surat_keluar/detail/"
LINK_TO_REQUEST_SURATBESAR = "https://sitbemui.herokuapp.com/surat_besar/detail/"



def index(request):
    return HttpResponse("test!!")


# this is code is modeified from https://github.com/line/line-bot-sdk-python
@csrf_exempt  # this is used for avoid csrf request from line server
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        global domain
        domain = request.META['HTTP_HOST']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# this function is used for process TextMessage from users
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    users_msg = event.message.text
    CMD_NOT_FOUND = (f"Maaf, pesan '{users_msg}' tidak dapat diproses.\n\n"
                     + "Ketik '!sit help' untuk melihat semua perintah yang ada.")
    HELP_MSG_GENERAL = ("[HELP GENERAL] \n\nSelamat datang di SIT BEM UI LineBot!\n\n"
                        + "1.) Ketik '!sit help'\n"
                        + "> Untuk melihat perintah yang ada.\n\n"
                        + "2.) Ketik '!sit list [JENIS DOKUMEN]'\n"
                        + "> Untuk melihat 10 permintaan dengan waktu permintaan terdahulu.\n\n"
                        + "3.) Ketik '!sit [KODE PERMINTAAN] [PASSWORD BOT].'\n"
                        + "> Untuk melihat detail permintaan dari kode permintaan."
                        )
    response = CMD_NOT_FOUND

    if users_msg[:4].lower() == "!sit":

        users_msg = users_msg[5:].strip()

        if users_msg == 'help':
            response = HELP_MSG_GENERAL
        elif users_msg[:4] == 'list':
            print(users_msg)
            users_msg = users_msg[5:].strip()
            if users_msg == "reimbursement":
                data = kr_read_all_line()
            elif users_msg == "advanced":
                data = ka_read_all_line()
            elif users_msg == "penyetoran":
                data = ks_read_all_line()
            elif users_msg == "surat-keluar":
                data = sk_read_all_line()
            elif users_msg == "surat-besar":
                data = sb_read_all_line()

            print(data)
            response = f"[LIST PERMINTAAN "+ users_msg.upper() +"] \n\n10 permintaan dengan waktu permintaan terdahulu:"

            if data:
                for key, val in data:
                    response += f"\n\n{val['judul']}\n> kode ID: {key}\n> Tgl: {val['waktu_pengajuan']}\n> Birdep: {val['nama_birdep']}"
            else:
                response += f"\n\nBelum ada permintaan lagi."
        elif users_msg == 'getidline':
            id_line = 'Error'
            if event.source.type == 'user':
                id_line = event.source.user_id
            elif event.source.type == 'group':
                id_line = event.source.group_id
            elif event.source.type == 'room':
                id_line = event.source.room_id
            response = f"ID Line Anda : {id_line}"
        elif users_msg == '':
            response = f"Halo semua!! Aku adalah Line bot untuk SIT BEM UI.\n\nSetiap perintah yang akan diproses harus didahului dengan kata '!sit' dan perintah selanjutnya dipisahkan dengan spasi. \n\nKetik '!sit help' untuk menampilkan semua perintah yang ada. \n\nTerima kasih telah menggunakan Line bot SIT BEM UI!"
        else:
            kode = users_msg[:2]
            users_msg = users_msg.split()

            if len(users_msg) != 2:
                password = users_msg[1]
                users_msg = users_msg[0]

                isValid = False

                response = ""
                if kode == "kr" and password == "KeuanganSIT":
                    isValid = True
                    data = kr_read(users_msg)
                    link_surat = data['link_voucher']
                    link_web = LINK_TO_REQUEST_REIMBURSEMENT
                elif kode == "ka" and password == "KeuanganSIT":
                    isValid = True
                    data = ka_read(users_msg)
                    link_surat = data['link_voucher']
                    link_web = LINK_TO_REQUEST_ADVANCED
                elif kode == "ks" and password == "KeuanganSIT":
                    isValid = True
                    data = ks_read(users_msg)
                    link_surat = data['link_voucher']
                    link_web = LINK_TO_REQUEST_PENYETORAN
                elif kode == "sk" and password == "SITPenyuratan":
                    isValid = True
                    data = sk_read(users_msg)
                    link_surat = data['link_docs']
                    link_web = LINK_TO_REQUEST_SURATKELUAR
                elif kode == "sb" and password == "SITPenyuratan":
                    isValid = True
                    data = sb_read(users_msg)
                    link_surat = data['link_docs']
                    link_web = LINK_TO_REQUEST_SURATBESAR
                else:
                    response = "Kode tidak valid atau password salah"

                if isValid:
                    response = (f"{users_msg} \n({data['judul']})\n\n"
                                + f"> Status : {data['nama_tahapan']}\n"
                                + f"> Birdeptim : {data['nama_birdep']}\n"
                                + f"> Tgl Permintaan : \n{data['waktu_pengajuan']}\n"
                                + f"> Link Surat : \n{link_surat}\n\n"
                                + f"Lihat pada website : " + link_web + users_msg
                                )
            else:
                response = "Kode tidak valid atau password salah"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))
    else:
        pass
