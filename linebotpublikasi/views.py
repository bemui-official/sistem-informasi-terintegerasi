from django.shortcuts import render
from django.conf import settings 
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils import timezone, dateformat
import datetime

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from backend.CRUD.crud_ka import ka_notification, ka_read
from backend.CRUD.crud_kr import kr_notification, kr_read
from backend.CRUD.crud_ks import ks_notification, ks_read

from backend.CRUD.crud_publikasi import publikasi_notification, publikasi_read
from backend.CRUD.crud_sb import sb_read
from backend.CRUD.crud_sd import sb_notification
from backend.CRUD.crud_sk import sk_notification, sk_read

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

# constant
LINK_TO_REQUEST_PUBLIKASI = "https://sitbemui.com/publikasi/detail/"
LINK_TO_REQUEST_REIMBURSEMENT = "https://sitbemui.com/reimbursement/detail/"
LINK_TO_REQUEST_ADVANCED = "https://sitbemui.com/advanced/detail/"
LINK_TO_REQUEST_PENYETORAN = "https://sitbemui.com/penyetoran/detail/"
LINK_TO_REQUEST_SURATKELUAR = "https://sitbemui.com/surat_keluar/detail/"
LINK_TO_REQUEST_SURATBESAR = "https://sitbemui.com/surat_besar/detail/"

def index(request):
	return HttpResponse("test!")

# this is code is modeified from https://github.com/line/line-bot-sdk-python
@csrf_exempt # this is used for avoid csrf request from line server
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
	HELP_MSG_GENERAL = ("[HELP GENERAL] \n\nSelamat datang di Publikasi SIT BEM UI LineBot!\n\n" 
				+ "1.) Ketik '!sit kode-pub'\n" 
				+ "> (ex: '!sit mulmed-1') untuk melihat status publikasi yang memiliki kode tersebut.\n\n"
				+ "2.) Ketik '!sit kode-pub komentar'\n" 
				+ "> Untuk melihat 5 komentar terakhir yang ada pada publikasi tersebut.\n\n"
				+ "3.) Ketik '!sit p'\n"
				+ "> Untuk melihat 10 publikasi dengan waktu publikasi terdekat. (MULAI DARI HARI INI)\n\n"
				+ "4.) Ketik '!sit ka'\n"
				+ "> Untuk melihat 10 keuangan advanced. (KECUALI YANG SUDAH SELESAI)\n\n"
				+ "5.) Ketik '!sit kr'\n"
				+ "> Untuk melihat 10 keuangan reimbursment. (KECUALI YANG SUDAH SELESAI)\n\n"
				+ "5.) Ketik '!sit ks'\n"
				+ "> Untuk melihat 10 keuangan penyetoran. (KECUALI YANG SUDAH SELESAI)\n\n"
				+ "6.) Ketik '!sit sb'\n"
				+ "> Untuk melihat 10 surat besar yang ada. (KECUALI YANG SUDAH SELESAI)\n\n"
				+ "7.) Ketik '!sit sk'\n"
				+ "> Untuk melihat 10 surat keluar yang ada. (KECUALI YANG SUDAH SELESAI)\n\n"
				+ "8.) Ketik '!sit help'\n"
				+ "> Untuk melihat perintah yang ada.\n\n"
				+ "9.) Ketik '!sit help-humas' atau '!sit help-dkv'\n"
				+ "> Untuk melihat perintah yang ada bagi HUMAS atau DKV."
				)
	HELP_MSG_HUMAS = ("[HELP HUMAS] \n\nHalo Humas! Selamat datang di Publikasi SIT BEM UI LineBot!\n\n" 
				+ "1.) Ketik '!sit kode-pub terima'\n" 
				+ "> (ex: '!sit mulmed-1 terima') untuk menerima dan melanjutkan proses pemesanan publikasi ke status selanjutnya. (Dapat dilakukan pada status tertentu saja)\n\n"
				+ "2.) Ketik '!sit kode-pub tolak'\n" 
				+ "> (ex: '!sit mulmed-1 tolak') untuk menolak dan memundurkan proses pemesanan publikasi ke status sebelumnya. (Dapat dilakukan pada status tertentu saja)\n\n"
				+ "3.) Ketik '!sit kode-pub selesai'\n"
				+ "> (ex: '!sit mulmed-1 selesai') untuk menyelesaikan langsung publikasi apapun statusnya.\n\n"
				+ "4.) Ketik '!sit list-humas'\n"
				+ "> Untuk melihat 10 publikasi yang perlu diperhatikan oleh HUMAS diurutkan dari waktu publikasi terdekat.\n\n"
				+ "5.) Ketik '!sit kode-pub komen komentar-anda'" 
				+ "> Untuk berkomentar pada publikasi tersebut. \nMOHON berkomentar SEBELUM Anda terima atau tolak sebuah publikasi.\n\n"
				+ "6.) Ketik '!sit getidline'\n"
				+ "> Untuk mendapatkan ID Line Anda."
				)
	HELP_MSG_DKV = ("[HELP DKV] \n\nHalo DKV! Selamat datang di Publikasi SIT BEM UI LineBot!\n\n" 
				+ "1.) Ketik '!sit kode-pub terima link-desain'\n" 
				+ "> (Hanya untuk tahap: DESIGN)\n"
				+ "(ex: '!sit mulmed-1 terima https://www.google.com')\n\n"
				+ "2.) [BARU!!] Ketik '!sit kode-pub terima no-link' \n"
				+ "> Jika tidak ingin memberikan link.\n\n"
				+ "3.) Ketik '!sit kode-pub tolak'\n" 
				+ "> (ex: '!sit mulmed-1 tolak') untuk menolak dan memundurkan proses pemesanan publikasi ke status sebelumnya. (Dapat dilakukan pada status DESIGN saja)\n\n"
				+ "4.) Ketik '!sit kode-pub selesai'\n"
				+ "> (ex: '!sit mulmed-1 selesai') untuk menyelesaikan langsung publikasi apapun statusnya.\n\n"
				+ "5.) Ketik '!sit list-dkv'\n"
				+ "> Untuk melihat 10 publikasi yang perlu diperhatikan oleh DKV diurutkan dari waktu publikasi terdekat.\n\n"
				+ "6.) Ketik '!sit kode-pub komen komentar-anda'" 
				+ "> Untuk berkomentar pada publikasi tersebut. \nMOHON berkomentar SEBELUM Anda terima atau tolak sebuah publikasi.\n\n"
				+ "7.) Ketik '!sit getidline'\n"
				+ "> Untuk mendapatkan ID Line Anda."
				)
	response = CMD_NOT_FOUND

	if users_msg[:4].lower() == "!sit":

		users_msg = users_msg[5:].strip()

		if users_msg == 'help':
			response = HELP_MSG_GENERAL
		elif users_msg == 'help-humas':
			response = HELP_MSG_HUMAS
		elif users_msg == 'help-dkv':
			response = HELP_MSG_DKV
		elif users_msg == 'p':
			response = f"[LIST PUBLIKASI TERDEKAT] \n\n10 pesanan publikasi dengan waktu post terdekat (MULAI DARI HARI INI):"
			pub_requests = publikasi_notification([4])
   
			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					#DATE_POSTED
					date_posted_str = pub_request.get("date_posted")

					date_posted = datetime.datetime.strptime(date_posted_str, "%Y-%m-%d")     

					date_posted = translateDateToIndo(date_posted)

					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Tgl: {date_posted}\n> Waktu: {pub_request.get('time_posted')}"
			else:
				response += f"\n\nBelum ada pesanan publikasi lagi."
		elif users_msg == 'ka':
			response = f"[LIST KEUANGAN ADVANCED] \n\n10 permintaan keuangan advanced (KECUALI YANG SUDAH SELESAI):"
			pub_requests = ka_notification()

			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Nama Kegiatan: {pub_request.get('nama_kegiatan')}\n> Nama Birdept: {pub_request.get('nama_birdep')}"
			else:
				response += f"\n\nBelum ada list keuangan advanced lagi."
		elif users_msg == 'kr':
			response = f"[LIST KEUANGAN REIMBURSEMENT] \n\n10 permintaan keuangan reimbursement (KECUALI YANG SUDAH SELESAI):"
			pub_requests = kr_notification()

			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Nama Kegiatan: {pub_request.get('nama_kegiatan')}\n> Nama Birdept: {pub_request.get('nama_birdep')}"
			else:
				response += f"\n\nBelum ada list keuangan reimbursement lagi."
		elif users_msg == 'ks':
			response = f"[LIST KEUANGAN PENYETORAN] \n\n10 permintaan keuangan reimbursement (KECUALI YANG SUDAH SELESAI):"
			pub_requests = ks_notification()

			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Nama Kegiatan: {pub_request.get('nama_kegiatan')}\n> Nama Birdept: {pub_request.get('nama_birdep')}"
			else:
				response += f"\n\nBelum ada list keuangan penyetoran lagi."
		elif users_msg == 'sb':
			response = f"[LIST SURAT BESAR] \n\n10 permintaan SURAT BESAR (KECUALI YANG SUDAH SELESAI):"
			pub_requests = sb_notification()

			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Nama Kegiatan: {pub_request.get('nama_kegiatan')}\n> Nama Birdept: {pub_request.get('nama_birdep')}"
			else:
				response += f"\n\nBelum ada list surat besar lagi."
		elif users_msg == 'sk':
				response = f"[LIST SURAT KELUAR] \n\n10 permintaan SURAT KELUAR (KECUALI YANG SUDAH SELESAI):"
				pub_requests = sk_notification()
				if len(pub_requests) != 0:
					for pub_request in pub_requests:
						print(pub_request.get("nama_kegiatan"))
						response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Nama Kegiatan: {pub_request.get('nama_kegiatan')}\n> Nama Birdept: {pub_request.get('nama_birdep')}"
				else:
					response += f"\n\nBelum ada list surat keluar lagi."
		elif users_msg == 'publikasi-humas':
			response = f"[LIST PUBLIKASI TERDEKAT HUMAS] \n\n10 pesanan publikasi yang perlu diperhatikan oleh HUMAS diurutkan dari waktu post terdekat:"
			pub_requests = publikasi_notification([1, 4])

			
			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					#DATE_POSTED
					date_posted_str = pub_request.get("date_posted")
     
					date_posted = datetime.datetime.strptime(date_posted_str, "%Y-%m-%d")     

					date_posted = translateDateToIndo(date_posted)

					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Tgl: {date_posted}\n> Waktu: {pub_request.get('time_posted')}"
			else:
				response += f"\n\nBelum ada pesanan publikasi lagi."
		elif users_msg == 'publikasi-dkv':
			response = f"[LIST PUBLIKASI TERDEKAT DKV] \n\n10 pesanan publikasi yang perlu diperhatikan oleh DKV diurutkan dari waktu post terdekat:"
			pub_requests = publikasi_notification([0, 2, 3, 4])
			
			if len(pub_requests) != 0:
				for pub_request in pub_requests:
					#DATE_POSTED
					date_posted_str = pub_request.get("date_posted")

					date_posted = datetime.datetime.strptime(date_posted_str, "%Y-%m-%d")   

					date_posted = translateDateToIndo(date_posted)

					response += f"\n\n{pub_request.get('judul')}\n> kode ID: {pub_request.get('idPermintaan')}\n> Tgl: {date_posted}\n> Waktu: {pub_request.get('time_posted')}"
			else:
				response += f"\n\nBelum ada pesanan publikasi lagi."
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
			response = f"Halo semua!! Aku adalah Line bot untuk Publikasi SIT BEM UI.\n\nSetiap perintah yang akan diproses harus didahului dengan kata '!sit' dan perintah selanjutnya dipisahkan dengan spasi. \n\nKetik '!sit help' untuk menampilkan semua perintah yang ada. \n\nTerima kasih telah menggunakan Line bot Publikasi SIT BEM UI!"
		else:
			temp = users_msg.split(" ")
			cmd_and_param = ""

			#cmd_and_param is lowered if its not a 'komen' command
			if len(temp) > 1 and temp[1].lower() == "komen":
				cmd_and_param = users_msg.split(" ")
				cmd_and_param[0] = cmd_and_param[0].lower()
				cmd_and_param[1] = cmd_and_param[1].lower()
			else:
				cmd_and_param = users_msg.lower().split(" ")

			kode = cmd_and_param[0].split("-")[0]

			isValid = True
			if(kode == "publikasi"):
				isValid = False
				pub_request = publikasi_read(cmd_and_param[0])
				if pub_request:
					#INSIDENTAL
					insidental = ""
					if pub_request.get("is_insidental") == "True":
						insidental = "Ya"
						insidental += f"\n> Bukti Insidental: {pub_request.get('bukti_insidental')}"
					else:
						insidental = "Tidak"
					insidental_msg = f'> Insidental : {insidental}'

					#Link Publikasi
					design_link = '> Link Publikasi : '
					if pub_request.get("link_publikasi"):
						design_link += pub_request.get("link_publikasi")
					else:
						design_link = '> Belum ada link desain publikasi yang diberikan.'

					#DATE_POSTED
					date_posted_str = pub_request.get("date_posted")

					date_posted = datetime.datetime.strptime(date_posted_str, "%Y-%m-%d")     

					date_posted = translateDateToIndo(date_posted)

					#CHANNELS
					pub_request_channels = pub_request.get("channels")
					pub_request_channels_result = ""

					for channel in pub_request_channels:
						pub_request_channels_result += f"- {channel}\n"

					response = (f"{pub_request.get('judul')} \n({pub_request.get('idPermintaan')})\n\n" 
								+ f"> Status : {pub_request.get('nama_tahapan')}\n"
								+ f"> Peminta : {pub_request.get('nama_birdep')}\n"
								+ f"> Tgl Publikasi : \n{date_posted}\n"
								+ f"> Waktu Publikasi : \n{pub_request.get('time_posted')}\n\n"
								+ f"{insidental_msg}\n\n"
								+ f"> Kanal Publikasi :\n{pub_request_channels_result}\n" 
								+ f"> Bahan Publikasi : {pub_request.get('publikasi')}\n"
								+ f"{design_link}\n\n"
								+ f"Lihat pada website : " + LINK_TO_REQUEST_PUBLIKASI + pub_request.get("idPermintaan")
								)
			elif (kode == "ka"):
				pub_request = ka_read(cmd_and_param[0])
				link_web = LINK_TO_REQUEST_ADVANCED
			elif (kode == "kr"):
				pub_request = kr_read(cmd_and_param[0])
				link_web = LINK_TO_REQUEST_REIMBURSEMENT
			elif(kode == "ks"):
				pub_request = ks_read(cmd_and_param[0])
				link_web = LINK_TO_REQUEST_PENYETORAN
			elif(kode == "sb"):
				pub_request = sb_read(cmd_and_param[0])
				link_web = LINK_TO_REQUEST_SURATBESAR
			elif(kode == "sk"):
				pub_request = sk_read(cmd_and_param[0])
				link_web = LINK_TO_REQUEST_SURATKELUAR
			        
			elif pub_request and len(cmd_and_param) == 2 and cmd_and_param[1] == "komentar":
				notes_writers = pub_request.publicationnotes.get_writers()
				notes_writers.reverse()
				notes_timestamps = pub_request.publicationnotes.get_notes_timestamps()
				notes_timestamps.reverse()
				notes = pub_request.publicationnotes.get_notes()
				notes.reverse()

				response = f"5 Notes terakhir pada publikasi '{pub_request.id}':"
				if len(notes) > 0:
					for i in range(0, 5):
						if len(notes) > 4-i:
							response += f"\n\n{notes_writers[4-i]}\n"
							response += f"{notes_timestamps[4-i]}\n"
							note = notes[4-i].replace("<strong>", "").replace("</strong>", "")
							response += f"> {note}"
				else:
					response += "\n\nBelum ada notes pada publikasi ini"
			# elif pub_request and (len(cmd_and_param) == 3 or len(cmd_and_param) == 2) and cmd_and_param[1] == "terima":
			# 	response = terima_publikasi(event, pub_request, cmd_and_param)
			# elif pub_request and len(cmd_and_param) <= 3 and cmd_and_param[1] == "tolak":
			# 	if len(cmd_and_param) == 3:
			# 		response = f"Pesan '{cmd_and_param[2]}' tidak dapat diproses. Silakan coba lagi."
			# 	elif len(cmd_and_param) == 2:
			# 		response = tolak_publikasi(event, pub_request)
			# 	else:
			# 		response = CMD_NOT_FOUND
			# elif pub_request and len(cmd_and_param) == 2 and cmd_and_param[1] == 'selesai':
			# 	response = selesai_publikasi(event, pub_request)
			# elif pub_request and len(cmd_and_param) > 2 and cmd_and_param[1] == 'komen':
			# 	response = comment_on_pub_request(event, pub_request, cmd_and_param)
		if not pub_request and len(cmd_and_param) > 0 and cmd_and_param[0] != "":
			response = f"Tidak ada id dengan kode '{cmd_and_param[0]}'. Silakan coba lagi."

		if isValid and pub_request:
			if(kode == "kr" or kode == "ks" or kode == "ka"):
				link_surat = pub_request.get('link_voucher')
			else:
				link_surat = pub_request.get('link_docs')

			response = (f"{users_msg} \n({pub_request.get('judul')})\n\n"
						+ f"> Status : {pub_request.get('nama_tahapan')}\n"
						+ f"> Birdeptim : {pub_request.get('nama_birdep')}\n"
						+ f"> Tgl Permintaan : \n{pub_request.get('waktu_pengajuan')}\n"
						+ f"> Link Surat : \n{link_surat}\n\n"
						+ f"Lihat pada website : " + link_web + users_msg
						)
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=response))
	else:
		pass


''' -------------------------- Custom Methods ------------------------------- '''

def translateDateToIndo(date):
	date = date.strftime('%A, %d %b %Y')
	
	idx = date.find(",")
	date_en = date[:idx].lower()
	date_id = date[idx:]

	if date_en == "monday":
		date_en = "Senin"
	elif date_en == "tuesday":
		date_en = "Selasa"
	elif date_en == "wednesday":
		date_en = "Rabu"
	elif date_en == "thursday":
		date_en = "Kamis"
	elif date_en == "friday":
		date_en = "Jumat"
	elif date_en == "saturday":
		date_en = "Sabtu"
	elif date_en == "sunday":
		date_en = "Minggu"

	date_id = date_id.replace("May", "Mei")
	date_id = date_id.replace("Oct", "Okt")
	date_id = date_id.replace("Dec", "Des")

	date_id = date_en + date_id

	return date_id


# def terima_publikasi(event, pub_request, cmd_and_param):
# 	id_line = None
# 	result = ''

# 	if event.source.type == 'user':
# 		id_line = event.source.user_id
# 	elif event.source.type == 'group':
# 		id_line = event.source.group_id
# 	elif event.source.type == 'room':
# 		id_line = event.source.room_id

# 	users = CustomUser.objects.filter(id_line = id_line)
	
# 	authorization_result = publication_request_authorization(pub_request, users)

# 	user_authorized = authorization_result[0]
# 	user = authorization_result[1]

# 	if user_authorized:
# 		skip = False

# 		if pub_request.status.next is None:
# 			result = f"Publikasi dengan kode '{pub_request.id}' sudah di status 'Published' dan tidak dapat diterima lagi."
# 			skip = True

# 		if pub_request.status.status == '2' and not skip:
# 			if len(cmd_and_param) == 3 and is_URL_valid(cmd_and_param[2]):
# 				pub_request.design_link = cmd_and_param[2]
# 			elif len(cmd_and_param) == 3 and cmd_and_param[2] == "no-link":
# 				pass
# 			else:
# 				if len(cmd_and_param) == 2:
# 					result = f"Publikasi dengan kode '{pub_request.id}' ini sedang berada di status 'Design'. Oleh karena itu Anda perlu memberikan link desain publikasi. \n\nKetik '!sit {pub_request.id} terima link-desain-publikasi' \n\n(CONTOH: '!sit {pub_request.id} terima https://www.google.com')\n\n[BARU! TIDAK PERLU LINK?]\nJika tidak ingin memberikan link, ketik '!sit {pub_request.id} terima no-link'"
# 				elif not is_URL_valid(cmd_and_param[2]):
# 					result = f"Link yang Anda berikan ({cmd_and_param[2]}) tidak valid. Silakan coba lagi. \n\nContoh URL yang valid: \nhttps://www.google.com"
# 				skip = True
# 		else:
# 			if len(cmd_and_param) == 3 and not skip:
# 				result = f"Pesan '{cmd_and_param[2]}' tidak dapat diproses. Silakan coba lagi."
# 				skip = True

# 		if not skip:
# 			msg_current = pub_request.status.message
# 			msg_next = pub_request.status.next.message

# 			result = f"Tahap '{msg_current}' telah disetujui oleh Anda ({str(user)}). Tahap saat ini: '{msg_next}' \n\nLihat pada website: {LINK_TO_REQUEST}{pub_request.id}"

# 			pub_request.status = pub_request.status.next
# 			pub_request.save()


# 			''' ADD NOTIFICATION TO NOTES '''
# 			#add notification to notes with custom method addNotificationToNotes
# 			notification_msg = f'Tahap <strong>{msg_current}</strong> telah disetujui oleh <strong>{str(user)}</strong>. Tahap saat ini: <strong>{msg_next}</strong> (LINE)'
# 			addNotificationToNotes(pub_request, True, notification_msg, str(user))


# 			''' SENDING EMAIL '''
# 			#Get groups who will get the email
# 			allowed_groups_verify = pub_request.status.get_allowed_groups_verify()
# 			if pub_request.status.status == '5' or pub_request.status.status == '4':
# 				list_involved = []
# 			else:
# 				list_involved = getUsersToBeRecipient(allowed_groups_verify)

# 			#Add publication requester to the list_involved
# 			list_involved.append(pub_request.requester.email)

# 			#send email after accepting
# 			#to people involved
# 			email_subject = f'Tahap "{msg_current}" "{pub_request.id}" Disetujui!'
# 			email_message = f'Tahap "{msg_current}" pada request dengan id "{pub_request.id}" telah disetujui oleh {str(user)}. Tahap saat ini: "{msg_next}". \n\n {LINK_TO_REQUEST}{pub_request.id}'
# 			email_to_list = list_involved
# 			send_email(email_subject, email_message, email_to_list)
# 	else:
# 		result = f"Maaf, Anda (LINE ID: {id_line}) tidak dapat melakukan perintah ini pada publikasi '{pub_request.id}'. \n\nJika menurut Anda ada kesalahan, mohon hubungi Biro Multimedia BEM UI."

# 	return result


# def tolak_publikasi(event, pub_request):
# 	id_line = None
# 	result = ''

# 	if event.source.type == 'user':
# 		id_line = event.source.user_id
# 	elif event.source.type == 'group':
# 		id_line = event.source.group_id
# 	elif event.source.type == 'room':
# 		id_line = event.source.room_id

# 	users = CustomUser.objects.filter(id_line = id_line)

# 	authorization_result = publication_request_authorization(pub_request, users)

# 	user_authorized = authorization_result[0]
# 	user = authorization_result[1]

# 	if user_authorized:
# 		skip = False
			
# 		msg_current = pub_request.status.message

# 		if pub_request.status.prev.first() is not None:
# 			if pub_request.status.status == '4':
# 				pub_request.status = pub_request.status.prev.first().prev.first()
# 			else:
# 				pub_request.status = pub_request.status.prev.first()

# 		msg_prev = pub_request.status.message

# 		if not skip:
# 			result = f"Tahap '{msg_current}' telah ditolak oleh Anda ({str(user)}). Tahap saat ini: '{msg_prev}' \n\nLihat pada website: {LINK_TO_REQUEST}{pub_request.id}"

# 			pub_request.save()


# 			''' ADD NOTIFICATION TO NOTES '''
# 			notification_msg = f'Tahap <strong>{msg_current}</strong> telah ditolak oleh <strong>{str(user)}</strong>. Tahap saat ini: <strong>{msg_prev}</strong> (LINE)'
# 			addNotificationToNotes(pub_request, False, notification_msg, str(user))


# 			''' SENDING EMAIL '''
# 			#Get groups who will get the email
# 			allowed_groups_verify = pub_request.status.get_allowed_groups_verify()
# 			list_involved = getUsersToBeRecipient(allowed_groups_verify)

# 			#Add publication requester to the list_involved
# 			list_involved.append(pub_request.requester.email)

# 			#send email after declining
# 			#to people involved
# 			email_subject = f'Tahap "{msg_current}" "{pub_request.id}" Ditolak!'
# 			email_message = f'Tahap "{msg_current}" pada request dengan id "{pub_request.id}" telah ditolak oleh {str(user)}. Tahap saat ini: "{msg_prev}". \n\n {LINK_TO_REQUEST}{pub_request.id}'
# 			email_to_list = list_involved
# 			send_email(email_subject, email_message, email_to_list)
# 	else:
# 		result = f"Maaf, Anda (LINE ID: {id_line}) tidak dapat melakukan perintah ini pada publikasi '{pub_request.id}'. \n\nJika menurut Anda ada kesalahan, mohon hubungi Biro Multimedia BEM UI."

# 	return result


# def selesai_publikasi(event, pub_request):
# 	id_line = None
# 	result = ''

# 	if event.source.type == 'user':
# 		id_line = event.source.user_id
# 	elif event.source.type == 'group':
# 		id_line = event.source.group_id
# 	elif event.source.type == 'room':
# 		id_line = event.source.room_id

# 	users = CustomUser.objects.filter(id_line = id_line)

# 	authorization_result = publication_request_authorization(pub_request, users)

# 	user_authorized = authorization_result[0]
# 	user = authorization_result[1]

# 	if user_authorized:
# 		skip = False

# 		if pub_request.status.next is None:
# 			result = f"Publikasi dengan kode '{pub_request.id}' sudah di status 'Published' dan tidak dapat disetujui lagi."
# 			skip = True

# 		if not skip:
# 			msg_current = pub_request.status.message

# 			#Next status until next is None
# 			while pub_request.status.next is not None:
# 				pub_request.status = pub_request.status.next

# 			pub_request.save()

# 			msg_next = pub_request.status.message

# 			result = f"Publikasi ({pub_request.id}) telah diselesaikan oleh Anda ({str(user)}). Tahap '{msg_current}' telah menjadi tahap '{msg_next}' \n\nLihat pada website: {LINK_TO_REQUEST}{pub_request.id}"


# 			''' ADD NOTIFICATION TO NOTES '''
# 			#add notification to notes with custom method addNotificationToNotes
# 			notification_msg = f'Permintaan Publikasi ini telah diselesaikan oleh <strong>{str(user)}</strong>. \nTahap <strong>{msg_current}</strong> telah menjadi tahap <strong>{msg_next}</strong> (LINE)'
# 			addNotificationToNotes(pub_request, True, notification_msg, str(user))


# 			''' SENDING EMAIL '''
# 			#Get groups who will get the email (no one for finish publication request)
# 			list_involved = []

# 			#Add publication requester to the list_involved
# 			list_involved.append(pub_request.requester.email)

# 			#send email after accepting
# 			#to people involved
# 			email_subject = f'Permintaan Publikasi "{pub_request.id}" Sudah Diselesaikan!'
# 			email_message = f'Permintaan Publikasi dengan id "{pub_request.id}" telah diselesaikan oleh {str(user)}. Tahap "{msg_current}" telah menjadi tahap "{msg_next}". \n\n {LINK_TO_REQUEST}{pub_request.id}'
# 			email_to_list = list_involved
# 			send_email(email_subject, email_message, email_to_list)
# 	else:
# 		result = f"Maaf, Anda (LINE ID: {id_line}) tidak dapat melakukan perintah ini pada publikasi '{pub_request.id}'. \n\nJika menurut Anda ada kesalahan, mohon hubungi Biro Multimedia BEM UI."

# 	return result


def is_URL_valid(URL):
	URL = URL.lower()

	if "http" in URL[:4]:
		if "://" in URL:
			if "." in URL[URL.find("/"):]:
				return True
	return False


def publication_request_authorization(pub_request, users):
	'''
	(MODIFIED from a method from main with the same name)
	custom method for authorization to verify publication requests
	parameter: <PublicationRequest> publication request, <List of CustomUser> list of users that have a certain line_id
	return: Boolean (True if authorized to verify request), (False if not)
	'''
	pub_request_status = pub_request.status
	lst_allowed_groups_verify = pub_request_status.get_allowed_groups_verify()
	lst_allowed_users_verify = pub_request_status.get_allowed_users_verify()

	user_authorized = False
	the_user = None

	if users:
		for user in users:
			users_groups = user.groups.values_list('name', flat = True)
			users_email = user.email

			if any(e in lst_allowed_groups_verify for e in users_groups) or (users_email in lst_allowed_users_verify):
				user_authorized = True
				the_user = user
				break
			else:
				user_authorized = False
	else:
		user_authorized = False

	result = [user_authorized, the_user]

	return result


# def comment_on_pub_request(event, pub_request, cmd_and_param):
# 	id_line = None
# 	result = ''

# 	if event.source.type == 'user':
# 		id_line = event.source.user_id
# 	elif event.source.type == 'group':
# 		id_line = event.source.group_id
# 	elif event.source.type == 'room':
# 		id_line = event.source.room_id

# 	users = CustomUser.objects.filter(id_line = id_line)
	
# 	authorization_result = publication_request_authorization(pub_request, users)

# 	user_authorized = authorization_result[0]
# 	user = authorization_result[1]

# 	if user_authorized:
# 		''' ADD NOTIFICATION TO NOTES '''
# 		#add notes with custom method addNotificationToNotes
# 		separator = " "
# 		notification_msg = separator.join(cmd_and_param[2:])
# 		addNotificationToNotes(pub_request, None, notification_msg, str(user))

# 		result = f"Terima kasih, komentar Anda telah berhasil direkam."
# 	else:
# 		result = f"Maaf, Anda (LINE ID: {id_line}) tidak dapat melakukan perintah ini pada publikasi '{pub_request.id}'. \n\nJika menurut Anda ada kesalahan, mohon hubungi Biro Multimedia BEM UI."

# 	return result
	

# def getUsersToBeRecipient(allowed_groups_verify, type=None):
# 	list_involved = []
# 	temp_list = []

# 	if 'Biro Hubungan Masyarakat' in allowed_groups_verify:
# 		temp_list = CustomUser.objects.filter(groups__name='Biro Hubungan Masyarakat')
# 	elif 'Biro Desain Komunikasi Visual' in allowed_groups_verify:
# 		temp_list = CustomUser.objects.filter(groups__name='Biro Desain Komunikasi Visual')
	
# 	if type == "notifikasi":
# 		for user in temp_list:
# 			list_involved.append(user.email)
# 	else:
# 		for user in temp_list:
# 			if user.subscribe_to_email:
# 				list_involved.append(user.email)

# 	return list_involved


def send_email(email_subject, email_message, emailt_to_list):

	#send email only if host's email and password is set
	if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD and len(emailt_to_list) > 0:
		send_mail(
			email_subject, # subject
			email_message, # message
			settings.EMAIL_HOST_USER, # from
			emailt_to_list, # to
			)