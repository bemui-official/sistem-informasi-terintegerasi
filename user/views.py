from django.http import Http404
from django.shortcuts import render, redirect
from backend.CRUD.crud_publikasi import publikasi_read_all, publikasi_read_requests

from backend.CRUD.crud_sb import sb_read_all, sb_read_requests
from backend.CRUD.crud_user import user_create, user_read, user_update_admin
from backend.CRUD.crud_dashboard import read_requests
from django.contrib import auth

from backend.constants.tahapan import tahap_reimbursement, tahap_advanced, tahap_penyetoran, tahap_surat_keluar, tahap_surat_besar, tahap_publikasi
from backend.misc import firebase_init
from backend.constants.birdeptim import pi, birdeptim, kode_fungsionaris

from backend.CRUD.crud_kr import kr_read_requests, kr_read_all
from backend.CRUD.crud_ka import ka_read_requests, ka_read_all
from backend.CRUD.crud_ks import ks_read_requests, ks_read_all
from backend.CRUD.crud_sk import sk_read_requests, sk_read_all

from django.views.decorators.csrf import csrf_protect

fauth = firebase_init


# ---------------------
# Authentication
# --------------------
def signUp(request):
	return render(request, 'signUp.html', {
		"pi": pi,
		"birdeptim": birdeptim,
		"kode_fungsionaris": kode_fungsionaris
	})

@csrf_protect
def postSignUp(request):
	try:
		idBirdep = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password1")
		password2 = request.POST.get("password2")
		asal = request.POST.get("asal")
		nama = request.POST.get("nama")
		panggilan = request.POST.get("panggilan")
		birdeptim = request.POST.get("birdeptim")
		permintaan = []
		if (password == password2):
			message = user_create(idBirdep, email, password, asal, nama, 0, panggilan, permintaan, birdeptim)
		if message == "":
			return redirect("user:signin")
		else:
			return redirect("user:signup")
	except:
		return redirect("user:signup")

def signIn(request):
	return render(request, 'signIn.html')

@csrf_protect
def postSignIn(request):
	try:
		email = request.POST.get("email")
		password = request.POST.get("password")
		try:
			user = fauth.sign_in_with_email_and_password(email, password)
		except:
			return redirect(signIn)
		print(user)
		session_id = user['idToken']
		request.session['uid'] = str(session_id)
		if email == 'admin_sit@admin.com':
			request.session['admin'] = True
		else:
			request.session['admin'] = False
		print(request.session['uid'])
		return redirect('/')
	except:
		return redirect("user:signin")

def logout(request):
	auth.logout(request)
	return redirect("user:signin")


# ---------------------
# Dashboard
# --------------------
def dashboard(request, category, sort):
	try:
		if (request.session['uid']):
			user_session = fauth.get_account_info(request.session['uid'])
			if (user_session):
				user = user_read(user_session['users'][0]['localId'])
				print(user['id'])
				data = []
				tahapan = []
				judul = "Home Dashboard"
				if category == 'reimbursement':
					data = kr_read_requests(user['id'], sort)
					judul = "Keuangan - Reimbursement"
					tahapan = tahap_reimbursement
				elif category == "advanced":
					data = ka_read_requests(user['id'], sort)
					judul = "Keuangan - Cash Advanced"
					tahapan = tahap_advanced
				elif category == "penyetoran":
					data = ks_read_requests(user['id'], sort)
					judul = "Keuangan - Penyetoran"
					tahapan = tahap_penyetoran
				elif category == "surat_keluar":
					data = sk_read_requests(user["id"], sort)
					judul = "Surat Menyurat - Surat"
					tahapan = tahap_surat_keluar
				elif category == "surat_besar":
					data = sb_read_requests(user["id"], sort)
					judul = "Dokumen - Surat"
					tahapan = tahap_surat_besar
				elif category == "publikasi":
					if(user['birdeptim'] not in ["201", "202", "203"]):
						data = publikasi_read_requests(user["id"], sort)
					else:
						data = publikasi_read_all(sort)

					judul = "Publikasi"
					tahapan = tahap_publikasi
					data.reverse() 
				def extract_time(json):
					try:
						# Also convert to int since update_time will be string.  When comparing
						# strings, "10" is smaller than "2".
						return json['waktu_pengajuan']
					except KeyError:
						return 0

				# lines.sort() is more efficient than lines = lines.sorted()
				if(category != "publikasi"):
					data.sort(key=extract_time, reverse=False)

				hostname = request.build_absolute_uri("/")
				print(request.get_full_path)
				return render(request, 'dashboard.html', {
					'datas': data,
					'user': user,
					'judul': judul,
					'hostname': hostname,
					'category': category,
					'tahapan': tahapan,
				})
			else:
				return redirect("/user/logout")
	except:
		return redirect("/user/signin")

def dashboard_pengurus(request, category, sort):
	try:
		if (request.session['uid']):
			user_session = fauth.get_account_info(request.session['uid'])
			if (user_session):
				user = user_read(user_session['users'][0]['localId'])
				print(user['id'])
				data = []
				tahapan = []
				judul = "Home Dashboard"
				if user["admin"]:
					if category == 'reimbursement' and 'keuangan' in user['admin']:
						data = kr_read_all(sort)
						judul = "Keuangan - Reimbursement"
						tahapan = tahap_reimbursement
					elif category == "advanced" and 'keuangan' in user['admin']:
						data = ka_read_all(sort)
						judul = "Keuangan - Cash Advanced"
						tahapan = tahap_advanced
					elif category == "penyetoran" and 'keuangan' in user['admin']:
						data = ks_read_all(sort)
						judul = "Keuangan - Penyetoran"
						tahapan = tahap_penyetoran
					elif category == "surat_keluar" and 'surat' in user['admin']:
						data = sk_read_all(sort)
						judul = "Surat Menyurat - Surat"
						tahapan = tahap_surat_keluar
					elif category == "surat_besar" and 'surat' in user['admin']:
						data = sb_read_all(sort)
						judul = "Dokumen - Surat"
						tahapan = tahap_surat_besar
					elif category == "publikasi":
						data = publikasi_read_all(sort)
						judul = "Publikasi"
						tahapan = tahap_publikasi
					hostname = request.build_absolute_uri("/")

					def extract_time(json):
						try:
							# Also convert to int since update_time will be string.  When comparing
							# strings, "10" is smaller than "2".
							return json['waktu_pengajuan']
						except KeyError:
							return 0

					# lines.sort() is more efficient than lines = lines.sorted()

     
					if(category != "publikasi"):
						data.sort(key=extract_time, reverse=False)

					return render(request, 'dashboard_pengurus.html', {
						'datas': data,
						'user': user,
						'judul': judul,
						'hostname': hostname,
						'category': category,
						'tahapan': tahapan,
					})
				else:
					raise Http404
			else:
				return redirect("/user/logout")
	except:
		return redirect("/user/signin")

def give_permission(request):
	try:
		if (request.session['uid']):
			user_session = fauth.get_account_info(request.session['uid'])
			if (user_session):
				user = user_read(user_session['users'][0]['localId'])
				if(user['super_admin']):
					return render(request, 'give_permission.html')
				else:
					raise Http404
			else:
				return redirect("/user/logout")
	except:
	    return redirect("/user/signin")

def post_give_permission(request):
	id = request.POST.get("id")
	kode = request.POST.get("kode")

	user_update_admin(id, kode)
	return redirect('/')